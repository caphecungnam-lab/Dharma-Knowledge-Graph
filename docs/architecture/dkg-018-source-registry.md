# DKG-018: Source Registry

## Purpose

DKG-018 adds a central Source Registry for the Giac Khang Corpus.

The registry tracks every source or video, its metadata, file paths, and current
pipeline status. It is metadata only and does not replace Evidence, transcripts,
or curated corpus data.

## Registry File

The registry lives at:

```text
data/registry/sources.json
```

The file contains top-level metadata and a list of source records.

## Source Fields

Each source record includes:

- `source_id`
- `corpus_id`
- `title`
- `speaker`
- `source_owner`
- `source_kind`
- `source_url`
- `video_id`
- `language`
- `topic`
- `notes`
- `created_at`
- `updated_at`

The first source is the Giac Khang `FISpARohzy8` YouTube video for Kinh Sáu Sáu.

## Status Fields

The registry tracks source lifecycle through:

- `status`
- `ingestion_status`
- `review_status`
- `curation_status`
- `index_status`
- `health_status`

For new YouTube sources, `add-youtube` uses safe defaults:

- `status: planned`
- `ingestion_status: pending`
- `review_status: not_started`
- `curation_status: not_started`
- `index_status: not_indexed`
- `health_status: unknown`

## File Path Fields

Each source may track related files:

- `raw_paths`
- `processed_paths`
- `reviewed_paths`
- `curated_paths`
- `index_paths`

These fields must be lists. Duplicate paths inside the same source are invalid.

## CLI Usage

List sources:

```bash
python3 scripts/source_registry.py list
```

Show one source:

```bash
python3 scripts/source_registry.py show source_youtube_fisp_arohzy8
```

Validate registry:

```bash
python3 scripts/source_registry.py validate
```

Add a planned YouTube source:

```bash
python3 scripts/source_registry.py add-youtube \
  --source-id source_youtube_example \
  --video-id example \
  --url https://www.youtube.com/watch?v=example \
  --title "Example title" \
  --speaker "HT. Thích Giác Khang" \
  --topic "Example topic" \
  --language vi \
  --corpus-id corpus_giac_khang
```

Validate through Make:

```bash
make source-registry
```

## Safety Rules

- Do not change raw data.
- Do not change processed data.
- Do not change reviewed data.
- Do not change curated data.
- Keep the registry as metadata only.
- Preserve Vietnamese Unicode.
- Keep registry JSON deterministic except timestamp fields.

## Next Step

Use the registry before adding the next Giac Khang video so every source has a
clear lifecycle state before ingestion begins.
