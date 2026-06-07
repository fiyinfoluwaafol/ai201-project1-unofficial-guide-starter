"""Embedding, vector storage, and retrieval helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection
from sentence_transformers import SentenceTransformer

from .chunking import chunk_documents
from .ingestion import DEFAULT_DOCUMENTS_DIR, ROOT, load_documents


DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_CHROMA_DIR = ROOT / "chroma_db"
DEFAULT_COLLECTION_NAME = "propresenter_chunks"
DEFAULT_TOP_K = 5


def load_embedding_model(model_name: str = DEFAULT_MODEL_NAME) -> SentenceTransformer:
    """Load the sentence-transformers embedding model."""
    try:
        return SentenceTransformer(model_name, local_files_only=True)
    except OSError:
        return SentenceTransformer(model_name)


def build_embedding_text(chunk: dict[str, Any]) -> str:
    """Build the text that should be embedded for a chunk."""
    heading_path = _format_heading_path(chunk.get("heading_path"))
    return "\n".join(
        [
            f"Title: {chunk.get('title', '')}",
            f"Heading: {heading_path}",
            f"Type: {chunk.get('document_type', '')}",
            f"Source file: {chunk.get('source_file', '')}",
            f"Chunk index: {chunk.get('chunk_index', '')}",
            "",
            str(chunk.get("text", "")).strip(),
        ]
    ).strip()


def build_index(
    documents_dir: Path | str = DEFAULT_DOCUMENTS_DIR,
    persist_dir: Path | str = DEFAULT_CHROMA_DIR,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    model_name: str = DEFAULT_MODEL_NAME,
    reset: bool = True,
) -> dict[str, Any]:
    """Load, chunk, embed, and store all source documents in ChromaDB."""
    documents = load_documents(documents_dir)
    chunks = chunk_documents(documents)
    model = load_embedding_model(model_name)
    collection = get_collection(persist_dir, collection_name, reset=reset)

    ids = [chunk["chunk_id"] for chunk in chunks]
    embedding_texts = [build_embedding_text(chunk) for chunk in chunks]
    embeddings = model.encode(embedding_texts, convert_to_numpy=True).tolist()
    metadatas = [_metadata_for_chroma(chunk) for chunk in chunks]
    documents_text = [chunk["text"] for chunk in chunks]

    if ids:
        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents_text,
            metadatas=metadatas,
        )

    return {
        "documents_count": len(documents),
        "chunks_count": len(chunks),
        "collection_name": collection_name,
        "persist_dir": str(Path(persist_dir)),
        "model_name": model_name,
    }


def get_collection(
    persist_dir: Path | str = DEFAULT_CHROMA_DIR,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    reset: bool = False,
) -> Collection:
    """Return a persistent ChromaDB collection, optionally recreating it."""
    client = chromadb.PersistentClient(path=str(Path(persist_dir)))

    if reset:
        _delete_collection_if_exists(client, collection_name)
        return client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )


def retrieve_chunks(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    persist_dir: Path | str = DEFAULT_CHROMA_DIR,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    model_name: str = DEFAULT_MODEL_NAME,
) -> list[dict[str, Any]]:
    """Retrieve the top matching chunks for a user query."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    model = load_embedding_model(model_name)
    collection = get_collection(persist_dir, collection_name)
    if collection.count() == 0:
        raise RuntimeError(
            f"Chroma collection {collection_name!r} is empty. Run scripts/index_chunks.py first."
        )
    query_embedding = model.encode([query], convert_to_numpy=True).tolist()[0]
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    return _format_query_results(result)


def _metadata_for_chroma(chunk: dict[str, Any]) -> dict[str, str | int | float | bool]:
    metadata: dict[str, str | int | float | bool] = {
        "chunk_id": chunk["chunk_id"],
        "source_file": chunk.get("source_file", ""),
        "source_url": chunk.get("source_url", ""),
        "title": chunk.get("title", ""),
        "document_type": chunk.get("document_type", ""),
        "product": chunk.get("product", ""),
        "heading_path": _format_heading_path(chunk.get("heading_path")),
        "section_title": chunk.get("section_title", ""),
        "chunk_index": int(chunk.get("chunk_index", 0)),
        "token_count": int(chunk.get("token_count", 0)),
        "word_count": int(chunk.get("word_count", 0)),
    }

    optional_fields = [
        "start_timestamp",
        "end_timestamp",
        "start_seconds",
        "end_seconds",
    ]
    for field in optional_fields:
        value = chunk.get(field)
        if value is not None:
            metadata[field] = value

    return metadata


def _format_query_results(result: dict[str, Any]) -> list[dict[str, Any]]:
    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    formatted: list[dict[str, Any]] = []
    for chunk_id, text, metadata, distance in zip(ids, documents, metadatas, distances):
        metadata = metadata or {}
        score = 1 - float(distance)
        formatted.append(
            {
                "chunk_id": metadata.get("chunk_id", chunk_id),
                "score": score,
                "distance": float(distance),
                "title": metadata.get("title", ""),
                "source_url": metadata.get("source_url", ""),
                "source_file": metadata.get("source_file", ""),
                "heading_path": _parse_heading_path(metadata.get("heading_path", "")),
                "section_title": metadata.get("section_title", ""),
                "chunk_index": metadata.get("chunk_index", 0),
                "document_type": metadata.get("document_type", ""),
                "product": metadata.get("product", ""),
                "token_count": metadata.get("token_count", 0),
                "word_count": metadata.get("word_count", 0),
                "start_timestamp": metadata.get("start_timestamp"),
                "end_timestamp": metadata.get("end_timestamp"),
                "start_seconds": metadata.get("start_seconds"),
                "end_seconds": metadata.get("end_seconds"),
                "text": text or "",
            }
        )

    return formatted


def _delete_collection_if_exists(client: chromadb.PersistentClient, collection_name: str) -> None:
    try:
        client.delete_collection(collection_name)
    except Exception as exc:
        message = str(exc).lower()
        if "does not exist" not in message and "not found" not in message:
            raise


def _format_heading_path(value: Any) -> str:
    if isinstance(value, list):
        return " > ".join(str(item) for item in value if item)
    return str(value or "")


def _parse_heading_path(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [part.strip() for part in str(value or "").split(">") if part.strip()]
