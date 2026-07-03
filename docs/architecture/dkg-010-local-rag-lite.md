# DKG-010: Local RAG-lite

## Purpose

DKG-010 adds a local question-answer utility over curated Evidence.

It is "RAG-lite" because it retrieves curated Evidence and constructs a grounded
answer, but it does not use an LLM, embeddings, vector search, or external APIs.

## Input

The default input file is:

`data/curated/giac_khang/FISpARohzy8/evidence_curated.json`

The input can be changed with:

```bash
python3 scripts/ask_curated_evidence.py "Sư Giác Khang nói gì về 36 pháp?" --path custom/path/to/evidence_curated.json
```

## Retrieval Rule

The utility reuses the keyword and Vietnamese alias search logic from
`scripts/search_curated_evidence.py`.

It first searches the full question text. If the full question does not match,
it tries smaller keyword phrases from the question, such as numeric phrases like
`36 pháp`.

## Answer Construction Rule

The answer is constructed only from `evidence_text` in matched curated Evidence.

When multiple Evidence nodes match, their `evidence_text` values are joined in
result order. The default limit is 3 Evidence nodes.

## Citation Rule

Each answer includes citation metadata for every matched Evidence node:

- evidence id
- timestamp
- source URL
- speaker
- review status
- curated status
- citation string

## No Hallucination Rule

If no matching curated Evidence is found, the tool prints:

`Chưa có Evidence phù hợp trong curated corpus.`

The tool must not infer, summarize from memory, or add claims that are not in
matched curated Evidence.

## Limitations

This is deterministic keyword search.

It does not understand semantic similarity, resolve ambiguous doctrine terms, or
rank Evidence beyond the current curated file order.

## Next Step

The next step is to add verified Evidence and then evaluate whether a richer
retrieval layer is needed after the corpus contains more reviewed transcript
segments.
