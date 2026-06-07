# Retrieval Approach Analysis

This note compares practical retrieval options for the current ProPresenter RAG source set. It is a planning document only; it does not implement the final retrieval pipeline or directly update `planning.md`.

## Corpus Summary

The current project is an unofficial guide for ProPresenter operators in church and media team environments. Based on the established chunking strategy, the corpus is expected to contain:

- Official Renewed Vision support articles.
- One or more YouTube transcript sources.
- Structured Markdown with source metadata, titles, headings, lists, screenshots, links, and some tables.
- Product-specific terms such as Looks, Props, Stage Screens, Macros, Themes, Bibles, Media Inspector, Screen Configuration, Audio Routing, and Audience Screens.
- Practical operator questions that may use informal language instead of official documentation wording.

This matters for retrieval because ProPresenter questions often mix exact UI vocabulary with natural-language descriptions. A volunteer may ask "How do I put a timer on the back screen?" while the relevant documentation may use terms like "stage screen," "audience screen," "countdown," or "looks." A good retriever should handle both precise product terms and semantic similarity.

## Core Retrieval Concepts

### Embeddings

An embedding model converts text into a numeric vector. Texts with similar meanings are placed near each other in vector space. This is why semantic search can find relevant chunks even when the query does not share exact words with the source document.

Example:

```text
User query: "How do I send different content to the confidence monitor?"
Likely source wording: "Using a Stage Screen to its Full Potential"
```

The query does not need to say "stage screen" for semantic search to find that article, because "confidence monitor" and "stage screen" are meaningfully related in this domain.

### Top-k

`top_k` is the number of retrieved chunks passed into the generation step. If `top_k = 5`, the retriever returns the five highest-ranked chunks for the user's query.

Choosing `top_k` is a recall-versus-noise tradeoff:

- Too few chunks can miss a key detail, especially for questions that combine multiple ProPresenter concepts.
- Too many chunks can crowd the prompt with weakly related context, increase latency, confuse the LLM, and make citations less precise.

For this project, a reasonable MVP default is `top_k = 5`.

## Strategy A: Dense Semantic Vector Search

### Description

Embed every chunk using a sentence embedding model, embed the user query with the same model, then rank chunks by vector similarity. Cosine similarity is a common scoring method.

Suggested MVP model:

```text
all-MiniLM-L6-v2 via sentence-transformers
```

### Pros

- Finds conceptually related chunks even when wording differs.
- Strong fit for volunteer-style questions written in plain language.
- Simple to implement with `sentence-transformers` and a local vector index.
- Fast and inexpensive for a small student project.
- Works well with heading-aware chunks because each chunk should represent a coherent topic.

### Cons

- Can miss exact technical details such as menu labels, shortcuts, acronyms, or UI feature names.
- May retrieve a generally related article instead of the exact workflow.
- Small models may underperform on domain-specific language.
- Results can be harder to debug than keyword search because vector similarity is less transparent.

### Best Use Case

Best baseline for natural-language support questions like:

- "How do I show different things on the projector and the back screen?"
- "How can I add scripture slides during service?"
- "Where do I adjust the audio output?"

### Expected Retrieval Quality

Medium-high for the MVP. It should answer many practical questions well, but evaluation may reveal misses around exact shortcuts, menu names, or narrow feature names.

## Strategy B: Keyword or Lexical Search

### Description

Use exact word matching to rank chunks. A common production-style algorithm is BM25, which rewards chunks that contain important query terms.

### Pros

- Strong for exact feature names and UI labels.
- Good for queries involving shortcuts, menus, acronyms, and named ProPresenter features.
- Easier to inspect and debug than vector search.
- Does not require an embedding model.

### Cons

- Weak when the user uses different words from the documentation.
- Cannot reliably infer that "confidence monitor" may mean "stage screen."
- May over-rank chunks that repeat a word without answering the question.

### Best Use Case

Useful for queries like:

- "What does Command-K do?"
- "Where is Media Inspector?"
- "How do I use Looks?"
- "What is the File menu shortcut?"

### Expected Retrieval Quality

