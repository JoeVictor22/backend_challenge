.PHONY: install test

default: start

install:
	pip install -r requirements.txt

start:
	python run.py runserver

test:
	PYTHONPATH=. pytest
