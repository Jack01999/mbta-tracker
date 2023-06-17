import copy
import sys
import time
from typing import List
import numpy as np
import requests
import datetime
from src.algs import draw_character, key_to_character
from src.data.types import LedMatrix, Program
from src.displays.adafruit import AdaFruit
from src.data.fonts import default_font
from src.displays.simulate import Simulate
import src.data.state as state

# Example URLs
# redline_centralsq_outbound_url = 'https://api-v3.mbta.com/predictions?filter[stop]=place-cntsq&filter[direction_id]=1&page[limit]=3'
# redline_centralsq_inbound_url = 'https://api-v3.mbta.com/predictions?filter[stop]=place-cntsq&filter[direction_id]=0&page[limit]=3'
try:
    with open("credentials.txt", "r") as file:
        api_key = file.read().strip()
except:
    api_key = None

headers = {"Accept": "application/json", "x-api-key": api_key}

matrix_to_display = LedMatrix(
    pixels=copy.deepcopy(state.background),
)


def getArrivalTimes(stop: str, direction: int, limit: int):
    # Fetch
    response = requests.get(
        url=f"https://api-v3.mbta.com/predictions?filter[stop]={stop}&filter[direction_id]={direction}&page[limit]={limit}",
        headers=headers,
        auth=None,
    )
    # Stringify the promise to data
    data = response.json()
    print("x-ratelimit-remaining: ", response.headers["x-ratelimit-remaining"])
    # We don't need to worry about 'null' data for the arrival_time because the station we're predicting is not a 'first stop' station
    # If there is something wrong, we can use the 'schedule_relationship' field to figure out why.

    # Get current time
    currTime = datetime.datetime.now()
    arrivalTimes = []
    for stop in data["data"]:
        # Convert fetched string to datetime format
        time = datetime.datetime.strptime(
            stop["attributes"]["arrival_time"], "%Y-%m-%dT%H:%M:%S-%f:00"
        )
        # seconds till arrival time
        arrivalSecs = (time - currTime).total_seconds()
        # minutes till arrival time
        arrivalMins = round(arrivalSecs / 60)
        if arrivalMins <= 0:
            arrivalTimes.append("Arrived")
        else:
            arrivalTimes.append(str(arrivalMins) + "min")
    return arrivalTimes


"""
*INFO*
-- Parameter 0 --
stop: place-cntsq = "Central Square Station"
stop: place-davis = "Davis Square Station"
stop: place-portr = "Porter Square Station"

-- Parameter 1 -- 
direction: 0 = Inbound
direction: 1 = Outbound

-- Parameter 2 --
limit: Number of next "x" arrival times you want to see.


There are a list set of rules from the documentation that we should take into account (https://www.mbta.com/developers/v3-api/best-practices)
1. If `status` is non-null:
	Display this value as-is
2. If `departure_time` is null:
	Do not display this prediction, since riders won't be able to board the vehicle
3. Calculate the number of seconds until the vehicle reaches the stop, by subtracting the current time from the arrival time (if available) or the departure time (if not); call this value "seconds"
4. If seconds < 0
	Do not display this prediction, since the vehicle has already left the stop
5. If seconds <= 90, and the `status` of the associated `vehicle` is "STOPPED_AT", and the vehicle's `stop` is the same as the prediction's `stop`:
	Display "Boarding" (abbrev. "BRD")
6. If seconds is <= 30
	Display "Arriving" (abbrev. "ARR")
7. If seconds is <= 60
	Display "Approaching" (abbrev. "1 min")
8. Round the seconds value to the nearest whole number of minutes, rounding up if exactly in-between; call this value "minutes"
9. If minutes > 20
	Display “20+ minutes” (abbrev. “20+ min”)
10. Display the number of minutes followed by "minutes" (abbrev. "min"). For example:
	Up to 89 seconds: "1 minute" or "1 min"
	90 to 149 seconds: "2 minutes" or "2 min"
	150 to 209 seconds: "3 minutes" or "3 min"
"""


