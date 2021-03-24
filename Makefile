.PHONY: install test

default: start

install:
	pip install -r requirements.txt

create_db:
	rm -Rf migrations/
	python run.py db init
	python run.py db migrate
	python run.py db upgrade
	python -m utils.scripts.insertData

migrate_db:
	python run.py db migrate
	python run.py db upgrade

start:
	python run.py runserver

test: export STAGE=test
test:
	rm -Rf migrations/
	python run.py db init
	python run.py db migrate
	python run.py db upgrade
	python -m utils.scripts.insertData

test:
	PYTHONPATH=. pytest
