from __future__ import annotations

import datetime
import os
import time
from dataclasses import dataclass
from enum import Enum
from threading import Thread
from typing import TYPE_CHECKING, List, Optional

import numpy as np
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter, Retry

from controller.data import (
    PixelDisplay,
    dimensions,
    draw_lines_on,
)

if TYPE_CHECKING:
    from controller import Controller

# Load environment variables from .env file
load_dotenv()

# Try to get API key from environment variable
api_key = os.getenv("MBTA_API_KEY")

if not api_key:
    raise ValueError("No API key found.")


headers = {"Accept": "application/json", "x-api-key": api_key}

BASE_URL = "https://api-v3.mbta.com"


class Direction(Enum):
    INBOUND = "direction"
    OUTBOUND = "direction"


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


class Mbta:
    _TIMEOUT = 10  # seconds

    _BG = np.zeros((dimensions.height, dimensions.width, 3), dtype=np.int32)
    _BG.flags.writeable = False

    _TEST_ALERTS = [
        Alert(
            cause="MAINTENANCE",
            description="November 24: Closure will extend to JFK/UMass.",
            service_effect="Red Line shuttle",
            header="Red Line: Shuttle Buses are replacing service between Harvard & Broadway through Nov. 24 for track work. Shuttles will not be directly servicing Park St/Downtown Crossing. Board shuttles at Haymarket or State. The work will extend to JFK on Nov 24.",
            short_header="Red Ln: Shuttle Buses replace service between Harvard & Broadway, Nov 18-24 for track work.",
            timeframe="Through Tomorrow",
        ),
    ]

    _ERROR_MSG_LINES = ["Connection", "error, trying", "again."]

    _MAX_LOOP_TIME = 1e-3

    def __init__(self, controller: Controller):
        self.controller = controller
        self._session = requests.Session()
        adapter = HTTPAdapter(
            max_retries=Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"],
            )
        )

        self._pixels = self._BG.copy()

        self._session.mount("https://", adapter)
        self._session.headers.update(headers)

        self._stop = "place-cntsq"
        self._direction = 0  # 0 for inbound, 1 for outbound
        self._alerts: List[Alert] = []
        self._arrival_times: List[str] = []
        self._predictions: List[str] = []

    @property
    def pixels(self) -> PixelDisplay:
        """Return a copy of pixels."""
        return self._pixels

    def start(self):
        """Polling method placeholder."""
        Thread(target=self._http_loop, daemon=True).start()
        Thread(target=self._main_loop, daemon=True).start()

    def _http_loop(self):
        def innner():
            self._alerts = self._parse_alerts(self._get_alerts(self._stop))
            time.sleep(0.25)
            self._predictions = self._parse_predictions(
                self._get_predictions(self._stop, self._direction, 4)
            )
            time.sleep(0.5)

        while True:
            try:
                innner()
            except Exception as err:
                print(f"Error: {err}")
                self._pixels = draw_lines_on(
                    pixels=self._BG.copy(), lines=self._ERROR_MSG_LINES
                )
                time.sleep(1)

    def _main_loop(self):
        """Main loop placeholder."""

        horizontal_shift = 0
        prev_time = time.monotonic()
        bit_shift_delta = 1 / 11  # 11 pixels per second

        def inner():
            nonlocal horizontal_shift, prev_time
            pixels = self._BG.copy()
            pixels = draw_lines_on(
                pixels=pixels,
                lines=[
                    "Central",
                    "Inbound",
                    *self._predictions[:1],
                ],
            )

            pixels = draw_lines_on(
                pixels=pixels,
                lines=[
                    " ",
                    " ",
                    " ",
                    "Red Line: Shuttle Buses are replacing service between Harvard & Broadway through Nov. 24 for track work. Shuttles will not be directly servicing Park St/Downtown Crossing. Board shuttles at Haymarket or State. The work will extend to JFK on Nov 24.",
                ],
                horizontal_shift=horizontal_shift,
                vertical_shift=1,
            )

            # bit_shift_delta
            curr_time = time.monotonic()
            time_diff = curr_time - prev_time
            prev_time = curr_time

            time.sleep(max(self._MAX_LOOP_TIME, bit_shift_delta - time_diff))

            self._pixels = pixels
            horizontal_shift -= 1

        while True:
            err_postfix = "."
            try:
                inner()
            except Exception as err:
                print(f"Error: {err}")
                self._pixels = draw_lines_on(
                    pixels=self._BG.copy(),
                    lines=["Connection", "error, trying", "again" + err_postfix],
                )
                err_postfix = err_postfix + "." if len(err_postfix) < 3 else "."
                time.sleep(1)

    def _get(self, url: str, params: dict) -> dict:
        """Generic method to fetch data from an http API."""
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
            # save_json(response_json, f"{url.split('/')[-1]}.json")
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

    def _get_stops(self) -> dict:
        """Fetch stop data from the MBTA API."""
        url = f"{BASE_URL}/stops"
        return self._get(url, {})

    def _get_alerts(self, stop: str) -> dict:
        """Fetch alert data from the MBTA API."""
        url = f"{BASE_URL}/alerts"
        params = {"filter[stop]": stop}
        return self._get(url, params)

    def _parse_alerts(self, data: Optional[dict]) -> List[Alert]:
        if data is None:
            return []

        resp = []
        data = data.get("data", {})
        assert data is not None
        for alert in data:
            attributes = alert.get("attributes", {})
            resp.append(
                Alert(
                    cause=attributes.get("cause"),
                    description=attributes.get("description"),
                    service_effect=attributes.get("service_effect"),
                    header=attributes.get("header"),
                    short_header=attributes.get("short_header"),
                    timeframe=attributes.get("timeframe"),
                )
            )
        return resp

    def _parse_predictions(self, data: Optional[dict]) -> List[str]:
        """Process predictions data to get arrival times."""
        if data is None:
            print("Warning: Prediction data is None")
            return ["No data"]

        if not data.get("data"):
            print(f"Warning: Empty data returned from API: {data}")
            return ["No data"]

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
                arrival_times.append("1 min")
                continue

            minutes = int(round(seconds / 60))
            if minutes > 20:
                arrival_times.append("20+ min")
            else:
                arrival_times.append(f"{minutes} min")

        while len(arrival_times) < 5:
            # arbitrary large num
            arrival_times.append("--")

        return arrival_times
