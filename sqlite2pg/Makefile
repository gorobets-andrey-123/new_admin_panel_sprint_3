all: clean load check

.PHONY: clean
clean:
	python truncate_tables.py

.PHONY: load
load:
	python load_data.py

.PHONY: check
check:
	python tests/check_consistency.py