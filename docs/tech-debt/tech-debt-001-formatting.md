# TECH-DEBT-001: Format repository files for human review

Several repository files are currently difficult to review in GitHub raw views
because they appear minified or overly compressed:

- `scripts/validate_seed_data.py`
- `data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json`
- `docs/architecture/dkg-003-real-transcript-pilot.md`
- `README.md`

This does not block DKG-004. The current data model and validation work can
continue.

However, this must be fixed before large-scale transcript ingestion. Human
review will become much harder once many transcript sources, documents,
citations, and Evidence nodes are added. Formatting should be normalized before
the repository grows further.
