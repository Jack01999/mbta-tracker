#!/bin/bash

print_stars() {
  width=$(tput cols)

  # padding or margins
  adjusted_width=$((width - 1))

  stars=$(printf '*%.0s' $(seq 1 $adjusted_width))
  
  echo -e "\n$stars\n$1\n$stars"
}

print_stars "Update packages"
sudo apt-get update

print_stars "setup pre-requisites for rpi-rgb-led-matrix"
sudo apt install python3-pip
sudo apt install git
sudo apt install libgraphicsmagick++-dev libwebp-dev
sudo apt install libwebp-dev

print_stars "python2.7-dev required for the make process"
sudo apt install python2.7-dev -y
sudo apt install python3-dev python3-pillow -y

print_stars "Clone rpi-rgb-led-matrix"
git clone https://github.com/hzeller/rpi-rgb-led-matrix

print_stars "Clone mbta-tracker"
git clone https://github.com/Jack01999/mbta-tracker

print_stars "Build the project using the standard hardware profile (default=regular))"
cd rpi-rgb-led-matrix
sudo HARDWARE_DESC=regular make install-python

cd utils/
sudo make led-image-viewer

cd ../examples-api-use
make

print_stars "compile for Python 3 (https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python)"
cd ../bindings/python/
sudo make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)

print_stars "Set New York timezone"
sudo timedatectl set-timezone America/New_York