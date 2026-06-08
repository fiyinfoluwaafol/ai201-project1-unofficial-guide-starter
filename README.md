# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How do I open the Stage Layout editor in ProPresenter, and what shortcut can I use on Mac and Windows? | Open the Stage Layout editor from `Screens > Edit Layouts`. The shortcut is `Command+4` on Mac or `Control+4` on Windows. | To open the Stage Layout editor, select `Screens > Edit Layouts` from the menu bar or use the keyboard shortcut. The shortcut is `cmd+4` on Mac and `ctrl+4` on Windows. The response also noted that the editor lets you edit and customize Stage Screen layouts. | Relevant | Accurate |
| 2 | If my lower-thirds lyrics look different from the main auditorium lyrics, where should I check first? | Check the Looks window, especially the alternate theme selected for the Presentation layer on the lower-thirds screen. If lyrics are unexpectedly different, make sure an alternate theme is not applied next to `Presentation` for that screen. | Check the Looks window first and make sure an alternate theme is not applied next to `Presentation`. The response explained that the alternate theme can determine how text on the `Lower Thirds` screen appears differently from the `Main Screen` lyrics. | Relevant | Accurate |
| 3 | Why should I start a timer from a Header or from Timers instead of with a slide action in a looping announcement presentation? | Starting the timer from a Header or from Timers prevents the clock from resetting every time the looping slide is selected. Slide timer actions fire each time the slide is selected, so they are not recommended for an active slide in a looping presentation. | Starting a timer with a slide action causes the timer to reset every time the slide is selected, especially in an announcement loop. Starting it from a Header or from Timers prevents the clock from resetting every time. | Relevant | Accurate |
| 4 | What does the `Break on New Verse` Bible slide option do, and when is `Verse References` available? | `Break on New Verse` creates new slides for each verse in a passage. `Verse References` is only available when `Break on New Verse` is selected. | `Break on New Verse` creates new slides for each verse of a passage. `Verse References` is available when `Break on New Verse` is selected and displays the verse reference on each slide. | Relevant | Accurate |
| 5 | In the Audio Routing window, what do the `M`, `S`, and `T` buttons do? | `M` mutes a channel, `S` solos a channel, and `T` sends a tone to that channel. These can be used for troubleshooting audio signals. | In the Audio Routing window, `M` mutes a channel, `S` solos a channel, and `T` sends a tone to a channel. The response also said these functions can be used to troubleshoot audio signals. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

Do macros get saved in playlist templates?

**What the system returned:**

The system said the provided ProPresenter documents do not contain enough information to answer whether macros get saved in playlist templates. It retrieved chunks from the Playlist Templates article and the general UI article, but it did not retrieve the dedicated `Using Macros in ProPresenter` document.

**Root cause (tied to a specific pipeline stage):**

This was a retrieval-stage failure. The query asks about the relationship between two concepts: macros and playlist templates. The dense retriever focused heavily on the "playlist templates" part of the question and returned several chunks from the playlist template document, but it failed to retrieve the macro document even though "macros" appeared directly in the query and there is a source dedicated to macros. Because the macro context was missing from the top 5 retrieved chunks, the generator could only say that the retrieved documents did not contain enough information.

There is also a source coverage issue: the playlist template document explains that templates save service structure such as headers, placeholders, and presentations, while the macro document explains creating, triggering, and organizing macros. Neither source clearly states whether macros are included or excluded when saving a playlist template.

**What you would change to fix it:**

I would improve retrieval for multi-concept questions by adding hybrid search or keyword boosting, so exact terms like `macro`, `macros`, and `playlist template` are guaranteed to influence the top results. I would also consider query decomposition: retrieve chunks separately for `macros` and for `playlist templates`, then combine and rerank the results before generation. Finally, I would add or create a source that explicitly documents what playlist templates save and do not save, because the current corpus does not directly answer this cross-feature question.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

Writing `planning.md` first helped me think through how I wanted the system to be built before starting the actual pipeline code. It forced me to make design decisions early, including the domain, document sources, chunking strategy, retrieval approach, generation model, and evaluation questions. That made the implementation smoother because the AI tool had a clear blueprint to follow instead of needing to infer the system design from scratch.

The spec was especially helpful because I built the pipeline one stage at a time across different Codex chat sessions. Since `planning.md` captured the intended behavior for each stage, I could give the relevant section to Codex as context and get implementation help that stayed aligned with the project. This meant there were fewer major corrections needed because the requirements were already written down in a concrete way.

**One way your implementation diverged from the spec, and why:**

One place where the implementation diverged slightly from the spec was the initial chunking implementation. The plan called for heading-aware chunks that preserved focused sections of each document, but some of the first chunks were still a little too broad and combined more information than I wanted. Once I noticed that, I intervened and steered Codex toward a more refined chunking approach so the chunks better matched the structure described in `planning.md`.

This divergence happened because the source documents were not all structured the same way. Some documents had clear Markdown headings, while others used bold labels or longer sections that needed extra handling. Adjusting the chunking logic after inspecting the output helped the final implementation better match the original intent of the spec.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I gave Codex the Domain, Documents, and Chunking Strategy sections from `planning.md`, along with the local `documents/` folder. I asked it to help implement the ingestion and chunking stage for a ProPresenter guide, including preserving front matter metadata, source URLs, document titles, heading paths, and chunk indexes.
- *What it produced:* Codex produced the ingestion and chunking modules that load the Markdown files, parse their metadata, and split the documents into structured chunks. It also helped create inspection scripts so I could check the number of chunks, the size of each chunk, and whether the heading paths were being preserved correctly.
- *What I changed or overrode:* The first chunking approach produced some chunks that were too broad, especially in documents that used bold labels instead of normal Markdown headings. After inspecting the chunk output, I steered Codex to treat short standalone bold labels as soft section headings and to keep chunks more focused around specific ProPresenter workflows.

**Instance 2**

- *What I gave the AI:* I gave Codex the Retrieval Approach, Architecture, and Evaluation Plan sections from `planning.md`. I asked it to implement the embedding, ChromaDB storage, retrieval, and grounded generation stages using `all-MiniLM-L6-v2` for embeddings and Groq's `llama-3.3-70b-versatile` model for answer generation.
- *What it produced:* Codex produced the indexing script, retrieval helpers, generation function, and CLI script for asking questions against the indexed ProPresenter documents. It also helped format retrieved chunks with source titles, URLs, heading paths, scores, and `[Source N]` markers so generated answers could cite the context they used.
- *What I changed or overrode:* I tested the five evaluation questions from `planning.md` myself through the CLI and recorded the actual responses in the README instead of assuming the system worked. I also added a failure case after testing the question "Do macros get saved in playlist templates?" because it revealed that dense retrieval focused on playlist template chunks and missed the dedicated macro document.
