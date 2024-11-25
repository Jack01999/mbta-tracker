from __future__ import annotations

import datetime
import time
from dataclasses import dataclass
from enum import Enum
from threading import Thread
from typing import TYPE_CHECKING, List, Optional

import numpy as np
import requests
from requests.adapters import HTTPAdapter, Retry

from controller.data import PixelDisplay, dimensions, draw_text, str_to_lines

if TYPE_CHECKING:
    from controller import Controller


try:
    with open("credentials.txt", "r", encoding="utf-8") as file:
        api_key = file.read().strip()
except FileNotFoundError:
    api_key = None
    print("No API key found.")
else:
    print("API key found.")

headers = {"Accept": "application/json", "x-api-key": api_key}

BASE_URL = "https://api-v3.mbta.com"

# enum direction inbound / outbound


class Direction(Enum):
    INBOUND = "direction"
    OUTBOUND = "direction"


# convert to inbour string
# Direction.INBOUND.name
class Mbta:

    _TIMEOUT = 10  # seconds

    _BG = np.zeros((dimensions.height, dimensions.width, 3), dtype=np.int32)
    _BG.flags.writeable = False

    def __init__(self, controller: Controller):
        self.controller = controller
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retries)

        self._pixels = self._BG.copy()

        self.session.mount("https://", adapter)
        self.session.headers.update(headers)

        self._stop = "place-cntsq"
        self._direction = Direction.INBOUND

    @property
    def pixels(self) -> PixelDisplay:
        """Return a copy of pixels."""
        # TODO: Pylint error
        return self._pixels

    def start(self):
        """Polling method placeholder."""
        Thread(target=self._main_loop, daemon=True).start()

    def _main_loop(self):
        """Main loop placeholder."""
        err_postfix = "."
        while True:

            try:
                alerts = self._get_alerts(self._stop)
                alerts = self._parse_alerts(alerts) if alerts else []

                # If there is an alert with a short header, display it
                for count, alert in enumerate(alerts):
                    short_header = alert.short_header
                    if short_header is None:
                        continue
                    print(f"Alert: {short_header}")

                    short_header = f"Alert {count + 1}/{len(alerts)}: {short_header}"

                    lines = str_to_lines(short_header)  # .upper())

                    # display four rows at a time
                    for i in range(0, len(lines), 4):
                        self._pixels = draw_text(
                            pixels=self._BG.copy(), lines=lines[i : i + 4]
                        )
                        time.sleep(5)

                for _ in range(5):
                    self._pixels = self._train_arrival_pixels()
                    time.sleep(3)

            except Exception as err:
                print(f"Error: {err}")
                lines = ["Connection", "error, trying", "again" + err_postfix]
                self._pixels = draw_text(pixels=self._BG.copy(), lines=lines)
                err_postfix = err_postfix + "." if len(err_postfix) < 3 else "."
                time.sleep(1)

    def _get(self, url: str, params: dict) -> dict:
        """Placeholder for a class method."""
        try:
            print(f"GET {url} {params}")
            response = requests.get(
                url, params=params, headers=headers, timeout=self._TIMEOUT
            )
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                print(f"Error {response.status_code}: {response.text}")
                raise http_err

            response_json = response.json()
            print(f"Success {response.status_code}")
            return response_json
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request exception: {req_err}")
        except Exception as err:
            print(f"Error occurred: {err}")
            raise
        raise ValueError("No data returned from API")

    def _get_predictions(self, stop: str, direction: int, limit: int) -> dict:
        """Fetch predictions data from the MBTA API."""
        url = f"{BASE_URL}/predictions"
        params = {
            "filter[stop]": stop,
            "filter[direction_id]": direction,
            "page[limit]": limit,
        }
        return self._get(url, params)

    def _get_vehicles(self, vehicle_id: str) -> dict:
        """Fetch vehicle data from the MBTA API."""
        url = f"{BASE_URL}/vehicles/{vehicle_id}"

        return self._get(url, {})

    def _get_lines(self) -> dict:
        """Fetch line data from the MBTA API."""
        url = f"{BASE_URL}/lines"
        return self._get(url, {})

    def _get_facilities(self) -> dict:
        """Fetch facility data from the MBTA API."""
        url = f"{BASE_URL}/facilities"
        return self._get(url, {})

    def _get_alerts(self, stop: str) -> dict:
        """Fetch alert data from the MBTA API."""
        url = f"{BASE_URL}/alerts"
        params = {"filter[stop]": stop}
        return self._get(url, params)

    @dataclass
    class Alert:
        cause: Optional[str]
        """ ex: MAINTENANCE """

        description: Optional[str]
        """ ex: November 24: Closure will extend to JFK/UMass. """

        service_effect: Optional[str]
        """ ex: Red Line shuttle """

        header: Optional[str]
        """ ex: Red Line: Shuttle Buses are replacing service between Harvard & Broadway through Nov. 24 for track work. Shuttles will not be directly servicing Park St/Downtown Crossing. Board shuttles at Haymarket or State. The work will extend to JFK on Nov 24. """

        short_header: Optional[str]
        """ ex: Red Ln: Shuttle Buses replace service between Harvard & Broadway, Nov 18-24 for track work. """

        timeframe: Optional[str]
        """ ex: Through Tomorrow """

    def _parse_alerts(self, data: dict) -> List[Alert]:
        resp = []
        data = data.get("data", {})
        for alert in data:
            attributes = alert.get("attributes", {})
            resp.append(
                self.Alert(
                    cause=attributes.get("cause"),
                    description=attributes.get("description"),
                    service_effect=attributes.get("service_effect"),
                    header=attributes.get("header"),
                    short_header=attributes.get("short_header"),
                    timeframe=attributes.get("timeframe"),
                )
            )
        return resp

    def _get_arrival_times(self, stop: str, direction: int, limit: int) -> List[str]:
        """Process predictions data to get arrival times."""
        data = self._get_predictions(stop, direction, limit)
        if data is None:
            raise ValueError("No data returned from API")

        curr_time = datetime.datetime.now(datetime.timezone.utc)
        arrival_times = []

        for prediction in data.get("data", []):
            attributes = prediction.get("attributes", {})
            relationships = prediction.get("relationships", {})

            status = attributes.get("status")
            departure_time_str = attributes.get("departure_time")
            arrival_time_str = attributes.get("arrival_time")
            vehicle_data_rel = relationships.get("vehicle", {}).get("data", {})
            vehicle_id = vehicle_data_rel.get("id")
            stop_id = relationships.get("stop", {}).get("data", {}).get("id")

            if status:
                arrival_times.append(status)
                continue

            if not departure_time_str:
                continue

            if arrival_time_str:
                arrival_time = datetime.datetime.fromisoformat(arrival_time_str)
            else:
                arrival_time = datetime.datetime.fromisoformat(departure_time_str)

            seconds = (arrival_time - curr_time).total_seconds()

            # check if the vehicle is boarding
            if seconds <= 90 and vehicle_id:
                vehicle_data = self._get_vehicles(vehicle_id)
                if vehicle_data:
                    vehicle_attrs = vehicle_data.get("data", {}).get("attributes", {})
                    vehicle_stop_id = (
                        vehicle_data.get("data", {})
                        .get("relationships", {})
                        .get("stop", {})
                        .get("data", {})
                        .get("id")
                    )
                    if (
                        vehicle_attrs.get("current_status") == "STOPPED_AT"
                        and vehicle_stop_id == stop_id
                    ):
                        arrival_times.append("Boarding")
                        continue

            if seconds < 0:
                continue

            if seconds <= 30:
                arrival_times.append("Arriving")
                continue

            if seconds <= 60:
                arrival_times.append(f"{int(seconds)} sec")
                continue

            minutes = int(round(seconds / 60))
            if minutes > 20:
                arrival_times.append("20+ minutes")
            else:
                arrival_times.append(f"{minutes} min")

        # Ensure a fixed number of arrival times for consistent display
        while len(arrival_times) < limit:
            arrival_times.append("--")

        return arrival_times[:limit]

    def _train_arrival_pixels(self) -> PixelDisplay:
        """Display inbound or outbound train arrival times based on button index."""
        inbound = self.controller.keyboard.button_a_index % 2 == 0
        direction = 0 if inbound else 1
        direction_label = "Inbound" if inbound else "Outbound"

        arrival_times = self._get_arrival_times(self._stop, direction, 4)

        lines = [
            "Central Sq",
            direction_label,
            *arrival_times[:2],  # Display only the first two arrival times
        ]

        pixels = self._BG.copy()
        pixels = draw_text(pixels=pixels, lines=lines)
        return pixels