Medium by itself. It is useful for exact product terminology, but not enough for informal support questions.

## Strategy C: Hybrid Retrieval

### Description

Combine dense vector search with keyword search. For example, retrieve candidates from both semantic search and BM25, merge the results, remove duplicates, and sort by a combined score.

### Pros

- Captures both meaning and exact product vocabulary.
- Better suited to this domain than either dense or keyword retrieval alone.
- Helps with queries that contain a mix of informal wording and exact terms.
- More resilient when one retriever misses a relevant chunk.

### Cons

- More implementation work than a single retriever.
- Requires score normalization or a merge strategy.
- Can produce duplicate or near-duplicate chunks if not cleaned up.
- Adds tuning decisions: how many chunks from each retriever, how to weight scores, and when to prefer exact matches.

### Best Use Case

Likely the best production retrieval strategy for this project, especially when the corpus grows to include official docs, transcripts, Reddit posts, and troubleshooting notes.

### Expected Retrieval Quality

High if tuned carefully. It should improve both recall and precision for ProPresenter support questions.

## Strategy D: Metadata-Aware Retrieval

### Description

Use chunk metadata during retrieval. Metadata can be used for filtering, boosting, display, or citation.

Useful fields from the chunking plan include:

- `source_file`
- `source_url`
- `title`
- `document_type`
- `product`
- `heading_path`
- `chunk_index`
- `start_timestamp`
- `end_timestamp`
- `start_seconds`
- `end_seconds`

### Pros

- Improves citation quality.
- Can prioritize likely-relevant sources, such as the Keyboard Shortcuts article for shortcut questions.
- Helps separate official docs from transcripts or future community sources.
- Enables timestamp citations for video transcript chunks.
- Can support later filters such as "official documentation only."

### Cons

- Strict filters can accidentally remove useful context.
- Requires consistent metadata extraction during ingestion.
- If metadata is incomplete or noisy, filtering can make retrieval worse.
- Metadata alone does not solve semantic matching.

### Best Use Case

Best used as a light boost and citation layer in the MVP, not as strict filtering.

Example:

```text
If query contains "shortcut", "hotkey", or key symbols, boost chunks whose title includes "Keyboard Shortcuts".
```

### Expected Retrieval Quality

Medium-high as a supporting strategy. It should make results easier to cite and can improve ranking for obvious document categories.

## Strategy E: MMR or Diversity-Aware Retrieval

### Description

Maximum Marginal Relevance (MMR) retrieves chunks that are relevant to the query while reducing redundancy among selected chunks.

Instead of returning five very similar chunks from the same article, MMR may return a more diverse set of relevant chunks.

### Pros

- Reduces repeated context.
- Useful for broad questions that need several angles.
- Helps when multiple chunks from the same article rank highly but say similar things.
- Can improve answer coverage without increasing `top_k`.

### Cons

- May skip a highly relevant neighboring chunk because it looks too similar.
- Adds another tuning parameter for relevance versus diversity.
- Less useful for narrow, exact questions where the best few chunks may legitimately come from the same source.

### Best Use Case

Good for broad troubleshooting or setup questions, such as:

- "How do I set up screens for a service?"
- "How do I route ProPresenter into livestream and in-room displays?"
- "What should I check if the stage display is wrong?"

### Expected Retrieval Quality

Medium-high for broad questions. Use cautiously for exact workflow questions.

## Strategy F: Reranked Retrieval

### Description

Use a two-stage retrieval pipeline:

1. Retrieve a larger candidate set, such as 10-20 chunks, with vector or hybrid retrieval.
2. Use a stronger reranker, often a cross-encoder model, to reorder candidates.
3. Pass only the best final chunks to the LLM.

### Pros

- Improves precision when the first-stage retriever finds the right chunk but ranks it too low.
- Stronger at judging query-chunk relevance than embeddings alone.
- Can make final context cleaner without lowering recall.

### Cons

- Adds latency.
- Adds implementation complexity.
- May require another model dependency or API.
- Probably unnecessary until evaluation shows ranking problems.

### Best Use Case

