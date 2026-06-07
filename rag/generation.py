"""Grounded answer generation for the ProPresenter guide."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from .retrieval import (
    DEFAULT_CHROMA_DIR,
    DEFAULT_COLLECTION_NAME,
    DEFAULT_MODEL_NAME,
    DEFAULT_TOP_K,
    retrieve_chunks,
)


DEFAULT_GENERATION_MODEL = "llama-3.3-70b-versatile"
DEFAULT_TEMPERATURE = 0.1
DEFAULT_MAX_TOKENS = 700

SYSTEM_PROMPT = """You are a ProPresenter support assistant for an unofficial guide.

Grounding rules:
- Answer only from the retrieved ProPresenter context provided by the user message.
- If the context does not contain enough information, say that the provided ProPresenter documents do not contain enough information to answer.
- If the question is vague, ask one concise clarifying question and, only if useful, mention the documented areas that may be relevant.
- Do not use general product knowledge, assumptions, or unrelated advice.
- Include source attribution with [Source N] markers for every factual claim that comes from the context.
- Keep answers practical and concise."""


def generate_answer(
    question: str,
    top_k: int = DEFAULT_TOP_K,
    persist_dir: Path | str = DEFAULT_CHROMA_DIR,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    retrieval_model: str = DEFAULT_MODEL_NAME,
    generation_model: str = DEFAULT_GENERATION_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> dict[str, Any]:
    """Retrieve context for a question and generate a grounded answer with Groq."""
    normalized_question = question.strip()
    if not normalized_question:
        raise ValueError("question must not be empty")

    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not set. Add it to .env before generating answers.")

    chunks = retrieve_chunks(
        normalized_question,
        top_k=top_k,
        persist_dir=persist_dir,
        collection_name=collection_name,
        model_name=retrieval_model,
    )
    context = format_retrieved_context(chunks)
    user_prompt = _build_user_prompt(normalized_question, context)

    client = Groq()
    completion = client.chat.completions.create(
        model=generation_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    answer = completion.choices[0].message.content or ""
    return {
        "answer": answer.strip(),
        "sources": build_sources(chunks),
        "retrieved_chunks": chunks,
    }


def format_retrieved_context(chunks: list[dict[str, Any]]) -> str:
    """Format retrieved chunks for the grounded generation prompt."""
    if not chunks:
        return "No retrieved ProPresenter context was available."

    formatted_sources = []
    for index, chunk in enumerate(chunks, start=1):
        heading = _format_heading_path(chunk.get("heading_path"))
        formatted_sources.append(
            "\n".join(
                [
                    f"Source {index}:",
                    f"Title: {chunk.get('title', '')}",
                    f"URL: {chunk.get('source_url', '')}",
                    f"Heading: {heading}",
                    f"Source file: {chunk.get('source_file', '')}",
                    f"Chunk index: {chunk.get('chunk_index', '')}",
                    f"Retrieval score: {float(chunk.get('score', 0.0)):.4f}",
                    "Content:",
                    str(chunk.get("text", "")).strip(),
                ]
            ).strip()
        )

    return "\n\n---\n\n".join(formatted_sources)


def build_sources(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return source metadata in the same order used by the generation prompt."""
    sources = []
    for index, chunk in enumerate(chunks, start=1):
        sources.append(
            {
                "source_number": index,
                "title": chunk.get("title", ""),
                "url": chunk.get("source_url", ""),
                "heading_path": chunk.get("heading_path", []),
                "source_file": chunk.get("source_file", ""),
                "chunk_index": chunk.get("chunk_index", 0),
                "score": chunk.get("score", 0.0),
            }
        )
    return sources


def _build_user_prompt(question: str, context: str) -> str:
    return f"""User question:
{question}

Retrieved ProPresenter context:
{context}

Answer the user question using only the retrieved context. Include [Source N] markers."""


def _format_heading_path(value: Any) -> str:
    if isinstance(value, list):
        return " > ".join(str(item) for item in value if item)
    return str(value or "")
