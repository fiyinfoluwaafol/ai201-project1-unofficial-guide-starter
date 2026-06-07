# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

My domain is an unofficial guide for ProPresenter operators in church/media team environments. The guide focuses on practical questions around lyrics, scriptures, stage display, audience screens, looks, props, macros, lower thirds, OBS/ATEM routing, and common Sunday-service troubleshooting. This knowledge is valuable because new volunteers often have to learn ProPresenter through scattered official docs, YouTube tutorials, Reddit threads, and last-minute troubleshooting during service.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | YouTube Video | How to Download + Install ProPresenter | https://www.youtube.com/watch?v=7awG_JK6eWo |
| 2 | Official Documentation | Understanding The ProPresenter User Interface | https://support.renewedvision.com/hc/en-us/articles/360041345954-Understanding-The-ProPresenter-User-Interface |
| 3 | Official Documentation | Keyboard Shortcuts in ProPresenter | https://support.renewedvision.com/hc/en-us/articles/360042123293-Keyboard-Shortcuts-in-ProPresenter |
| 4 | Official Documentation | Using Bibles in ProPresenter | https://support.renewedvision.com/hc/en-us/articles/360041347594-Using-Bibles-in-ProPresenter |
| 5 | Official Documentation | Using a Stage Screen to its Full Potential | https://support.renewedvision.com/hc/en-us/articles/360041407794-Using-a-Stage-Screen-to-its-Full-Potential |
| 6 | Official Documentation | Using Macros in ProPresenter | https://support.renewedvision.com/hc/en-us/articles/4402663090323-Using-Macros-in-ProPresenter |
| 7 | Official Documentation | Using Looks to Show Different Screen Content in ProPresenter | https://support.renewedvision.com/hc/en-us/articles/360041407174-Using-Looks-to-Show-Different-Screen-Content-in-ProPresenter |
| 8 | Official Documentation | Audio Routing in ProPresenter | https://support.renewedvision.com/hc/en-us/articles/360052696094-Audio-Routing-in-ProPresenter |
| 9 | Official Documentation | Audio Outputs in ProPresenter | https://support.renewedvision.com/hc/en-us/articles/360052697694-Audio-Outputs-in-ProPresenter |
| 10 | Official Documentation | Screen Configuration in ProPresenter | https://support.renewedvision.com/hc/en-us/articles/360041879173-Screen-Configuration-in-ProPresenter |
| 11 | Official Documentation | What is the Media Inspector | https://support.renewedvision.com/hc/en-us/articles/7200487649299-What-is-the-Media-Inspector |
| 12 | Official Documentation | Creating and Using Playlist Templates in ProPresenter | https://support.renewedvision.com/hc/en-us/articles/40377194830995-Creating-and-Using-Playlist-Templates-in-ProPresenter |
| 13 | Official Documentation | Guide to Using Themes in ProPresenter | https://support.renewedvision.com/hc/en-us/articles/34551484745875-Guide-to-Using-Themes-in-ProPresenter |
| 14 | Official Documentation | How to Create a Countdown for an Audience Screen | https://support.renewedvision.com/hc/en-us/articles/360050786794-How-to-Create-a-Countdown-for-an-Audience-Screen |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

For official documentation, I will use hybrid heading-aware chunks. The chunker should first split each Markdown file by meaningful document structure: Markdown headings (`#`, `##`, `###`) and conservative standalone bold section labels such as `**File Menu**` or `**Creating a Macro**` when they function like headings. Most target chunks should land around 400-700 tokens.

For YouTube transcripts, I will use timestamp-group chunks instead of heading chunks. The chunker should group adjacent timestamp paragraphs into chunks of roughly 250-500 words, preserving the first and last timestamp for citation.

The maximum chunk size should be about 800-1,000 tokens. If a heading section is larger than that, it should be split further by paragraph, list block, or table block so that instructions and shortcut tables stay readable.

**Overlap:**

Use little or no overlap for normal heading-based chunks because the headings already preserve context. Add about 75-125 tokens of overlap only when splitting an oversized section into multiple sub-chunks.

**Reasoning:**

The current source set is mostly official Renewed Vision documentation with useful article titles, headings, lists, screenshots, links, and some table-heavy reference content. A simple fixed-size splitter would be easy to build, but it could cut through workflows, menu sections, keyboard shortcut tables, or troubleshooting instructions. Heading-aware chunking should produce cleaner retrieval results and better citations.

Some documents only have one top-level heading but use bold standalone labels as real section boundaries, so the chunker should treat those as soft headings when they are short, text-only labels. The YouTube transcript is different because its natural structure is time-based, so timestamp grouping will make later citations more useful.

Each chunk should preserve metadata such as `source_file`, `source_url`, `title`, `document_type`, `product`, `heading_path`, `chunk_index`, `text`, `token_count`, and transcript-only fields like `start_timestamp`, `end_timestamp`, `start_seconds`, and `end_seconds`.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
