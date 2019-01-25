#!/bin/bash -
sudo apt-get install python-pip python-virtualenv
mkdir /opt/goshna -p
cp -rf ../Server /opt/goshna
cd /opt/goshna/Server
rm -rf .venv/
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
mv -f config/goshna.service /etc/systemd/system/goshna.service
sudo systemctl daemon-reload
sudo systemctl start goshna
sudo systemctl enable goshna
