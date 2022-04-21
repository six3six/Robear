#!/bin/bash

export FLASK_APP=server
cd /home/pi/robot
sudo -u pi FLASK_APP=server flask run -h 0.0.0.0
sudo -u pi /usr/bin/python ./camera.py