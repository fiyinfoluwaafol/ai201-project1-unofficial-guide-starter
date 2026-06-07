#!/usr/bin/env python3
"""Inspect Milestone 3 ingestion and chunking output."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rag import chunk_documents, load_documents


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--documents-dir",
        default=str(ROOT / "documents"),
        help="Directory containing Markdown source documents.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to write chunk records as JSON.",
    )
    args = parser.parse_args()

    documents = load_documents(Path(args.documents_dir))
    chunks = chunk_documents(documents)

    is_valid = print_summary(documents, chunks)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(chunks, indent=2), encoding="utf-8")
        print()
        print(f"Wrote chunks: {output_path}")

    if not is_valid:
        raise SystemExit(1)


def print_summary(documents: list[dict[str, Any]], chunks: list[dict[str, Any]]) -> bool:
    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")
    print()

    print("Chunks by document type:")
    for document_type, count in sorted(Counter(chunk["document_type"] for chunk in chunks).items()):
        print(f"- {document_type}: {count}")
    print()

    print("Per-source summary:")
    chunks_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for chunk in chunks:
        chunks_by_source[chunk["source_file"]].append(chunk)

    for document in documents:
        source_chunks = chunks_by_source[document["source_file"]]
        token_counts = [chunk["token_count"] for chunk in source_chunks]
        max_tokens = max(token_counts) if token_counts else 0
        headings = sorted(
            {
                " > ".join(chunk["heading_path"])
                for chunk in source_chunks
                if chunk.get("heading_path")
            }
        )
        print(
            "- {source} | type={type} | chunks={chunks} | max_tokens={max_tokens} | headings={headings}".format(
                source=document["source_file"],
                type=document["document_type"],
                chunks=len(source_chunks),
                max_tokens=max_tokens,
                headings=len(headings),
            )
        )

    print()
    print("Largest chunks:")
    for chunk in sorted(chunks, key=lambda item: item["token_count"], reverse=True)[:10]:
        heading = " > ".join(chunk["heading_path"])
        print(
            "- {tokens:>4} tokens | {source} | #{index} | {heading}".format(
                tokens=chunk["token_count"],
                source=chunk["source_file"],
                index=chunk["chunk_index"],
                heading=heading,
            )
        )

    transcript_chunks = [
        chunk for chunk in chunks if chunk.get("start_timestamp") and chunk.get("end_timestamp")
    ]
    if transcript_chunks:
        print()
        print("Transcript chunks:")
        for chunk in transcript_chunks:
            print(
                "- {source} | #{index} | {start}-{end} | {words} words".format(
                    source=chunk["source_file"],
                    index=chunk["chunk_index"],
                    start=chunk["start_timestamp"],
                    end=chunk["end_timestamp"],
                    words=chunk["word_count"],
                )
            )

    print()
    print("Validation:")
    return report_validation(chunks)


def report_validation(chunks: list[dict[str, Any]]) -> bool:
    required_fields = ["source_url", "title", "document_type", "text"]
    failures: list[str] = []

    for chunk in chunks:
        for field in required_fields:
            if not chunk.get(field):
                failures.append(f"{chunk.get('chunk_id', '(missing id)')} missing {field}")
        if not chunk.get("heading_path"):
            failures.append(f"{chunk.get('chunk_id', '(missing id)')} missing heading_path")

    if not failures:
        print("- OK: required fields are present and chunks are non-empty.")
        return True

    for failure in failures:
        print(f"- FAIL: {failure}")
    return False


if __name__ == "__main__":
    main()
