all: init load

.PHONY: init
init:
	python init_schema.py

.PHONY: load
load:
	python etl.py