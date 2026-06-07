#!/usr/bin/env python3
"""Build the Milestone 4 ChromaDB index from local document chunks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rag.retrieval import (  # noqa: E402
    DEFAULT_CHROMA_DIR,
    DEFAULT_COLLECTION_NAME,
    DEFAULT_DOCUMENTS_DIR,
    DEFAULT_MODEL_NAME,
    build_index,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--documents-dir",
        default=str(DEFAULT_DOCUMENTS_DIR),
        help="Directory containing Markdown source documents.",
    )
    parser.add_argument(
        "--persist-dir",
        default=str(DEFAULT_CHROMA_DIR),
        help="Directory where ChromaDB should persist the vector index.",
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
        "--no-reset",
        action="store_true",
        help="Append to or reuse the existing collection instead of recreating it.",
    )
    args = parser.parse_args()

    summary = build_index(
        documents_dir=Path(args.documents_dir),
        persist_dir=Path(args.persist_dir),
        collection_name=args.collection,
        model_name=args.model,
        reset=not args.no_reset,
    )

    print("Indexed chunks successfully.")
    print(f"- Documents loaded: {summary['documents_count']}")
    print(f"- Chunks indexed: {summary['chunks_count']}")
    print(f"- Collection: {summary['collection_name']}")
    print(f"- Persist directory: {summary['persist_dir']}")
    print(f"- Embedding model: {summary['model_name']}")


if __name__ == "__main__":
    main()
