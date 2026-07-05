.PHONY: all validate build report quality export-neo4j export-rdf build-index dashboard health health-strict source-registry add-source-example download-transcript-example test docs-links check clean source

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

dashboard:
	PYTHONPATH=src python3 scripts/build_corpus_dashboard.py

health:
	PYTHONPATH=src python3 scripts/check_corpus_health.py

health-strict:
	PYTHONPATH=src python3 scripts/check_corpus_health.py --strict

source-registry:
	PYTHONPATH=src python3 scripts/source_registry.py validate

add-source-example:
	PYTHONPATH=src python3 scripts/add_new_source.py youtube --dry-run --url "https://www.youtube.com/watch?v=example123" --title "Example" --speaker "HT. Thích Giác Khang" --topic "Example topic"

download-transcript-example:
	PYTHONPATH=src python3 scripts/download_transcript.py source_youtube_fisp_arohzy8 --dry-run

test:
	python3 -m unittest discover -s tests

docs-links:
	python3 scripts/validate_docs_links.py

check: validate report quality export-neo4j export-rdf docs-links test
	python3 -m py_compile build_backend/dharma_build.py src/dharma_kg/citations.py src/dharma_kg/youtube.py src/dharma_kg/registry.py src/dharma_kg/source_pipeline.py src/dharma_kg/quality.py scripts/build_graph.py scripts/validate_seed_data.py scripts/import_manual_transcript.py scripts/vtt_to_evidence.py scripts/review_evidence.py scripts/batch_review_helper.py scripts/promote_reviewed_evidence.py scripts/build_curated_index.py scripts/build_corpus_dashboard.py scripts/source_registry.py scripts/add_new_source.py scripts/download_transcript.py scripts/run_source_pipeline.py scripts/search_curated_evidence.py scripts/ask_curated_evidence.py scripts/system_health_check.py scripts/seed_dharma_core.py scripts/load_test.py scripts/stress_safety_test.py scripts/stress_test.py scripts/day1_common.py scripts/day1_system_health_check.py scripts/day1_latency_baseline.py scripts/day1_retrieval_audit.py scripts/day1_safety_audit.py scripts/day1_truth_engine_snapshot.py scripts/day1_graph_health.py scripts/day1_generate_report.py scripts/day2_consistency_check.py scripts/write_graph_report.py scripts/write_quality_report.py scripts/export_neo4j_csv.py scripts/export_rdf_turtle.py scripts/validate_docs_links.py

clean:
	rm -rf scripts/__pycache__ tests/__pycache__

source:
	PYTHONPATH=src python3 -m dharma_kg.source_pipeline --source "$(SOURCE)" --teacher "$(TEACHER)" --title "$(TITLE)"
