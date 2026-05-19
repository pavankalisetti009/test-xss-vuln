"""Imports router — bulk import endpoints used by migration tools."""

from lxml import etree

from fastapi import APIRouter, Body

from utils.responses import ok

router = APIRouter(prefix="/api/v1/imports", tags=["Imports"])


@router.post("/sitemap")
def import_sitemap(xml: str = Body(..., embed=True)):
    """Parse a sitemap.xml uploaded by the migration tool and return the URLs found."""
    root = etree.fromstring(xml.encode("utf-8"))
    urls = [loc.text for loc in root.iter() if loc.tag.endswith("loc") and loc.text]
    return ok({"count": len(urls), "urls": urls})
