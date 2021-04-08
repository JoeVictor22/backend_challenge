.PHONY: install test swagger

default: start

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

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

venv:
	virtualenv venv
	. $(shell pwd)/venv/bin/activate
	pip install -r requirements.txt

test: export STAGE=test
test: venv
	PYTHONPATH=. pytest

swagger:
	python swagger_server.py