def update_train_times():
    while True:
        print(
            "Central Square - Red Line - Inbound - ",
            getArrivalTimes("place-cntsq", 0, 3),
        )
        # print(
        #     "Central Square - Red Line - Outbound - ",
        #     getArrivalTimes("place-cntsq", 1, 3),
        # )
        print(
            "------------------------------------------------------------------------------"
        )


def print_text(display, lines: List[str] = ["Hello World,", "how are you?"]):
    """Update the display with this, return immediatly"""

    matrix_to_display = LedMatrix(
        pixels=copy.deepcopy(state.background),
    )

    # clear the background
    matrix_to_display.pixels = copy.deepcopy(state.background)

    row_index = 0
    for line in lines:
        col_index = 0
        for character_key in line:
            character = key_to_character(default_font, character_key)

            if col_index + character.width_px >= state.width:
                print(f"Charcter is to long")
                return

            if row_index + default_font.height_px >= state.height:
                print("To many rows")
                return

            matrix_to_display = draw_character(
                matrix_to_display,
                character,
                row_index + 1 if character.dropdown else row_index,
                col_index,
            )
            col_index += character.width_px + 1
        row_index += default_font.height_px + 1

    display.display_matrix(matrix_to_display)


def print_default_font(display):
    """Display the entire default font one page at a time,
    displaying each page for 1 second"""

    # clear the page
    matrix_to_display = LedMatrix(
        pixels=copy.deepcopy(state.background),
    )

    col_index = 0
    row_index = 0

    for character in default_font.characters:
        # new row is needed for this character
        if col_index + character.width_px >= state.width:
            col_index = 0
            row_index += default_font.height_px + 1

        # new page is needed for this character
        if row_index + default_font.height_px >= state.height:
            display.display_matrix(matrix_to_display)
            time.sleep(1)

            # clear the page
            row_index = 0
            col_index = 0
            matrix_to_display.pixels = copy.deepcopy(state.background)

        matrix_to_display = draw_character(
            matrix_to_display,
            character,
            row_index + 1 if character.dropdown else row_index,
            col_index,
        )

        # move imaginary curser to the start of the next character
        col_index += character.width_px + 1

    display.display_matrix(matrix_to_display)
    time.sleep(1)


strobe_frequency_hz = 2

last_strobe_time = time.time()

strobe_on = False


def strobe(display):
    global last_strobe_time, strobe_on
    strobe_time_between = 1 / strobe_frequency_hz

    if strobe_on:
        pixels = np.zeros((state.height, state.width, 3), dtype=np.int8)
    else:
        pixels = np.full((state.height, state.width, 3), state.bit_depth, dtype=np.int8)
        

    matrix_to_display = LedMatrix(
        pixels=pixels,
    )

    time_d = time.time() - last_strobe_time  # always positive

    if time_d < strobe_time_between:
        time.sleep(strobe_time_between - time_d)
    else:
        print(f"strobe {time_d- strobe_time_between} seconds to slow")


    last_strobe_time = time.time()
    strobe_on = not strobe_on

    display.display_matrix(matrix_to_display)


if __name__ == "__main__":
    # Main function of the entire program

    # select display output
    if len(sys.argv) > 1 and sys.argv[-1] == "simulate":
        display = Simulate()
    else:
        display = AdaFruit()

    # TODO: start button thread here
    program = Program.STROBE

    try:
        print("Press CTRL-C to stop")
        while True:
            # try:
            if program == Program.BALL_BOUNCE:
                pass
            elif program == Program.MBTA:
                lines = ["    Central SQ.", "Inbound", "10 min", "11 min"]
                print_text(display, lines=lines)
                pass
            elif program == Program.STROBE:
                strobe(display)
                pass

            # except:
            #     print("Error, waiting 3 seconds and trying again")
            #     time.sleep(3)

    except KeyboardInterrupt:
        print("Exiting\n")
        sys.exit(0)