Best after the MVP, once test questions show that relevant chunks are being retrieved but not consistently placed in the top 4-6 results.

### Expected Retrieval Quality

High, but with higher cost and latency.

## Strategy G: Query Expansion or Query Rewriting

### Description

Before retrieval, rewrite or expand the user's query with likely related ProPresenter terms.

Example:

```text
Original query:
"How do I put words on the back monitor for singers?"

Expanded query:
"stage screen confidence monitor lyrics singers ProPresenter"
```

### Pros

- Can improve recall when users ask questions in informal language.
- Useful for domain synonyms such as "confidence monitor" and "stage screen."
- Can be implemented with a small rule-based synonym map for the MVP.

### Cons

- Poor expansions can pull retrieval away from the user's intent.
- LLM-based rewriting adds latency and may introduce incorrect assumptions.
- Rule-based synonyms require maintenance.

### Best Use Case

Useful later if evaluation shows repeated misses caused by vocabulary mismatch.

### Expected Retrieval Quality

Medium as a standalone technique, but potentially valuable as a small enhancement layered on top of vector or hybrid retrieval.

## Strategy H: Parent-Child Retrieval

### Description

Embed smaller child chunks for precise matching, but return a larger parent section to the LLM for context.

Example:

```text
Child chunk embedded:
"Starting a Timer"

Parent context returned:
"How to Create a Countdown for an Audience Screen > Basic Countdown"
```

### Pros

- Improves retrieval precision while preserving enough context for generation.
- Good for step-by-step workflows.
- Can reduce the risk that a retrieved chunk is too narrow to answer the full question.

### Cons

- More complex storage model.
- Requires mapping child chunks back to parent sections.
- May return too much context if parent sections are large.

### Best Use Case

Useful if chunk evaluation shows that small chunks retrieve well but do not provide enough context for complete answers.

### Expected Retrieval Quality

High for procedural docs, but more complex than the MVP needs unless context gaps appear during testing.

## Short, Opinion-Based Text Considerations

The current corpus is mostly official documentation, not short opinion-based text. However, the domain description mentions Reddit threads and community troubleshooting as possible future sources. Those sources would require extra retrieval care because posts and comments are short, noisy, subjective, and often context-dependent.

For short opinion-based text:

- Embed the comment text plus lightweight context, such as thread title and subreddit.
- Preserve metadata like author, date, score, URL, and thread title.
- Group very short adjacent comments only when they are part of the same reply chain.
- Avoid treating a single opinion as authoritative.
- Prefer retrieval that can separate official docs from community advice.
- Use citations clearly so generated answers do not blur documentation with anecdotes.

This suggests a future split retrieval design:

```text
Official docs retriever -> authoritative setup instructions
Community retriever -> troubleshooting patterns and lived experience
```

The generation step should then label community-derived guidance more cautiously than official documentation.

## Recommended MVP Approach

For the first implementation, use:

- Dense semantic retrieval.
- `all-MiniLM-L6-v2` through `sentence-transformers`.
- Cosine similarity.
- `top_k = 5`.
- Chunk metadata attached to every result.
- Light metadata boosting for obvious categories, if simple to implement.

This is the best MVP because it is easy to build, inexpensive to run, and likely good enough for the current English, official-documentation-heavy corpus.

Recommended retrieval flow:

1. Load chunk records from the chunking pipeline.
2. Build embedding text from the chunk title, heading path, and chunk body.
3. Embed chunks with `all-MiniLM-L6-v2`.
4. Store vectors with chunk metadata.
5. Embed the user query.
6. Retrieve the top 5 chunks by cosine similarity.
7. Include each chunk's source metadata in the final context.
8. Ask the LLM to answer only from retrieved context and cite sources.

Suggested embedded text format:

```text
Title: Using Bibles in ProPresenter
Section: Bible Slide Options
Type: official_docs

[chunk text here]
```

Adding title and section text to the embedded content should improve matching for product-specific terms without requiring a more complex retriever.

## Recommended Future Upgrade Path

If MVP evaluation exposes retrieval weaknesses, upgrade in this order:

