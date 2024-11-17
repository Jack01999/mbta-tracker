from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING, List

import numpy as np
import requests

from controller.data import dimensions

if TYPE_CHECKING:
    from controller import Controller

from controller.data import draw_text

try:
    with open("credentials.txt", "r") as file:
        api_key = file.read().strip()
except FileNotFoundError:
    api_key = None
    logging.info("No API key found.")

headers = {"Accept": "application/json", "x-api-key": api_key}

"""
Example URLs
    redline_centralsq_outbound_url = 'https://api-v3.mbta.com/predictions?filter[stop]=place-cntsq&filter[direction_id]=1&page[limit]=3'
    redline_centralsq_inbound_url = 'https://api-v3.mbta.com/predictions?filter[stop]=place-cntsq&filter[direction_id]=0&page[limit]=3'

*INFO*
-- Parameter 0 --
stop: place-cntsq = "Central Square Station"
stop: place-davis = "Davis Square Station"
stop: place-portr = "Porter Square Station"

-- Parameter 1 -- 
direction: 0 = Inbound
direction: 1 = Outbound

-- Parameter 2 --
limit: Number of next "x" arrival times you want to see. Should be 2 to fit into the board.
"""


bg = np.zeros((dimensions.height, dimensions.width, 3), dtype=np.int32)
bg.flags.writeable = False


class Mbta:
    def __init__(self, controller: Controller):
        self.controller = controller
        pass

    def display_error(self, error: List[str]):
        """Display an error message to the user"""
        pixels = bg.copy()
        pixels = draw_text(pixels=pixels, lines=error)
        self.controller.display.display_matrix(pixels=pixels)

    def poll(self):
        """ """

    def fetch_predictions_data(self, stop: str, direction: int, limit: int):
        try:
            # Fetch
            response = requests.get(
                url=f"https://api-v3.mbta.com/predictions?filter[stop]={stop}&filter[direction_id]={direction}&page[limit]={limit}",
                headers=headers,
                auth=None,
            )
        except Exception as e:
            if int(response.headers["x-ratelimit-remaining"]) <= 0:
                self.display_error(["Error : ", "Invalid API", "key"])
                logging.info(f"{e}, Invalid API key.")
            self.display_error(["Error : ", "Unable to", "fetch data"])
            logging.info(f"{e}, Unable to fetch predictions data.")
        else:
            # Stringify the promise to data
            data = response.json()
            return data

    def fetch_vehicles_data(self, id: str):
        try:
            # Fetch
            response = requests.get(
                url=f"https://api-v3.mbta.com/vehicles/{id}",
                headers=headers,
                auth=None,
            )
        except Exception as e:
            self.display_error(["Error : ", "Unable to", "fetch vehicle", "data"])
            logging.info(f"{e}, Unable to fetch vehicle data.")
        else:
            # Stringify the promise to data
            data = response.json()
            return data

    def get_arrival_times(self, stop: str, direction: int, limit: int):
        data = self.fetch_predictions_data(stop, direction, limit)
        # data = mock_fetch_predictions_data()

        currTime = datetime.datetime.now()
        arrival_times = []

        # Get arrival times using predictions
        for prediction in data["data"]:
            prediction_status = prediction["attributes"]["status"]
            prediction_departure_time = prediction["attributes"]["departure_time"]
            prediction_arrival_time = prediction["attributes"]["arrival_time"]
            prediction_vehicle_id = prediction["relationships"]["vehicle"]["data"]["id"]
            prediction_stop_id = prediction["relationships"]["stop"]["data"]["id"]
            # If `status` is non-null:
            # Display this value as-is
            if prediction_status is not None:
                arrival_times.append(prediction_status)
                continue
            # If `departure_time` is null:
            # Do not display this prediction, since riders won't be able to board the vehicle
            if prediction_departure_time is None:
                continue

            # Get the seconds till next arrival_time (or departure_time)
            # Use arrival_time preferred, departure_time if arrival_time is null
            # We don't need to check if departure_time is null again, b/c we checked it above
            time = None
            if prediction_arrival_time is not None:
                time = datetime.datetime.strptime(
                    prediction_arrival_time, "%Y-%m-%dT%H:%M:%S-%f:00"
                )
            else:
                time = datetime.datetime.strptime(
                    prediction_departure_time, "%Y-%m-%dT%H:%M:%S-%f:00"
                )

            # Calculate the number of seconds until the vehicle reaches the stop, by subtracting the current time from the arrival time/departure time
            seconds = (time - currTime).total_seconds()

            # If seconds <= 90, and the `status` of the associated `vehicle` is "STOPPED_AT", and the vehicle’s `stop` is the same as the prediction’s `stop`:
            # Display "Boarding" (abbrev. "BRD")
            if seconds <= 90:
                vehicle_data = self.fetch_vehicles_data(prediction_vehicle_id)["data"]
                if (
                    vehicle_data["attributes"]["current_status"] == "STOPPED_AT"
                    and vehicle_data["relationships"]["stop"]["data"]["id"]
                    == prediction_stop_id
                ):
                    arrival_times.append("Boarding")
                    continue

            # If seconds < 0
            # Do not display this prediction, since the vehicle has already left the stop
            if seconds < 0:
                continue

            # If seconds is <= 30
            # Display "Arriving" (abbrev. "ARR")
            if seconds <= 30:
                arrival_times.append("Arriving")
                continue

            # If seconds is <= 60
            # Display "Approaching" (abbrev. "1 min")
            if seconds <= 60:
                arrival_times.append(str(round(seconds)) + "  sec")
                continue

            # Round the seconds value to the nearest whole number of minutes, rounding up if exactly in-between.
            minutes = round(seconds / 60)

            # If minutes > 20
            # Display “20+ minutes” (abbrev. “20+ min”)
            if minutes > 20:
                arrival_times.append("20+ minutes")
                continue
            else:
                arrival_times.append(str(minutes) + "  min")
                continue
        return arrival_times

    def print_text(self, lines):
        """Update the display with this, return immediately"""
        # np.zeros(
        #     (HEIGHT, WIDTH, 3), dtype=np.int32
        # )
        pixels = np.zeros((dimensions.height, dimensions.width, 3), dtype=np.int32)

        pixels = draw_text(pixels=pixels, lines=lines)

        self.controller.display.display_matrix(pixels)

    def display_train_arrival_times(self):
        # State mode loops through 0 -> 5 -> 0 whenever the button is pressed.
        # Therefore, we will use odd/even to determine whether to discount inbound or outbound
        logging.info("Displaying train arrival times")
        if self.controller.button_a_index % 2 == 0:
            arrival_time_inbound = self.get_arrival_times("place-cntsq", 0, 4)
            lines_inbound = [
                "    Central SQ.",
                "Inbound",
                f"{arrival_time_inbound[0]}",
                f"{arrival_time_inbound[1]}",
            ]
            self.print_text(lines=lines_inbound)
        else:
            arrival_time_outbound = self.get_arrival_times("place-cntsq", 1, 4)
            lines_outbound = [
                "    Central SQ.",
                "Outbound",
                f"{arrival_time_outbound[0]}",
                f"{arrival_time_outbound[1]}",
            ]
            self.print_text(lines=lines_outbound)
