# MBTA Tracker App

## About the project
Don't miss the T! Boston T Station schedule tracker. 

## Getting started


### Local Installation
If on a raspberry pi or normal computer, you still need to install the requirements via:
```sh
pip3 install -r requirements.txt
```

### Connecting to Raspberry Pi
```sh
ssh pi@raspberrypi.local
```

### Run the tracker
Go to project root directory, and run:
```sh
# Adafruit led matrix
sudo python3 -m src.main

# Simulator
sudo python3 -m src.main simulate
```
