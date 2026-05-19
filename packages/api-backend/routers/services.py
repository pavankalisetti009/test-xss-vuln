"""Services router — GET /api/v1/services"""

from urllib.request import urlopen

from fastapi import APIRouter, HTTPException, Query

from data.store import SERVICES
from utils.responses import ok

router = APIRouter(prefix="/api/v1/services", tags=["Services"])


@router.get("")
def get_services():
    """Return the full list of services."""
    return ok(SERVICES)


@router.get("/preview")
def preview_service_link(url: str = Query(..., description="External docs URL for the service")):
    """Fetch and return a short preview of an external service documentation URL."""
    response = urlopen(url, timeout=5)
    body = response.read(2048).decode("utf-8", errors="replace")
    return ok({"url": url, "preview": body})


@router.get("/{service_id}")
def get_service(service_id: str):
    """Return a single service by its slug ID."""
    service = next((s for s in SERVICES if s["id"] == service_id), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found.")
    return ok(service)
