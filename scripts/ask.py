#!/usr/bin/env python3
"""Ask grounded ProPresenter questions from the command line."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rag.generation import (  # noqa: E402
    DEFAULT_GENERATION_MODEL,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    generate_answer,
)
from rag.retrieval import (  # noqa: E402
    DEFAULT_CHROMA_DIR,
    DEFAULT_COLLECTION_NAME,
    DEFAULT_MODEL_NAME,
    DEFAULT_TOP_K,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "query",
        nargs="?",
        help="Question to ask. Omit this to start interactive mode.",
    )
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
        "--retrieval-model",
        default=DEFAULT_MODEL_NAME,
        help="sentence-transformers model name for retrieval.",
    )
    parser.add_argument(
        "--generation-model",
        default=DEFAULT_GENERATION_MODEL,
        help="Groq chat model for grounded generation.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help="Groq generation temperature.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help="Maximum answer tokens to request from Groq.",
    )
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Show retrieved chunk previews after the source list.",
    )
    args = parser.parse_args()

    if args.query:
        return _ask_once(args.query, args)

    return _interactive(args)


def _interactive(args: argparse.Namespace) -> int:
    print("ProPresenter guide CLI. Type 'exit' or 'quit' to stop.")
    while True:
        try:
            query = input("\nQuestion: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if query.lower() in {"exit", "quit"}:
            return 0
        if not query:
            print("Please enter a question.")
            continue

        status = _ask_once(query, args)
        if status != 0:
            return status


def _ask_once(query: str, args: argparse.Namespace) -> int:
    try:
        result = generate_answer(
            query,
            top_k=args.top_k,
            persist_dir=Path(args.persist_dir),
            collection_name=args.collection,
            retrieval_model=args.retrieval_model,
            generation_model=args.generation_model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
    except ValueError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - CLI should convert failures to readable output.
        print(f"Generation failed: {exc}", file=sys.stderr)
        return 1

    print()
    print(result["answer"])
    _print_sources(result.get("sources", []))
    if args.show_context:
        _print_context_previews(result.get("retrieved_chunks", []))
    return 0


def _print_sources(sources: list[dict[str, Any]]) -> None:
    if not sources:
        print("\nSources: none")
        return

    print("\nSources:")
    for source in sources:
        heading = _format_heading_path(source.get("heading_path"))
        print(
            f"[Source {source['source_number']}] "
            f"score={float(source.get('score', 0.0)):.4f} "
            f"{source.get('title', '')}"
        )
        if heading:
            print(f"  heading: {heading}")
        print(f"  source: {source.get('source_file', '')} #{source.get('chunk_index', '')}")
        if source.get("url"):
            print(f"  url: {source['url']}")


def _print_context_previews(chunks: list[dict[str, Any]]) -> None:
    if not chunks:
        return

    print("\nRetrieved context:")
    for index, chunk in enumerate(chunks, start=1):
        preview = _preview(str(chunk.get("text", "")), max_chars=500)
        print(f"[Source {index}] {preview}")


def _preview(text: str, max_chars: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max(0, max_chars - 3)].rstrip() + "..."


def _format_heading_path(value: Any) -> str:
    if isinstance(value, list):
        return " > ".join(str(item) for item in value if item)
    return str(value or "")


if __name__ == "__main__":
    raise SystemExit(main())
