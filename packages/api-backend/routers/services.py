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


@router.post("/{service_id}/refresh-doc")
def refresh_service_doc(service_id: str, doc_url: str = Query(..., description="Public URL of the latest service spec")):
    """Pull the latest service documentation snippet from an external source."""
    service = next((s for s in SERVICES if s["id"] == service_id), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found.")
    response = urlopen(doc_url, timeout=5)
    body = response.read(4096).decode("utf-8", errors="replace")
    service["doc_excerpt"] = body
    return ok({"service_id": service_id, "bytes": len(body)})


@router.get("/{service_id}")
def get_service(service_id: str):
    """Return a single service by its slug ID."""
    service = next((s for s in SERVICES if s["id"] == service_id), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found.")
    return ok(service)
