"""Gradio UI for the ProPresenter unofficial guide."""

from __future__ import annotations

import html
from typing import Any, Generator

import gradio as gr

from rag.generation import generate_answer


EXAMPLE_QUESTIONS = [
    "How do I open the Stage Layout editor in ProPresenter, and what shortcut can I use on Mac and Windows?",
    "If my lower-thirds lyrics look different from the main auditorium lyrics, where should I check first?",
    "In the Audio Routing window, what do the M, S, and T buttons do?",
]

EMPTY_SOURCES = "Sources will appear here after you ask a question."
EMPTY_CONTEXT = "Retrieved chunk previews will appear here when available."
READY_STATUS = "Ready."
LOADING_STATUS = "Searching the guide and generating an answer..."

CSS = """
:root {
    --container-width: 920px;
    --app-bg: #f8fafc;
    --panel-bg: #ffffff;
    --panel-muted: #f1f5f9;
    --text-main: #111827;
    --text-muted: #4b5563;
    --border: #d9e2ec;
    --button-bg: #334155;
    --button-bg-hover: #1f2937;
}

.gradio-container,
.gradio-container main {
    color: var(--text-main) !important;
}

.gradio-container {
    background: var(--app-bg) !important;
}

#app-shell {
    max-width: var(--container-width);
    margin: 0 auto;
    color: var(--text-main);
}

#header {
    margin: 0 0 18px;
}

#header h1 {
    margin-bottom: 6px;
    font-size: 2rem;
    line-height: 1.15;
    color: var(--text-main) !important;
    font-weight: 700;
}

#header p {
    margin: 0;
    color: var(--text-muted) !important;
    font-size: 0.98rem;
}

#app-shell label,
#app-shell .label-wrap,
#app-shell .label-wrap span {
    color: var(--text-main) !important;
    font-weight: 650;
}

#app-shell .block,
#app-shell .form,
#app-shell textarea,
#app-shell input {
    background: var(--panel-bg) !important;
    color: var(--text-main) !important;
    border-color: var(--border) !important;
}

#app-shell textarea::placeholder,
#app-shell input::placeholder {
    color: #6b7280 !important;
    opacity: 1 !important;
}

#app-shell textarea {
    min-height: 112px;
}

#app-shell button {
    border-radius: 6px !important;
}

#app-shell button.primary,
#app-shell button[class*="primary"] {
    background: var(--button-bg) !important;
    border-color: var(--button-bg) !important;
    color: #ffffff !important;
    font-weight: 650;
}

#app-shell button.primary:hover,
#app-shell button[class*="primary"]:hover {
    background: var(--button-bg-hover) !important;
    border-color: var(--button-bg-hover) !important;
}

#app-shell button.secondary,
#app-shell button[class*="secondary"] {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    color: var(--text-main) !important;
    font-weight: 650;
}

#app-shell button.secondary:hover,
#app-shell button[class*="secondary"]:hover {
    background: var(--panel-muted) !important;
}

#app-shell button:disabled {
    background: #94a3b8 !important;
    border-color: #94a3b8 !important;
    color: #f8fafc !important;
}

#answer-box,
#sources-box,
#context-box,
#status-box {
    border-radius: 8px;
    color: var(--text-main) !important;
}

#status-box {
    color: var(--text-muted) !important;
    font-weight: 500;
}

#answer-box p,
#sources-box p,
#context-box p,
#status-box p,
#answer-box li,
#sources-box li,
#context-box li,
#answer-box table,
#sources-box table,
#context-box table {
    color: var(--text-main) !important;
}

#sources-box table {
    background: var(--panel-bg) !important;
}

#sources-box th {
    background: var(--panel-muted) !important;
    color: var(--text-main) !important;
}

#sources-box td,
#sources-box th {
    border-color: var(--border) !important;
}

#sources-box a {
    color: #1d4ed8 !important;
}

#app-shell details,
#app-shell summary {
    background: var(--panel-bg) !important;
    color: var(--text-main) !important;
    border-color: var(--border) !important;
}

#app-shell button.label-wrap {
    background: var(--panel-bg) !important;
    color: var(--text-main) !important;
    border: 1px solid var(--border) !important;
}

#app-shell button.label-wrap span {
    color: var(--text-main) !important;
}

#app-shell details summary {
    font-weight: 650;
}

#app-shell button.gallery-item,
#app-shell button.gallery-item * {
    background: var(--panel-bg) !important;
    color: var(--text-main) !important;
}

#app-shell button.gallery-item {
    border: 1px solid var(--border) !important;
    font-weight: 500;
}

#app-shell button.gallery-item:hover {
    background: var(--panel-muted) !important;
}

.footer-note {
    color: var(--text-muted) !important;
    font-size: 0.88rem;
}
"""

THEME = gr.themes.Soft(
    primary_hue="slate",
    neutral_hue="gray",
    radius_size="sm",
)


