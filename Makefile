.PHONY: all validate build report export-neo4j export-rdf test check clean

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

test:
	python3 -m unittest discover -s tests

check: validate report export-neo4j export-rdf test
	python3 -m py_compile scripts/build_graph.py scripts/validate_seed_data.py scripts/write_graph_report.py scripts/export_neo4j_csv.py scripts/export_rdf_turtle.py

clean:
	rm -rf scripts/__pycache__ tests/__pycache__
