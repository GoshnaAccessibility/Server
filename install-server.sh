#!/bin/bash -
sudo apt-get install python-pip python-virtualenv
mkdir /opt/goshna -p
cp -rf . /opt/goshna
cd /opt/goshna
rm -rf .venv/
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
mv -f config/goshna.service /etc/systemd/system/goshna.service
sudo systemctl start goshna
sudo systemctl enable goshna