def ask_question(
    question: str,
) -> Generator[tuple[str, str, str, str, gr.Button], None, None]:
    """Answer a question and update the UI with loading and final states."""
    normalized_question = question.strip()
    if not normalized_question:
        yield (
            "Please enter a ProPresenter question before asking.",
            EMPTY_SOURCES,
            EMPTY_CONTEXT,
            "Question required.",
            gr.update(interactive=True),
        )
        return

    yield (
        "",
        EMPTY_SOURCES,
        EMPTY_CONTEXT,
        LOADING_STATUS,
        gr.update(interactive=False),
    )

    try:
        result = generate_answer(normalized_question)
    except RuntimeError as exc:
        yield (
            _friendly_runtime_error(str(exc)),
            EMPTY_SOURCES,
            EMPTY_CONTEXT,
            "Could not generate an answer.",
            gr.update(interactive=True),
        )
        return
    except Exception as exc:  # noqa: BLE001 - UI should show readable failures.
        yield (
            f"Generation failed: {exc}",
            EMPTY_SOURCES,
            EMPTY_CONTEXT,
            "Could not generate an answer.",
            gr.update(interactive=True),
        )
        return

    answer = result.get("answer") or "The model did not return an answer."
    sources = _format_sources(result.get("sources", []))
    context = _format_context(result.get("retrieved_chunks", []))
    yield (
        answer,
        sources,
        context,
        READY_STATUS,
        gr.update(interactive=True),
    )


def clear_outputs() -> tuple[str, str, str, str, str, gr.Button]:
    """Reset the question, answer, source, context, and status outputs."""
    return (
        "",
        "",
        EMPTY_SOURCES,
        EMPTY_CONTEXT,
        READY_STATUS,
        gr.update(interactive=True),
    )


def build_demo() -> gr.Blocks:
    """Build the Gradio app."""
    with gr.Blocks(title="ProPresenter Guide") as demo:
        with gr.Column(elem_id="app-shell"):
            gr.Markdown(
                """
                # ProPresenter Guide
                Ask practical questions about screens, looks, lyrics, Bibles, timers, macros, and audio routing.
                """,
                elem_id="header",
            )

            question = gr.Textbox(
                label="Question",
                placeholder=(
                    "Example: How do I open the Stage Layout editor, "
                    "and what shortcut can I use?"
                ),
                lines=4,
                max_lines=8,
                autofocus=True,
            )

            with gr.Row():
                ask_button = gr.Button("Ask", variant="primary")
                clear_button = gr.Button("Clear")

            status = gr.Markdown(READY_STATUS, elem_id="status-box")
            answer = gr.Markdown(
                "Answers will appear here.",
                label="Answer",
                elem_id="answer-box",
            )
            sources = gr.Markdown(
                EMPTY_SOURCES,
                label="Sources",
                elem_id="sources-box",
            )

            with gr.Accordion("Retrieved context", open=False):
                context = gr.Markdown(EMPTY_CONTEXT, elem_id="context-box")

            gr.Examples(
                examples=EXAMPLE_QUESTIONS,
                inputs=question,
                label="Try an example",
            )

            gr.Markdown(
                "<p class='footer-note'>Answers are generated only from the retrieved ProPresenter guide context.</p>"
            )

        ask_event = ask_button.click(
            ask_question,
            inputs=question,
            outputs=[answer, sources, context, status, ask_button],
            show_progress="full",
            show_progress_on=[answer, status],
        )
        question.submit(
            ask_question,
            inputs=question,
            outputs=[answer, sources, context, status, ask_button],
            show_progress="full",
            show_progress_on=[answer, status],
        )
        clear_button.click(
            clear_outputs,
            inputs=None,
            outputs=[question, answer, sources, context, status, ask_button],
            cancels=[ask_event],
            show_progress="hidden",
        )

    return demo.queue(default_concurrency_limit=1)


def _format_sources(sources: list[dict[str, Any]]) -> str:
    if not sources:
        return "No sources were returned."

    lines = [
        "| Source | Score | Title | Heading | URL |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for source in sources:
        number = source.get("source_number", "")
        score = float(source.get("score", 0.0))
        title = _escape_table_cell(str(source.get("title", "")))
        heading = _escape_table_cell(_format_heading_path(source.get("heading_path")))
        url = str(source.get("url", ""))
        url_cell = f"[Open source]({url})" if url else ""
        lines.append(f"| {number} | {score:.4f} | {title} | {heading} | {url_cell} |")

    return "\n".join(lines)


def _format_context(chunks: list[dict[str, Any]]) -> str:
    if not chunks:
        return "No retrieved context was returned."

    sections = []
    for index, chunk in enumerate(chunks, start=1):
        title = str(chunk.get("title", "Untitled source"))
        heading = _format_heading_path(chunk.get("heading_path"))
        preview = _preview(str(chunk.get("text", "")), max_chars=650)
        sections.append(
            "\n".join(
                [
                    f"### Source {index}: {html.escape(title)}",
                    f"**Heading:** {html.escape(heading) if heading else 'None'}",
                    "",
                    html.escape(preview),
                ]
            )
        )

    return "\n\n".join(sections)


def _friendly_runtime_error(message: str) -> str:
    lowered = message.lower()
    if "groq_api_key" in lowered:
        return "GROQ_API_KEY is not set. Add it to `.env` before using the web app."
    if "collection" in lowered and "empty" in lowered:
        return "The local Chroma index is empty. Run `scripts/index_chunks.py` before using the web app."
    return message


def _format_heading_path(value: Any) -> str:
    if isinstance(value, list):
        return " > ".join(str(item) for item in value if item)
    return str(value or "")


def _preview(text: str, max_chars: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max(0, max_chars - 3)].rstrip() + "..."


def _escape_table_cell(value: str) -> str:
    return html.escape(value).replace("|", "\\|")


demo = build_demo()


if __name__ == "__main__":
    demo.launch(theme=THEME, css=CSS)
