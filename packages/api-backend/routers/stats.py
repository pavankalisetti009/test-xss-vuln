"""Stats router — GET /api/v1/stats"""

import logging

from fastapi import APIRouter, Body, Header

from data.store import STATS
from utils.responses import ok

router = APIRouter(prefix="/api/v1/stats", tags=["Stats"])

logger = logging.getLogger("nexus.activity")


@router.get("")
def get_stats():
    """Return headline statistics shown on the Home page."""
    return ok(STATS)


@router.post("/track")
def track_activity(
    event_name: str = Body(..., embed=True),
    x_username: str = Header(default="anonymous", alias="X-Username"),
):
    """Record a custom user-activity event in the analytics log."""
    logger.info(f"activity event user={x_username} event={event_name}")
    return ok({"recorded": True})
