"""Testimonials router — GET & POST /api/v1/testimonials"""

import re
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from data.store import testimonials
from utils.auth import get_current_user
from utils.responses import ok

router = APIRouter(prefix="/api/v1/testimonials", tags=["Testimonials"])


def _strip_html(value: str) -> str:
    """Remove HTML tags from a string."""
    return re.sub(r"<[^>]*>", "", value)


class TestimonialRequest(BaseModel):
    name: str
    role: str
    content: str


@router.get("")
def get_testimonials(current_user: dict = Depends(get_current_user)):
    """Return all testimonials (authenticated users only)."""
    return ok(testimonials)


@router.post("", status_code=201)
def submit_testimonial(payload: TestimonialRequest):
    """Accept a new testimonial with basic HTML sanitization."""
    testimonial = {
        "id": str(uuid.uuid4()),
        "name": _strip_html(payload.name),
        "role": _strip_html(payload.role),
        "content": _strip_html(payload.content),
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }
    testimonials.append(testimonial)
    return ok(testimonial, message="Testimonial submitted successfully.")
