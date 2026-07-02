.PHONY: all validate build report export-neo4j check clean

all: check

validate:
	python3 scripts/validate_seed_data.py

build:
	python3 scripts/build_graph.py

report: build
	python3 scripts/write_graph_report.py

export-neo4j: build
	python3 scripts/export_neo4j_csv.py

check: validate report export-neo4j
	python3 -m py_compile scripts/build_graph.py scripts/validate_seed_data.py scripts/write_graph_report.py scripts/export_neo4j_csv.py

clean:
	rm -rf scripts/__pycache__
