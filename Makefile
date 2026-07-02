.PHONY: all validate build report check clean

all: check

validate:
	python3 scripts/validate_seed_data.py

build:
	python3 scripts/build_graph.py

report: build
	python3 scripts/write_graph_report.py

check: validate report
	python3 -m py_compile scripts/build_graph.py scripts/validate_seed_data.py scripts/write_graph_report.py

clean:
	rm -rf scripts/__pycache__
