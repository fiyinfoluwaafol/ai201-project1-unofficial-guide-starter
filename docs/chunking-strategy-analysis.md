# Chunking Strategy Analysis

This note compares practical chunking options for the current ProPresenter RAG source set. It is a planning document only; it does not implement the final chunking pipeline.

## Corpus Summary

The current `documents/` folder contains 14 Markdown files:

| Document type | Count | Notes |
| --- | ---: | --- |
| `official_docs` | 13 | Renewed Vision support articles about ProPresenter features and workflows. |
| `youtube_transcript` | 1 | A manually cleaned transcript for downloading, installing, and activating ProPresenter. |

All sampled files have YAML front matter with useful source metadata:

- `title`
- `source`
- `type`
- `product`

Most files are structured documentation pages. They usually have a single `#` title and then a mix of `##` / `###` headings, paragraphs, images, lists, links, and occasional tables. Some official docs use standalone bold text as section labels instead of Markdown headings, so a chunker should probably treat lines like `**Creating a Macro**` or `**File Menu**` as soft section boundaries.

Approximate corpus stats from `scripts/analyze_docs_for_chunking.py`:

| File | Type | Words | Markdown headings | Bold section labels | Table lines | List lines | Timestamp lines |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `audio-outputs-in-propresenter.md` | official docs | 398 | 2 | 0 | 0 | 0 | 0 |
| `audio-routing-in-propresenter.md` | official docs | 836 | 3 | 0 | 0 | 0 | 0 |
| `creating-and-using-playlist-templates-in-propresenter.md` | official docs | 266 | 3 | 3 | 0 | 12 | 0 |
| `guide-to-using-themes-in-propresenter.md` | official docs | 448 | 8 | 0 | 0 | 11 | 0 |
| `how-to-create-a-countdown-for-an-audience-screen.md` | official docs | 1752 | 4 | 0 | 0 | 5 | 0 |
| `keyboard-shortcuts-in-propresenter.md` | official docs | 569 | 1 | 7 | 101 | 0 | 0 |
| `propresenter_installation.md` | YouTube transcript | 519 | 3 | 0 | 0 | 0 | 19 |
| `screen-configuration-in-propresenter.md` | official docs | 689 | 1 | 0 | 0 | 4 | 0 |
| `understanding-the-propresenter-user-interface.md` | official docs | 1414 | 7 | 0 | 0 | 7 | 0 |
| `using-a-stage-screen-to-its-full-potential.md` | official docs | 1333 | 1 | 5 | 0 | 3 | 0 |
| `using-bibles-in-propresenter.md` | official docs | 1325 | 7 | 0 | 0 | 16 | 0 |
| `using-looks-to-show-different-screen-content-in-propresenter.md` | official docs | 629 | 3 | 0 | 0 | 0 | 0 |
| `using-macros-in-propresenter.md` | official docs | 591 | 1 | 4 | 0 | 0 | 0 |
| `what-is-the-media-inspector.md` | official docs | 580 | 1 | 0 | 0 | 6 | 0 |

Largest observed sections are still modest:

| Section | File | Approx. words |
| --- | --- | ---: |
| Screen Configuration in ProPresenter | `screen-configuration-in-propresenter.md` | 685 |
| Basic Countdown | `how-to-create-a-countdown-for-an-audience-screen.md` | 654 |
| What is the Media Inspector | `what-is-the-media-inspector.md` | 575 |
| Starting a Timer | `how-to-create-a-countdown-for-an-audience-screen.md` | 539 |
| Transcript | `propresenter_installation.md` | 493 |

The collection includes:

- Structured product documentation with headings and subheadings.
- Several medium-length articles, especially countdowns, UI overview, Bibles, and stage screen workflows.
- One timestamped transcript.
- Step-by-step instructions and procedural workflows.
- Lists, especially options and numbered setup steps.
- One table-heavy shortcut reference.
- Images and links embedded in the Markdown.
- Some troubleshooting-oriented details, especially audio routing, screen performance, and output configuration.
- Very little true Q&A-style content.

## Strategy A: Fixed-Size Token or Character Chunking

### Description

Split each file every fixed number of tokens or characters, for example 500-800 tokens with 50-150 tokens of overlap.

### Pros

- Easiest strategy to implement.
- Predictable chunk sizes.
- Works even when Markdown structure is poor or missing.
- Good fallback for any content type.

### Cons

- Can cut through headings, lists, tables, and multi-step instructions.
- May separate a setup step from the warning or condition that makes it useful.
- Overlap can duplicate irrelevant content and increase indexing cost.
- Citations become less meaningful because chunks may not map cleanly to article sections.

### Best Use Case

Useful as a safety fallback for unusually long sections or messy documents where no reliable structure exists.

### Risks for This ProPresenter RAG Project

This dataset has meaningful document structure. Fixed-size splitting would likely split sections like "Bible Slide Options", "Routing Audio Outputs", or keyboard shortcut tables without preserving the user's navigational context.

### Expected Retrieval Quality

