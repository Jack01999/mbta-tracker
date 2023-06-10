#!/bin/bash



echo "************************************************************"
echo "Update packages"
echo "************************************************************"
sudo apt-get update

echo "************************************************************"
echo "setup pre-requisites for rpi-rgb-led-matrix"
echo "************************************************************"
sudo apt install git
sudo apt install libgraphicsmagick++-dev libwebp-dev
sudo apt install libwebp-dev

echo "************************************************************"
echo "python2.7-dev required for the make process"
echo "************************************************************"
sudo apt install python2.7-dev -y
sudo apt install python3-dev python3-pillow -y
echo "************************************************************"
echo "Download rpi-rgb-led-matrix project"
echo "************************************************************"
git clone https://github.com/hzeller/rpi-rgb-led-matrix

echo "************************************************************"
echo "Build the project using the standard hardware profile (default=regular))"
echo "************************************************************"
cd rpi-rgb-led-matrix
sudo HARDWARE_DESC=regular make install-python

cd utils/
sudo make led-image-viewer

cd ../examples-api-use
make

echo "************************************************************"
echo "compile for Python 3 (https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python)"
echo "************************************************************"
cd ../bindings/python/
sudo make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)