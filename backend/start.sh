#!/bin/bash
pip3 install -r /root/offline/requirements.txt


python3 /root/offline/app.py > /root/offline/output.log 2>&1 &