Medium. It should retrieve relevant words, but answers may lose section context and may cite broad or awkward chunks.

## Strategy B: Markdown Heading-Aware Chunking

### Description

Split official docs based on Markdown headings such as `#`, `##`, and `###`. Preserve the heading hierarchy in each chunk, such as:

```text
Using Bibles in ProPresenter > Bible Slide Options
```

For this corpus, this should also consider standalone bold labels as soft headings when they appear on their own line.

### Pros

- Aligns chunks with article structure.
- Preserves user-facing concepts and workflows.
- Makes citations clearer: article title plus heading path.
- Good fit for official Renewed Vision documentation.
- Avoids unnecessary overlap for short sections.

### Cons

- Some files only have a single `#` heading, so the whole article may become one chunk unless soft headings or size fallbacks are added.
- Some headings are malformed or empty, such as a blank `##` in a couple files.
- Bold labels are not always guaranteed to be real headings.
- Large sections can still be too large for precise retrieval.

### Best Use Case

Official documentation pages with clean headings, short feature sections, or clear procedural sections.

### Risks for This ProPresenter RAG Project

If implemented using only `#` / `##` / `###`, several useful docs would be under-split:

- `screen-configuration-in-propresenter.md`
- `using-a-stage-screen-to-its-full-potential.md`
- `using-macros-in-propresenter.md`
- `keyboard-shortcuts-in-propresenter.md`
- `what-is-the-media-inspector.md`

The shortcut reference also needs table-aware handling so menu tables stay intact.

### Expected Retrieval Quality

High for well-structured docs. Medium-high overall if standalone bold section labels are treated as soft headings.

## Strategy C: Hybrid Heading-Aware and Size-Limited Chunking

### Description

First split by document structure:

1. Parse front matter.
2. Split official docs by Markdown headings.
3. Treat standalone bold labels as optional soft headings.
4. Preserve heading path in each chunk.
5. If a section exceeds a maximum size, split it further by paragraph, list block, or table block.
6. Add overlap only within oversized sections.

Suggested MVP defaults:

- Target chunk size: about 400-700 tokens.
- Maximum chunk size: about 800-1,000 tokens.
- Overlap inside oversized sections only: about 75-125 tokens.
- Keep Markdown tables intact where possible.
- Keep list items together where possible.

### Pros

- Uses the real structure of the documentation.
- Handles files with only one top-level heading.
- Avoids splitting most small sections unnecessarily.
- Keeps citations meaningful.
- Reduces duplicated text compared with global overlap.
- Flexible enough for both article-style pages and reference-style pages.

### Cons

- More implementation work than fixed-size chunking.
- Requires careful parsing rules for soft headings, empty headings, tables, images, and links.
- Needs guardrails so a bold sentence is not mistaken for a heading.

### Best Use Case

The best general-purpose strategy for this corpus: official docs are structured, but not uniformly structured.

### Risks for This ProPresenter RAG Project

The main risk is overcomplicating soft-heading detection. A conservative rule should only treat bold text as a soft heading when the whole line is bold, short, and not an image/link-only line. Another risk is splitting table-heavy shortcut content poorly; table blocks should remain attached to their menu heading.

### Expected Retrieval Quality

High. This should provide the best balance between precision, context, implementation effort, and citation quality for the MVP.

## Strategy D: Transcript-Specific Timestamp Chunking

### Description

For documents marked `type: "youtube_transcript"` or containing repeated timestamp blocks, split by groups of adjacent timestamp paragraphs. Each chunk should preserve:

- Video title.
- Video URL.
- Start timestamp.
- End timestamp.
- Transcript text.
- Chunk index.

For the current transcript, chunks might group 3-6 timestamp blocks at a time, or target about 250-500 words per chunk.

### Pros

- Preserves the natural timeline of the video.
- Enables citations to a video timestamp range.
- Avoids mixing unrelated moments from different parts of a video.
- Works better than heading chunking for transcript content because transcript sections are temporal, not article-like.

### Cons

- Timestamp blocks can be very short, so individual timestamp chunks may be too small.
- Topic changes may not align perfectly with timestamp intervals.
- Requires separate metadata fields and citation behavior.

### Best Use Case

YouTube transcripts, training videos, tutorial walkthroughs, and any source where the user may want to jump to the cited moment.

### Risks for This ProPresenter RAG Project

There is only one transcript right now, so this should stay simple. A highly tuned transcript chunker would be unnecessary. Grouping adjacent timestamp blocks is enough for the MVP.

### Expected Retrieval Quality

High for video-derived questions when chunks are grouped by timestamp range. Low-medium if each timestamp line is indexed separately because the chunks would be too fragmented.

## Strategy E: Semantic or Topic-Based Chunking

### Description

Use embeddings, an LLM, or another semantic segmentation method to split documents by topic changes instead of visible Markdown or timestamp structure.

### Pros

- Can find topic boundaries even when formatting is weak.
- May produce cleaner chunks for long narrative text.
- Could improve retrieval if future documents become much larger or less structured.

### Cons

