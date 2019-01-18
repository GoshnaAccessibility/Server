#!/bin/bash -
sudo apt-get install python-pip python-virtualenv
rm -rf .venv/
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
