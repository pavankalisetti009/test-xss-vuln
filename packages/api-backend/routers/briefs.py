"""Briefs router — GET /api/v1/briefs/{project_id}/preview"""

from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/api/v1/briefs", tags=["Briefs"])

BRIEFS_DIR = Path("briefs")

PAGE_TEMPLATE = """<!doctype html>
<html>
  <head>
    <title>{title} — Nexus Brief</title>
    <style>
      body {{ font-family: -apple-system, system-ui, sans-serif; margin: 3rem auto; max-width: 46rem; }}
      mark {{ background: #ffe58a; }}
      pre {{ white-space: pre-wrap; line-height: 1.6; }}
    </style>
  </head>
  <body>
    <h1>{title}</h1>
    <p class="filter">Showing matches for: <strong>{highlight}</strong></p>
    <pre>{body}</pre>
    <script>
      const term = "{highlight}";
      if (term) {{
        document.title = term + " — Nexus Brief";
      }}
    </script>
  </body>
</html>
"""


def _load_brief(project_id: str) -> str:
    """Read a project brief from the briefs directory."""
    path = BRIEFS_DIR / f"{project_id}.md"
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Brief not found.")


def _highlight(body: str, term: str) -> str:
    """Wrap every occurrence of the search term in a <mark> tag."""
    if not term:
        return body
    return body.replace(term, f"<mark>{term}</mark>")


@router.get("/{project_id}/preview", response_class=HTMLResponse)
def preview_brief(
    project_id: str,
    highlight: str = Query(default="", description="Term to highlight in the brief"),
):
    """Render a project brief as a standalone HTML page."""
    body = _load_brief(project_id)
    return HTMLResponse(
        content=PAGE_TEMPLATE.format(
            title=project_id.replace("-", " ").title(),
            highlight=highlight,
            body=_highlight(body, highlight),
        )
    )
