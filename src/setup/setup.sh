#!/bin/bash

echo "setup pre-requisites for rpi-rgb-led-matrix"
sudo apt-get update

sudo apt install git
sudo apt install libgraphicsmagick++-dev libwebp-dev
sudo apt install libwebp-dev

echo "python2.7-dev required for the make process"
sudo apt install python2.7-dev -y
sudo apt install python3-dev python3-pillow -y

echo "download the project"
git clone https://github.com/hzeller/rpi-rgb-led-matrix

echot "build the project using the standard hardware profile (change based on your hardware)"
cd rpi-rgb-led-matrix
sudo HARDWARE_DESC=regular make install-python

cd utils/
sudo make led-image-viewer

cd ../examples-api-use
make

echo "compile for Python 3 (https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python)"
cd ../bindings/python/
sudo make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)