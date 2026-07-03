.PHONY: all validate build report quality export-neo4j export-rdf build-index test docs-links check clean

all: check

validate:
	python3 scripts/validate_seed_data.py

build:
	python3 scripts/build_graph.py

report: build
	python3 scripts/write_graph_report.py

quality: build
	python3 scripts/write_quality_report.py

export-neo4j: build
	python3 scripts/export_neo4j_csv.py

export-rdf: build
	python3 scripts/export_rdf_turtle.py

build-index:
	python3 scripts/build_curated_index.py --input-dir data/curated/giac_khang --output data/indexes/giac_khang/curated_evidence_index.json

test:
	python3 -m unittest discover -s tests

docs-links:
	python3 scripts/validate_docs_links.py

check: validate report quality export-neo4j export-rdf docs-links test
	python3 -m py_compile scripts/build_graph.py scripts/validate_seed_data.py scripts/import_manual_transcript.py scripts/vtt_to_evidence.py scripts/review_evidence.py scripts/batch_review_helper.py scripts/promote_reviewed_evidence.py scripts/build_curated_index.py scripts/search_curated_evidence.py scripts/ask_curated_evidence.py scripts/write_graph_report.py scripts/write_quality_report.py scripts/export_neo4j_csv.py scripts/export_rdf_turtle.py scripts/validate_docs_links.py

clean:
	rm -rf scripts/__pycache__ tests/__pycache__
