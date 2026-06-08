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

My system is an unofficial guide for ProPresenter operators in church and media team environments. It focuses on practical questions that volunteers and production team members run into while preparing or running services, including lyrics, scriptures, stage screens, audience screens, Looks, themes, macros, timers, audio routing, and display configuration.

This knowledge is valuable because many church media volunteers need quick, practical answers during rehearsals or Sunday services, but the information is spread across official documentation, tutorial videos, and feature-specific support articles. Official docs are useful, but they are organized by product feature rather than by the kinds of real-world questions a volunteer might ask, such as why lower-thirds lyrics look different from the main screen or why a countdown keeps resetting in an announcement loop.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | ProPresenter- How to Download & Install | YouTube transcript | https://www.youtube.com/watch?v=7awG_JK6eWo |
| 2 | Understanding The ProPresenter User Interface | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/360041345954-Understanding-The-ProPresenter-User-Interface |
| 3 | Keyboard Shortcuts in ProPresenter | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/360042123293-Keyboard-Shortcuts-in-ProPresenter |
| 4 | Using Bibles in ProPresenter | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/360041347594-Using-Bibles-in-ProPresenter |
| 5 | Using a Stage Screen to its Full Potential | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/360041407794-Using-a-Stage-Screen-to-its-Full-Potential |
| 6 | Using Macros in ProPresenter | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/4402663090323-Using-Macros-in-ProPresenter |
| 7 | Using Looks to Show Different Screen Content in ProPresenter | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/360041407174-Using-Looks-to-Show-Different-Screen-Content-in-ProPresenter |
| 8 | Audio Routing in ProPresenter | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/360052696094-Audio-Routing-in-ProPresenter |
| 9 | Audio Outputs in ProPresenter | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/360052697694-Audio-Outputs-in-ProPresenter |
| 10 | Screen Configuration in ProPresenter | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/360041879173-Screen-Configuration-in-ProPresenter |
| 11 | What is the Media Inspector | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/7200487649299-What-is-the-Media-Inspector |
| 12 | Creating and Using Playlist Templates in ProPresenter | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/40377194830995-Creating-and-Using-Playlist-Templates-in-ProPresenter |
| 13 | Guide to Using Themes in ProPresenter | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/34551484745875-Guide-to-Using-Themes-in-ProPresenter |
| 14 | How to Create a Countdown for an Audience Screen | Official Renewed Vision documentation | https://support.renewedvision.com/hc/en-us/articles/360050786794-How-to-Create-a-Countdown-for-an-Audience-Screen |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

The implemented chunker uses a hybrid heading-aware strategy. For official documentation, it first splits Markdown files by real headings such as `#`, `##`, and `###`, then also treats short standalone bold labels like `**Creating a Macro**` as soft headings when they function like section titles. The target chunk size is about 650 tokens, with a maximum of 950 tokens before a section is split further.

For the YouTube transcript source, the chunker groups adjacent timestamped transcript entries instead of using document headings. The transcript target is about 425 words, with a maximum of 525 words, and each transcript chunk preserves start and end timestamps.

**Overlap:**

The system does not apply global overlap to every chunk. Instead, it uses up to 100 tokens of overlap only when an oversized section has to be split into smaller pieces. This keeps normal heading-based chunks clean while still preserving context when a long section is broken apart.

**Why these choices fit your documents:**

The corpus is mostly official Renewed Vision documentation, so the source files already have meaningful article titles, headings, lists, tables, and feature-specific sections. Splitting by document structure makes the retrieved context easier to cite and keeps related workflow steps together. The soft-heading rule matters because some documents, such as the Macros and Keyboard Shortcuts articles, use standalone bold labels as section boundaries instead of regular Markdown headings.

This approach also avoids the main weakness of simple fixed-size chunking: cutting through menu instructions, shortcut tables, or step-by-step workflows. Each chunk keeps metadata such as `source_file`, `source_url`, `title`, `document_type`, `product`, `heading_path`, `chunk_index`, and token counts so retrieval and citations can show where an answer came from.

**Final chunk count:**

The final chunk count is 61 chunks across 14 documents. This includes 60 chunks from official documentation and 1 chunk from the YouTube transcript.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

The system uses `all-MiniLM-L6-v2` through `sentence-transformers` for embeddings. It stores the embeddings in a persistent ChromaDB collection named `propresenter_chunks`, using cosine similarity for dense semantic search. The default retrieval setting is `top_k = 5`.

Each chunk is embedded with more than just the raw chunk text. The embedding input includes the title, heading path, document type, source file, chunk index, and chunk text. Adding this metadata helps short chunks retain their ProPresenter context, especially for terms like Looks, Stage Screens, Bibles, Macros, Media Inspector, Audio Routing, and Audience Screens.

**Production tradeoff reflection:**

I chose `all-MiniLM-L6-v2` because it is small, fast, free to run locally, and good enough for a small English-language RAG project. It works well as an MVP because the corpus is relatively small and most questions are practical support questions rather than extremely long or multilingual queries.

If this were deployed for real users and cost was not a constraint, I would compare larger or newer embedding models based on accuracy, context length, latency, privacy, and multilingual support. I would also strongly consider hybrid retrieval, combining semantic vector search with BM25 keyword search, because this project includes exact UI labels, shortcuts, menu paths, and short feature names that dense retrieval can miss. A production version could also add metadata boosting and reranking so multi-concept questions retrieve the most useful chunks more reliably.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system uses Groq's `llama-3.3-70b-versatile` model for answer generation. Before generation, it retrieves the top matching chunks from ChromaDB and formats them as numbered sources with titles, URLs, heading paths, source files, chunk indexes, retrieval scores, and chunk text. The model receives only the user's question and this retrieved ProPresenter context.

The grounding prompt used by the system says:

```text
You are a ProPresenter support assistant for an unofficial guide.

Grounding rules:
- Answer only from the retrieved ProPresenter context provided by the user message.
- If the context does not contain enough information, say that the provided ProPresenter documents do not contain enough information to answer.
- If the question is vague, ask one concise clarifying question and, only if useful, mention the documented areas that may be relevant.
- Do not use general product knowledge, assumptions, or unrelated advice.
- Include source attribution with [Source N] markers for every factual claim that comes from the context.
- Keep answers practical and concise.
```

**How source attribution is surfaced in the response:**

Retrieved chunks are formatted as `Source 1`, `Source 2`, and so on before being sent to the model. The system prompt requires the generated answer to use `[Source N]` markers for factual claims. After the answer, the CLI prints a source list showing each source number, retrieval score, article title, heading path, local source file, chunk index, and URL.

This structure makes the answer auditable: the user can see both the generated response and the exact retrieved documents that supported it. It also helps expose failures, such as cases where the answer says there is not enough information because retrieval missed a relevant source or because the corpus does not directly contain the needed cross-feature detail.

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