- More complex than this MVP needs.
- Harder to debug.
- Can produce inconsistent chunks across runs.
- May add API cost or model dependency.
- Citations are less predictable unless semantic chunks are still anchored to source structure.

### Best Use Case

Large, messy corpora where heading structure is absent or unreliable.

### Risks for This ProPresenter RAG Project

Probably overkill. The current corpus is small, mostly structured, and already cleaned. Semantic chunking would add complexity before the project has enough scale to justify it.

### Expected Retrieval Quality

Potentially high, but not worth the implementation cost for the current CodePath MVP.

## Recommended MVP Approach

The proposed preference makes sense for the actual files:

- Use heading-aware chunking for official documentation.
- Include standalone bold section labels as soft headings when they are clearly section labels.
- Use timestamp-group chunking for YouTube transcripts.
- Add a max chunk size fallback so oversized sections are split by paragraph or block.
- Preserve metadata for source URL, title, document type, product, heading path, timestamps, and chunk index.

This is essentially Strategy C plus Strategy D.

Recommended MVP behavior:

1. Read each Markdown file and parse YAML front matter.
2. If `type` is `youtube_transcript`, use transcript timestamp-group chunking.
3. Otherwise, use hybrid heading-aware chunking.
4. For official docs, split on Markdown headings and conservative soft headings.
5. Keep tables, lists, and paragraphs as block-level units when applying max size fallback.
6. Drop or normalize empty headings.
7. Include heading breadcrumbs in the chunk text or metadata. Prefer metadata for storage, but adding a short heading prefix to the embedded text can improve retrieval.
8. Use overlap only when splitting an oversized section.

## Suggested Metadata Schema

Recommended chunk fields:

| Field | Type | Applies to | Notes |
| --- | --- | --- | --- |
| `chunk_id` | string | all | Stable ID, for example hash of `source_file`, `chunk_index`, and optional heading/timestamp. |
| `source_file` | string | all | Relative path such as `documents/using-bibles-in-propresenter.md`. |
| `source_url` | string | all | From front matter `source`. |
| `title` | string | all | From front matter `title` or first `#` heading. |
| `document_type` | string | all | From front matter `type`, such as `official_docs` or `youtube_transcript`. |
| `product` | string | all | Currently `ProPresenter`. |
| `heading_path` | array of strings | official docs | Example: `["Using Bibles in ProPresenter", "Bible Slide Options"]`. |
| `section_title` | string | official docs | Last item in `heading_path`; useful for display. |
| `chunk_index` | integer | all | Zero-based or one-based, but use one convention consistently. |
| `text` | string | all | The chunk text to embed and retrieve. |
| `start_timestamp` | string or null | transcripts | Example: `00:47`. |
| `end_timestamp` | string or null | transcripts | Example: `01:20`. |
| `start_seconds` | integer or null | transcripts | Useful for YouTube timestamp links. |
| `end_seconds` | integer or null | transcripts | Useful for display and range citations. |
| `token_count` | integer | all | Use the embedding model tokenizer if available; approximate is fine for early debugging. |
| `word_count` | integer | all | Optional debugging field. |
| `source_kind` | string | all | Optional display grouping, for example `article`, `shortcut_reference`, `video_transcript`. |

Optional but useful later:

- `url_with_timestamp`: for transcript chunks, precompute a YouTube URL with `t=` seconds.
- `has_table`: useful for shortcut/reference chunks.
- `has_list`: useful for procedural chunks.
- `image_refs`: if future answers need to refer to screenshots.

## Citation Guidance

For official documentation:

- Cite the source URL.
- Include the article title.
- Include the heading path when available.

Example display:

```text
Renewed Vision, "Using Bibles in ProPresenter" > "Bible Slide Options"
https://support.renewedvision.com/hc/en-us/articles/360041347594-Using-Bibles-in-ProPresenter
```

For transcripts:

- Cite the video URL.
- Include the video title.
- Include the timestamp range.
- If possible, link to the start timestamp using YouTube's `t=` parameter.

Example display:

```text
"Download, Install, and Activate ProPresenter", 01:20-02:03
https://www.youtube.com/watch?v=7awG_JK6eWo&t=80s
```

## Implementation Notes for Later

- The chunker should not treat image-only bold lines as headings, such as `**![](...)**`.
- The chunker should ignore empty headings like `##`.
- Shortcut tables should remain grouped under menu labels such as `File Menu` or `View Menu`.
- For official docs with a single heading and no soft headings, one chunk may be acceptable if the section is under the maximum size.
- If a chunk is split because it is too large, keep the same `heading_path` and increment a local sub-index or rely on `chunk_index`.
- Use a deterministic `chunk_id` so embeddings can be regenerated without producing unrelated IDs.

## Assumptions

- The current front matter format will remain simple and consistent.
- The current corpus is intentionally small enough that a transparent rule-based chunker is preferable to semantic chunking.
- The RAG system should prioritize answer accuracy and citation clarity over maximizing the number of indexed chunks.
- Future transcript files will use timestamp lines similar to `[00:47]`.
