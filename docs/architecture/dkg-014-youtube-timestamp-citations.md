# DKG-014: YouTube Timestamp Citation Links

## Purpose

DKG-014 adds clickable source links for Evidence citations.

Curated Evidence already stores source URL and timestamps. This step derives a
YouTube timestamp URL so users can open the source video at the exact Evidence
start time.

## Input

The citation link is derived from Evidence fields:

- `source_url`
- `start_time`
- `end_time`
- `video_id` or source URL video id when available

No raw, processed, or reviewed data is changed.

## Timestamp Rule

`start_time` is converted to floor seconds.

Supported input forms:

- `00:02:37.959`
- `00:02:37`
- `02:37`
- `157`

Each value maps to `157` seconds.

## Citation URL Format

YouTube watch, short, and embed URLs are normalized to watch URLs with `t=`:

```text
https://www.youtube.com/watch?v=FISpARohzy8&t=157s
```

Supported YouTube source formats:

- `https://www.youtube.com/watch?v=FISpARohzy8`
- `https://youtu.be/FISpARohzy8`
- `https://www.youtube.com/embed/FISpARohzy8`

## Non-YouTube Sources

If `source_url` is not a supported YouTube URL, no timestamp URL is generated.

If `start_time` is missing or invalid, no timestamp URL is generated.

## Search Output

Search results include `citation_url` in JSON output.

Text output includes a `Citation URL:` line when a timestamp URL can be built.

## Ask Output

Ask results include `citation_url` for every matched Evidence item in both text
and JSON output.

The answer remains grounded only in matched curated Evidence text.

## Safety Rules

- Do not change raw data.
- Do not change processed data.
- Do not overwrite reviewed data.
- Do not alter `evidence_text`.
- Preserve existing citation metadata.
- Compute timestamp links from `source_url` and `start_time`.

## Next Step

Use timestamp links in Graph Explorer and local search/ask workflows to support
faster human source checking.
