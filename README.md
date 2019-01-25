# Goshna Server

## Install

> ./install.sh

## Run (debug/testing)

1) Activate the VirtualEnvironment (if not already active):

> source flask/bin/activate

2a) then run the application directly:

> PYTHONPATH=.. python app.py

2b) or run it through flask:

> FLASK_APP=app.py flask run --host=0.0.0.0

Alternatively, run the convenience script:
> ./start.sh

To exit the VirtualEnvironment, use:
> deactivate

## Test running through uWSGI (localhost:5000)

Ensure the VirtualEnvironment is active:

> source flask/bin/activate

then

> PYTHONPATH=.. uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:application
