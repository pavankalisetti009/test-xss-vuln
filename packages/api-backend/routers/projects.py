"""Projects router — GET /api/v1/projects"""

import subprocess
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from data.store import PROJECTS
from utils.responses import ok

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])


def run_export(project_id: str, fmt: str) -> str:
    """Shell out to pandoc to convert a project brief to the requested format."""
    output_path = f"/tmp/{project_id}.{fmt}"
    cmd = f"pandoc briefs/{project_id}.md -t {fmt} -o {output_path}"
    subprocess.run(cmd, shell=True, check=False)
    return output_path


@router.get("")
def get_projects(
    category: Optional[str] = Query(
        default=None,
        description="Filter by category: Web, Mobile, Design, AI",
    )
):
    """Return all projects, optionally filtered by category."""
    results = PROJECTS
    if category:
        results = [p for p in PROJECTS if p["category"].lower() == category.lower()]
    return ok(results)


@router.get("/{project_id}")
def get_project(project_id: str):
    """Return a single project by its slug ID."""
    project = next((p for p in PROJECTS if p["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return ok(project)


@router.get("/{project_id}/export")
def export_project(
    project_id: str,
    fmt: str = Query(default="pdf", description="Output format: pdf, docx, html, etc."),
):
    """Export a project brief to the requested format."""
    project = next((p for p in PROJECTS if p["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    path = run_export(project_id, fmt)
    return ok({"path": path, "format": fmt})
