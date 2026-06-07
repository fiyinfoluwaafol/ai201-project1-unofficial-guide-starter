"""Load Markdown source documents and normalize their metadata."""

from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCUMENTS_DIR = ROOT / "documents"


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Parse simple YAML-style front matter from a Markdown document."""
    if not text.startswith("---\n"):
        return {}, text

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text

    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata, parts[2].lstrip()


def load_documents(documents_dir: Path | str = DEFAULT_DOCUMENTS_DIR) -> list[dict[str, Any]]:
    """Load all Markdown files from documents_dir as normalized document records."""
    documents_path = Path(documents_dir)
    records: list[dict[str, Any]] = []

    for path in sorted(documents_path.glob("*.md")):
        if path.name == ".gitkeep":
            continue

        text = path.read_text(encoding="utf-8")
        metadata, body = parse_front_matter(text)
        try:
            relative_path = path.relative_to(ROOT).as_posix()
        except ValueError:
            relative_path = path.as_posix()

        records.append(
            {
                "source_file": relative_path,
                "source_url": metadata.get("source", ""),
                "title": metadata.get("title") or _first_heading(body) or path.stem,
                "document_type": metadata.get("type", "unknown"),
                "product": metadata.get("product", ""),
                "body": body.strip(),
                "metadata": metadata,
            }
        )

    return records


def _first_heading(body: str) -> str | None:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or None
    return None
