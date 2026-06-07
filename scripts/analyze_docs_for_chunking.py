#!/usr/bin/env python3
"""Print lightweight Markdown corpus stats for chunking decisions."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = ROOT / "documents"

WORD_RE = re.compile(r"\b[\w'-]+\b")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TIMESTAMP_RE = re.compile(r"^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*$")
BOLD_HEADING_RE = re.compile(r"^\*\*([^*\n]{3,100})\*\*\s*$")


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
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
        metadata[key.strip()] = value.strip().strip('"')
    return metadata, parts[2]


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def section_word_counts(body: str) -> list[tuple[str, int]]:
    sections: list[tuple[str, list[str]]] = []
    current_heading = "(intro)"
    current_lines: list[str] = []

    for line in body.splitlines():
        heading_match = HEADING_RE.match(line)
        bold_match = BOLD_HEADING_RE.match(line)
        if heading_match or bold_match:
            if current_lines:
                sections.append((current_heading, current_lines))
            current_heading = (
                heading_match.group(2).strip()
                if heading_match
                else bold_match.group(1).strip()
            )
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_heading, current_lines))

    return [
        (heading, count_words("\n".join(lines)))
        for heading, lines in sections
        if count_words("\n".join(lines)) > 0
    ]


def main() -> None:
    files = sorted(DOCUMENTS_DIR.glob("*.md"))
    print(f"Markdown files: {len(files)}")
    print()
    print(
        "| File | Type | Words | # headings | Bold headings | Tables | Lists | Timestamps | Looks transcript? |"
    )
    print("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |")

    largest_sections: list[tuple[int, str, str]] = []

    for path in files:
        text = path.read_text(encoding="utf-8")
        metadata, body = parse_front_matter(text)
        lines = body.splitlines()
        headings = [line for line in lines if HEADING_RE.match(line)]
        bold_headings = [line for line in lines if BOLD_HEADING_RE.match(line)]
        table_lines = [line for line in lines if line.strip().startswith("|")]
        list_lines = [
            line
            for line in lines
            if re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", line)
        ]
        timestamp_lines = [line for line in lines if TIMESTAMP_RE.match(line.strip())]
        looks_transcript = (
            metadata.get("type") == "youtube_transcript" or len(timestamp_lines) >= 3
        )

        for heading, words in section_word_counts(body):
            largest_sections.append((words, path.name, heading))

        print(
            "| {file} | {type} | {words} | {headings} | {bold} | {tables} | {lists} | {timestamps} | {transcript} |".format(
                file=path.name,
                type=metadata.get("type", "unknown"),
                words=count_words(body),
                headings=len(headings),
                bold=len(bold_headings),
                tables=len(table_lines),
                lists=len(list_lines),
                timestamps=len(timestamp_lines),
                transcript="yes" if looks_transcript else "no",
            )
        )

    print()
    print("Largest heading/bold-heading sections:")
    for words, file_name, heading in sorted(largest_sections, reverse=True)[:10]:
        print(f"- {words:>5} words | {file_name} | {heading}")


if __name__ == "__main__":
    main()
