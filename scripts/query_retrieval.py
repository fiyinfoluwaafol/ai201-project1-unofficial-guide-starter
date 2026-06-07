#!/usr/bin/env python3
"""Inspect retrieved chunks for a user query."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rag.retrieval import (  # noqa: E402
    DEFAULT_CHROMA_DIR,
    DEFAULT_COLLECTION_NAME,
    DEFAULT_MODEL_NAME,
    DEFAULT_TOP_K,
    retrieve_chunks,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="User query to retrieve context for.")
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help="Number of chunks to retrieve.",
    )
    parser.add_argument(
        "--persist-dir",
        default=str(DEFAULT_CHROMA_DIR),
        help="Directory containing the persisted ChromaDB vector index.",
    )
    parser.add_argument(
        "--collection",
        default=DEFAULT_COLLECTION_NAME,
        help="ChromaDB collection name.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL_NAME,
        help="sentence-transformers model name.",
    )
    parser.add_argument(
        "--preview-chars",
        type=int,
        default=450,
        help="Number of chunk text characters to show for each result.",
    )
    args = parser.parse_args()

    results = retrieve_chunks(
        query=args.query,
        top_k=args.top_k,
        persist_dir=Path(args.persist_dir),
        collection_name=args.collection,
        model_name=args.model,
    )

    print(f"Query: {args.query}")
    print(f"Results: {len(results)}")
    print()

    for index, result in enumerate(results, start=1):
        heading = " > ".join(result["heading_path"])
        preview = _preview(result["text"], args.preview_chars)
        print(f"{index}. score={result['score']:.4f} distance={result['distance']:.4f}")
        print(f"   id: {result['chunk_id']}")
        print(f"   title: {result['title']}")
        print(f"   heading: {heading}")
        print(f"   source: {result['source_file']} #{result['chunk_index']}")
        print(f"   url: {result['source_url']}")
        if result.get("start_timestamp") and result.get("end_timestamp"):
            print(f"   timestamp: {result['start_timestamp']}-{result['end_timestamp']}")
        print(f"   preview: {preview}")
        print()


def _preview(text: str, max_chars: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max(0, max_chars - 3)].rstrip() + "..."


if __name__ == "__main__":
    main()
