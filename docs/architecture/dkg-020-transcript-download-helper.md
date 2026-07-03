# DKG-020: Transcript Download Helper

## Purpose

DKG-020 adds a CLI helper for downloading YouTube subtitle transcripts for a
registered source.

The helper reads the Source Registry, resolves the source URL and video id, and
saves the transcript into the expected raw source folder.

## Input

Default registry input:

```text
data/registry/sources.json
```

The command accepts a registered `source_id`.

## Output

Default transcript output:

```text
data/raw/giac_khang/<video_id>/source.<language>.vtt
```

For the pilot source:

```text
data/raw/giac_khang/FISpARohzy8/source.vi.vtt
```

## yt-dlp Requirement

The helper uses `yt-dlp` through subprocess.

It checks:

```bash
python3 -m yt_dlp --version
yt-dlp --version
```

If neither command is available, install it with:

```bash
python3 -m pip install yt-dlp
```

## CLI Usage

Dry run:

```bash
PYTHONPATH=src python3 scripts/download_transcript.py source_youtube_fisp_arohzy8 --dry-run
```

Download transcript:

```bash
PYTHONPATH=src python3 scripts/download_transcript.py source_youtube_fisp_arohzy8
```

Force overwrite:

```bash
PYTHONPATH=src python3 scripts/download_transcript.py source_youtube_fisp_arohzy8 --force
```

Use cookies if needed:

```bash
PYTHONPATH=src python3 scripts/download_transcript.py source_youtube_fisp_arohzy8 --cookies cookies.txt
```

## File Naming Rule

The default output path is:

```text
data/raw/giac_khang/<video_id>/source.<language>.vtt
```

If `--output` is provided, that path is used instead.

## Safety Rules

- Do not overwrite existing transcript files unless `--force` is used.
- Do not modify processed data.
- Do not modify reviewed data.
- Do not modify curated data.
- Do not modify index files.
- Preserve Vietnamese Unicode.
- Support `--dry-run` without writing files or calling `yt-dlp`.

## Registry Status Update

Registry update is optional.

When `--update-registry` is used after a successful download, the helper:

- sets `ingestion_status` to `transcript_downloaded`
- appends the final transcript path to `raw_paths`
- updates source `updated_at`
- updates registry metadata `updated_at`

The registry is not updated when download fails.

## Next Step

After download, run batch ingestion:

```bash
PYTHONPATH=src python3 scripts/vtt_to_evidence.py \
  data/raw/giac_khang/<video_id>/source.vi.vtt \
  --limit 50 \
  --output data/processed/giac_khang/<video_id>/evidence_batch_001.json
```
