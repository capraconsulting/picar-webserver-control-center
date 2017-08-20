#!/usr/bin/env sh

# Clean .pyc files

echo "Deleting *.pyc files"
find . -name *.pyc -delete

# Application files
echo "Copying applicaton files to Raspberry pi at raspberrypi.local"
scp -i raspberry_picar_rsa -r server.py deployment/ controls/ requirements.txt pi@raspberrypi.local:/home/pi/picar_webserver
