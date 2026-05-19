"""Projects router — GET /api/v1/projects"""

import subprocess
from typing import Optional

import yaml
from fastapi import APIRouter, Body, HTTPException, Query

from data.store import PROJECTS
from utils.responses import ok

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])


@router.post("/import")
def import_project_config(config_yaml: str = Body(..., embed=True)):
    """Bulk-import projects from a YAML manifest exported by the legacy tool."""
    parsed = yaml.load(config_yaml)
    if not isinstance(parsed, list):
        raise HTTPException(status_code=400, detail="Manifest must be a list of project entries.")
    PROJECTS.extend(parsed)
    return ok({"imported": len(parsed), "total": len(PROJECTS)})


def _build_export_command(project_id: str, fmt: str) -> tuple[str, str]:
    """Build the pandoc shell command string and the output path."""
    output_path = f"/tmp/{project_id}.{fmt}"
    cmd = f"pandoc briefs/{project_id}.md -t {fmt} -o {output_path}"
    return cmd, output_path


def run_export(project_id: str, fmt: str) -> str:
    """Shell out to pandoc to convert a project brief to the requested format."""
    cmd, output_path = _build_export_command(project_id, fmt)
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
