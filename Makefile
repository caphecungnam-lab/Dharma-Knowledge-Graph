.PHONY: all validate build report export-neo4j export-rdf check clean

all: check

validate:
	python3 scripts/validate_seed_data.py

build:
	python3 scripts/build_graph.py

report: build
	python3 scripts/write_graph_report.py

export-neo4j: build
	python3 scripts/export_neo4j_csv.py

export-rdf: build
	python3 scripts/export_rdf_turtle.py

check: validate report export-neo4j export-rdf
	python3 -m py_compile scripts/build_graph.py scripts/validate_seed_data.py scripts/write_graph_report.py scripts/export_neo4j_csv.py scripts/export_rdf_turtle.py

clean:
	rm -rf scripts/__pycache__
