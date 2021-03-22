.PHONY: install test

default: test

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=. pytest
