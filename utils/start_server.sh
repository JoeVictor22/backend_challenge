#!/bin/bash

./venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8080 -m 007 wsgi:app