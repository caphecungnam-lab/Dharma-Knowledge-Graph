# DKG-011: Batch Evidence Ingestion

## Purpose

DKG-011 expands the Giac Khang pilot from the initial five VTT-derived
Evidence nodes into a larger batch that can enter the same review and curation
workflow.

The goal is still Evidence-first corpus building. The repository should ingest
real caption text from the source VTT file, preserve timestamps, and avoid any
invented transcript content.

## Source

The source file is:

```text
data/raw/giac_khang/FISpARohzy8/source.vi.vtt
```

The source video metadata remains:

- YouTube URL: `https://www.youtube.com/watch?v=FISpARohzy8`
- Video ID: `FISpARohzy8`
- Speaker: `HT. Thích Giác Khang`
- Topic: `Kinh Sáu Sáu`

## Batch Strategy

The VTT converter now supports controlled batch extraction through CLI options:

```bash
python3 scripts/vtt_to_evidence.py data/raw/giac_khang/FISpARohzy8/source.vi.vtt --limit 50
python3 scripts/vtt_to_evidence.py data/raw/giac_khang/FISpARohzy8/source.vi.vtt --start-time 00:00:00 --end-time 00:20:00 --limit 50
python3 scripts/vtt_to_evidence.py data/raw/giac_khang/FISpARohzy8/source.vi.vtt --output data/processed/giac_khang/FISpARohzy8/evidence_batch_001.json
```

For the first batch, the repository generates up to 50 Evidence nodes from the
first 20 minutes of the video and writes them to:

```text
data/processed/giac_khang/FISpARohzy8/evidence_batch_001.json
```

## ID Strategy

Evidence IDs remain stable and sequential:

```text
evidence_fisp_arohzy8_0001
evidence_fisp_arohzy8_0002
...
evidence_fisp_arohzy8_0050
```

The converter supports `--start-index` so later batches can continue the same
sequence without changing earlier IDs.

## Review Workflow

Batch output is processed data, not trusted corpus data.

The intended flow is:

```text
raw VTT -> processed Evidence batch -> review queue -> curated Evidence -> search / ask
```

Every generated Evidence node starts with:

```text
review_status: unreviewed
confidence: low
```

Human review is still required before promotion to curated corpus data.

## Safety Rules

- Do not invent transcript text.
- Do not paraphrase caption text during ingestion.
- Do not overwrite the raw VTT file.
- Do not overwrite `evidence_first_pass.json` when creating a batch.
- Preserve Vietnamese Unicode from the VTT source.
- Keep citation and document relationships attached to each Evidence node.

## Next Step

The next step is to create a review queue for
`evidence_batch_001.json`, then promote only human-reviewed Evidence into the
curated corpus.
