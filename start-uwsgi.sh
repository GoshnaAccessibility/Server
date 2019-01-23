#!/bin/bash -
source .venv/bin/activate
PYTHONPATH=.. uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:application