1. Add metadata-aware boosting for obvious categories.
2. Add BM25 and merge it with semantic search for hybrid retrieval.
3. Add MMR for broad troubleshooting questions.
4. Add a reranker if the right chunks appear in the candidate set but not at the top.
5. Add query expansion for recurring vocabulary mismatches.
6. Add parent-child retrieval if small chunks are too narrow for generation.

## Top-k Recommendation

Recommended default:

```text
top_k = 5
```

Suggested tuning rules:

| Query type | Suggested top-k | Reasoning |
| --- | ---: | --- |
| Exact shortcut or menu question | 3 | Narrow query; fewer chunks reduce noise. |
| Standard feature question | 5 | Good balance of context and focus. |
| Multi-feature workflow | 6-8 | May require chunks from multiple articles. |
| Broad troubleshooting question | 6-8 with MMR | Needs coverage across related concepts without repetition. |
| Very small corpus debugging | 10 | Useful only while inspecting retrieval behavior, not as final generation context. |

The final prompt should usually receive about 4-6 high-quality chunks. More than that may be useful for candidate retrieval, but a reranker or filter should narrow the final context.

## Production Tradeoff Reflection

If this guide were deployed for real users and cost was not a constraint, model choice should be evaluated across:

- **Accuracy:** Larger or newer embedding models may retrieve better chunks for complex troubleshooting and domain-specific terms.
- **Context length:** Longer-context embedding models can represent larger sections without losing as much meaning.
- **Domain-specific performance:** ProPresenter-specific terms should be tested directly, not assumed to work.
- **Multilingual support:** Real church media teams may ask questions in languages other than English.
- **Latency:** Local small models are fast and predictable; hosted larger models may improve quality but add API round trips.
- **Cost:** Hosted embeddings and rerankers can add ongoing cost.
- **Privacy:** Local embeddings keep church-specific setup questions inside the app.
- **Maintainability:** Simple retrieval is easier to explain and debug; hybrid and reranked systems need more evaluation infrastructure.

For production, the likely best system would be:

```text
Hybrid retrieval + metadata boosting + reranking
```

That means semantic search for meaning, BM25 for exact ProPresenter terms, metadata for source-aware prioritization, and a reranker to select the final 4-6 chunks passed to the LLM.

## Evaluation Questions for Retrieval

These questions can be used to test whether retrieval is finding the right source chunks before generation is evaluated:

| # | Test query | Expected retrieval behavior |
| --- | --- | --- |
| 1 | "How do I show different content on the projector and stage monitor?" | Retrieve chunks about Looks, Stage Screens, and Screen Configuration. |
| 2 | "Where do I set up scripture slides?" | Retrieve chunks from Using Bibles in ProPresenter. |
| 3 | "How do I make a countdown for the audience screen?" | Retrieve chunks from the countdown article, especially Basic Countdown or Starting a Timer sections. |
| 4 | "What shortcut opens the inspector?" | Retrieve Keyboard Shortcuts and/or Media Inspector chunks. |
| 5 | "How do I route audio out of ProPresenter?" | Retrieve Audio Routing and Audio Outputs chunks. |
| 6 | "How do I install and activate ProPresenter?" | Retrieve timestamped transcript chunks from the installation video. |

## Implementation Notes for Later

- Store the original chunk text and metadata separately from the embedded text.
- Include title and heading path in the embedded text.
- Use deterministic chunk IDs so embeddings can be regenerated cleanly.
- Log retrieved chunk IDs, scores, titles, and heading paths during development.
- Keep source URLs and transcript timestamps attached to every retrieved result.
- Do not pass low-score chunks into generation just to fill `top_k`.
- During evaluation, inspect retrieval results before judging generation quality.
- If retrieval fails, fix retrieval before trying to fix the prompt.

## Assumptions

- The first implementation will use local, English-language embeddings.
- The source set remains small enough that a simple vector index is acceptable.
- The current priority is clear, cited answers for practical ProPresenter operation.
- Official documentation should be treated as more authoritative than future community or opinion-based sources.
