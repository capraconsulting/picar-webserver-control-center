#!/usr/bin/env sh

scp -i raspberry_picar_rsa server.py requirements.txt pi@raspberrypi.local:/home/pi/picar_webserver
