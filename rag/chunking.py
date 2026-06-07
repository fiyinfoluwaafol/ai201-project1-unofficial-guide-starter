"""Chunk parsed Markdown documents for retrieval."""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any


TARGET_TOKENS = 650
MAX_TOKENS = 950
OVERLAP_TOKENS = 100
TRANSCRIPT_TARGET_WORDS = 425
TRANSCRIPT_MAX_WORDS = 525

WORD_RE = re.compile(r"\b[\w'-]+\b")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TIMESTAMP_LINE_RE = re.compile(r"^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*$")
SOFT_HEADING_RE = re.compile(r"^\*\*([^*\n]{3,100})\*\*\s*$")


def chunk_documents(documents: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Chunk all parsed document records."""
    chunks: list[dict[str, Any]] = []

    for document in documents:
        if _is_transcript(document):
            document_chunks = _chunk_transcript(document)
        else:
            document_chunks = _chunk_official_doc(document)
        chunks.extend(document_chunks)

    return chunks


def _chunk_official_doc(document: dict[str, Any]) -> list[dict[str, Any]]:
    sections = _split_markdown_sections(document["body"], document["title"])
    chunks: list[dict[str, Any]] = []

    for section in sections:
        if not section["blocks"]:
            continue

        text = "\n\n".join(section["blocks"]).strip()
        if not text:
            continue

        if estimate_token_count(text) <= MAX_TOKENS:
            chunks.append(_make_chunk(document, chunks, section["heading_path"], text))
            continue

        for part in _split_oversized_blocks(section["blocks"]):
            chunks.append(_make_chunk(document, chunks, section["heading_path"], part))

    return chunks


def _split_markdown_sections(body: str, fallback_title: str) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    heading_stack: list[tuple[int, str]] = []
    current_blocks: list[str] = []
    current_heading_path: list[str] = [fallback_title]

    for block in _iter_markdown_blocks(body):
        heading = _parse_heading(block)
        soft_heading = _parse_soft_heading(block)

        if heading or soft_heading:
            if current_blocks:
                sections.append(
                    {"heading_path": current_heading_path, "blocks": current_blocks}
                )
                current_blocks = []

            if heading:
                level, title = heading
                heading_stack = [(l, t) for l, t in heading_stack if l < level]
                heading_stack.append((level, title))
            else:
                level, title = 2, soft_heading or fallback_title
                heading_stack = [(l, t) for l, t in heading_stack if l < level]
                heading_stack.append((level, title))

            current_heading_path = [title for _, title in heading_stack]
            if not current_heading_path:
                current_heading_path = [fallback_title]
            continue

        current_blocks.append(block)

    if current_blocks:
        sections.append({"heading_path": current_heading_path, "blocks": current_blocks})

    return sections


def _iter_markdown_blocks(body: str) -> Iterable[str]:
    lines = body.splitlines()
    block: list[str] = []
    block_kind: str | None = None

    for line in lines:
        stripped = line.strip()
        is_table_line = stripped.startswith("|")
        is_list_line = _is_list_line(line)

        if not stripped:
            if block:
                yield "\n".join(block).strip()
                block = []
            block_kind = None
            continue

        if _parse_heading(line):
            next_kind = "heading"
        elif _parse_soft_heading(line):
            next_kind = "soft_heading"
        elif is_table_line:
            next_kind = "table"
        elif is_list_line:
            next_kind = "list"
        else:
            next_kind = "paragraph"

        if block and next_kind != block_kind:
            yield "\n".join(block).strip()
            block = []

        block.append(line)
        block_kind = next_kind

    if block:
        yield "\n".join(block).strip()


def _split_oversized_blocks(blocks: list[str]) -> list[str]:
    parts: list[str] = []
    current: list[str] = []

    for block in blocks:
        candidate = "\n\n".join([*current, block]).strip()
        if current and estimate_token_count(candidate) > TARGET_TOKENS:
            parts.append("\n\n".join(current).strip())
            current = _overlap_blocks(current)
        current.append(block)

    if current:
        parts.append("\n\n".join(current).strip())

    return [part for part in parts if part]


def _overlap_blocks(blocks: list[str]) -> list[str]:
    overlap: list[str] = []
    token_total = 0

    for block in reversed(blocks):
        block_tokens = estimate_token_count(block)
        if overlap and token_total + block_tokens > OVERLAP_TOKENS:
            break
        overlap.insert(0, block)
        token_total += block_tokens

    return overlap


def _chunk_transcript(document: dict[str, Any]) -> list[dict[str, Any]]:
    entries = _parse_transcript_entries(document["body"])
    chunks: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    current_words = 0

    for entry in entries:
        entry_words = count_words(entry["text"])
        candidate_words = current_words + entry_words
        if (
            current
            and current_words >= TRANSCRIPT_TARGET_WORDS
            and candidate_words > TRANSCRIPT_MAX_WORDS
        ):
            chunks.append(_make_transcript_chunk(document, chunks, current))
            current = []
            current_words = 0

        current.append(entry)
        current_words += entry_words

        if current_words >= TRANSCRIPT_MAX_WORDS:
            chunks.append(_make_transcript_chunk(document, chunks, current))
            current = []
            current_words = 0

    if current:
        chunks.append(_make_transcript_chunk(document, chunks, current))

    return chunks


def _parse_transcript_entries(body: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    current_timestamp: str | None = None
    current_lines: list[str] = []

    for line in body.splitlines():
        timestamp_match = TIMESTAMP_LINE_RE.match(line.strip())
        if timestamp_match:
            if current_timestamp and current_lines:
                entries.append(
                    {
                        "timestamp": current_timestamp,
                        "seconds": timestamp_to_seconds(current_timestamp),
                        "text": "\n".join(current_lines).strip(),
                    }
                )
            current_timestamp = timestamp_match.group(1)
            current_lines = []
            continue

        if current_timestamp and line.strip():
            current_lines.append(line.strip())

    if current_timestamp and current_lines:
        entries.append(
            {
                "timestamp": current_timestamp,
                "seconds": timestamp_to_seconds(current_timestamp),
                "text": "\n".join(current_lines).strip(),
            }
        )

    return entries


def _make_transcript_chunk(
    document: dict[str, Any], existing_chunks: list[dict[str, Any]], entries: list[dict[str, Any]]
) -> dict[str, Any]:
    start = entries[0]
    end = entries[-1]
    text = "\n\n".join(f"[{entry['timestamp']}]\n{entry['text']}" for entry in entries)
    chunk = _make_chunk(
        document,
        existing_chunks,
        [document["title"], "Transcript"],
        text,
        start_timestamp=start["timestamp"],
        end_timestamp=end["timestamp"],
        start_seconds=start["seconds"],
        end_seconds=end["seconds"],
    )
    return chunk


def _make_chunk(
    document: dict[str, Any],
    existing_chunks: list[dict[str, Any]],
    heading_path: list[str],
    text: str,
    start_timestamp: str | None = None,
    end_timestamp: str | None = None,
    start_seconds: int | None = None,
    end_seconds: int | None = None,
) -> dict[str, Any]:
    chunk_index = len(existing_chunks)
    normalized_heading_path = _dedupe_heading_path(heading_path or [document["title"]])
    source_slug = _source_slug(document["source_file"])

    return {
        "chunk_id": f"{source_slug}__{chunk_index:03d}",
        "source_file": document["source_file"],
        "source_url": document["source_url"],
        "title": document["title"],
        "document_type": document["document_type"],
        "product": document["product"],
        "heading_path": normalized_heading_path,
        "section_title": normalized_heading_path[-1] if normalized_heading_path else "",
        "chunk_index": chunk_index,
        "text": text.strip(),
        "token_count": estimate_token_count(text),
        "word_count": count_words(text),
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp,
        "start_seconds": start_seconds,
        "end_seconds": end_seconds,
    }


def _parse_heading(block: str) -> tuple[int, str] | None:
    if "\n" in block:
        return None
    match = HEADING_RE.match(block.strip())
    if not match:
        return None

    title = match.group(2).strip()
    if not title:
        return None
    return len(match.group(1)), title


def _parse_soft_heading(block: str) -> str | None:
    if "\n" in block:
        return None

    stripped = block.strip()
    match = SOFT_HEADING_RE.match(stripped)
    if not match:
        return None

    title = match.group(1).strip()
    if not title or title.startswith("![") or "](" in title:
        return None
    if len(title.split()) > 12:
        return None
    if title.endswith("."):
        return None
    return title.rstrip(":")


def _is_list_line(line: str) -> bool:
    return bool(re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", line))


def _is_transcript(document: dict[str, Any]) -> bool:
    if document.get("document_type") == "youtube_transcript":
        return True
    timestamp_count = sum(
        1 for line in document.get("body", "").splitlines() if TIMESTAMP_LINE_RE.match(line.strip())
    )
    return timestamp_count >= 3


def _source_slug(source_file: str) -> str:
    slug = source_file.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", slug).strip("-")


def _dedupe_heading_path(heading_path: list[str]) -> list[str]:
    deduped: list[str] = []
    for heading in heading_path:
        if heading and (not deduped or heading != deduped[-1]):
            deduped.append(heading)
    return deduped


def timestamp_to_seconds(timestamp: str) -> int:
    parts = [int(part) for part in timestamp.split(":")]
    if len(parts) == 2:
        minutes, seconds = parts
        return minutes * 60 + seconds
    hours, minutes, seconds = parts
    return hours * 3600 + minutes * 60 + seconds


def estimate_token_count(text: str) -> int:
    return max(1, round(count_words(text) * 1.3))


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))
