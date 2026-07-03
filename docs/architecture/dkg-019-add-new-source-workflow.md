# DKG-019: Add New Source Workflow

## Purpose

DKG-019 creates a standard workflow for registering a new source or video in the
Giac Khang Corpus.

The workflow updates the Source Registry and creates the expected folder
scaffold for ingestion, review, curation, and indexing.

## Input

The command accepts YouTube metadata:

- URL
- title
- speaker
- topic
- language
- corpus id
- source owner

It does not download YouTube content.

## Generated Source ID

The source id is derived from the YouTube video id:

```text
source_youtube_<lowercase_video_id>
```

For example:

```text
source_youtube_fisp_arohzy8
```

## Registry Update

The workflow appends a new source entry to:

```text
data/registry/sources.json
```

New sources start with safe default statuses:

- `status: planned`
- `ingestion_status: pending`
- `review_status: not_started`
- `curation_status: not_started`
- `index_status: not_indexed`
- `health_status: unknown`

## Folder Scaffold

For a video id, the workflow creates:

```text
data/raw/giac_khang/<video_id>/
data/processed/giac_khang/<video_id>/
data/reviewed/giac_khang/<video_id>/
data/curated/giac_khang/<video_id>/
```

Each directory receives a `README.md` placeholder.

## Safety Rules

- Do not modify existing source data except `data/registry/sources.json`.
- Do not overwrite raw, processed, reviewed, or curated files.
- Do not download YouTube content yet.
- Fail if `source_id` already exists.
- Fail if `video_id` already exists unless `--allow-duplicate-video-id` is used.
- Preserve Vietnamese Unicode.
- Support `--dry-run` for no-write previews.

## CLI Usage

Dry run:

```bash
PYTHONPATH=src python3 scripts/add_new_source.py youtube \
  --dry-run \
  --url "https://www.youtube.com/watch?v=NEW_VIDEO_ID" \
  --title "Title here" \
  --speaker "HT. Thích Giác Khang" \
  --topic "Topic here"
```

Create scaffold and registry entry:

```bash
PYTHONPATH=src python3 scripts/add_new_source.py youtube \
  --url "https://www.youtube.com/watch?v=NEW_VIDEO_ID" \
  --title "Title here" \
  --speaker "HT. Thích Giác Khang" \
  --topic "Topic here" \
  --language vi \
  --corpus-id corpus_giac_khang
```

## Example

```bash
PYTHONPATH=src python3 scripts/add_new_source.py youtube \
  --dry-run \
  --url "https://www.youtube.com/watch?v=example123" \
  --title "Example" \
  --speaker "HT. Thích Giác Khang" \
  --topic "Example topic"
```

The command prints the folders that would be created and the next pipeline
commands.

## Next Step

After registration, download or place the transcript at:

```text
data/raw/giac_khang/<video_id>/source.vi.vtt
```

Then run batch ingestion, initialize review, promote reviewed Evidence, rebuild
the index, dashboard, and health gate.
