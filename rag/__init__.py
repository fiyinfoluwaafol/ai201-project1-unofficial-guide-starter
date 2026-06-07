"""RAG helpers for the ProPresenter unofficial guide."""

from .chunking import chunk_documents
from .ingestion import load_documents

__all__ = ["build_index", "chunk_documents", "load_documents", "retrieve_chunks"]


def __getattr__(name: str):
    if name == "build_index":
        from .retrieval import build_index

        return build_index
    if name == "retrieve_chunks":
        from .retrieval import retrieve_chunks

        return retrieve_chunks
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
