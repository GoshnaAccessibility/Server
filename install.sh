#!/bin/bash -
sudo apt-get install python-virtualenv
rm -rf flask/
virtualenv flask
source flask/bin/activate
pip install -r requirements.txt
