# PiCar Control Center Web Server

This repository contains the code of the web server component of the PiCar control center.

## Requirements
  ```bash
  sudo apt-get install python-dev
  sudo apt-get install python-virtualenv

  cd control-center installation-folder/
  virtualenv venv # Only during first installation
  source venv/bin/activate
  pip install -r requirements.txt
  ```

The code is intended to run on a Raspberry Pi, powering a [SunFounder PiCar-S](https://www.sunfounder.com/robotic-drone/smartcar/picar-s/picar-s-kit.html)
