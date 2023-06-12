# MBTA Tracker App

## About the project
Don't miss the T! Boston T Station schedule tracker. 

## Getting started


### Local Installation
Go to project root directory, and run:
```sh
# ONLY on local computer, NOT on raspberrypi
pip3 install -r requirements.txt
```

### Run the tracker
Go to project root directory, and run:
```sh
# Adafruit led matrix
sudo python3 -m src.mbta-tracker

# Matplotlib simulator
python3 -m src.mbta-tracker simulate
```
