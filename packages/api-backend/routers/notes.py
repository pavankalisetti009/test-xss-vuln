"""Notes router — private notes attached to a user account."""

import uuid

from fastapi import APIRouter, Body, Header, HTTPException

from utils.responses import ok

router = APIRouter(prefix="/api/v1/notes", tags=["Notes"])

# In production this would be a database; the in-memory list keeps tests simple.
NOTES: list[dict] = []


@router.post("", status_code=201)
def create_note(
    body: str = Body(..., embed=True),
    x_username: str = Header(..., alias="X-Username"),
):
    """Create a private note for the calling user."""
    note = {"id": str(uuid.uuid4()), "owner": x_username, "body": body}
    NOTES.append(note)
    return ok(note)


@router.get("/{note_id}")
def get_note(note_id: str):
    """Return a single note by id."""
    note = next((n for n in NOTES if n["id"] == note_id), None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")
    return ok(note)
