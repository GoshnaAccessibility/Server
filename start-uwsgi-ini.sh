#!/bin/bash -
source .venv/bin/activate
uwsgi --protocol=http --ini config/wsgi.ini
