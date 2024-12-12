# import openmeteo_requests

# import requests_cache
# import pandas as pd
# from retry_requests import retry

# # Setup the Open-Meteo API client with cache and retry on error
# cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
# retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
# openmeteo = openmeteo_requests.Client(session = retry_session)

# # Make sure all required weather variables are listed here
# # The order of variables in hourly or daily is important to assign them correctly below
# url = "https://api.open-meteo.com/v1/forecast"
# params = {
# 	"latitude": 42.3584,
# 	"longitude": -71.0598,
# 	"hourly": "temperature_2m",
# 	"temperature_unit": "fahrenheit",
# 	"timezone": "GMT",
# 	"forecast_days": 1
# }
# responses = openmeteo.weather_api(url, params=params)

# # Process first location. Add a for-loop for multiple locations or weather models
# response = responses[0]
# print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
# print(f"Elevation {response.Elevation()} m asl")
# print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
# print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# # Process hourly data. The order of variables needs to be the same as requested.
# hourly = response.Hourly()
# hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

# hourly_data = {"date": pd.date_range(
# 	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
# 	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
# 	freq = pd.Timedelta(seconds = hourly.Interval()),
# 	inclusive = "left"
# )}
# hourly_data["temperature_2m"] = hourly_temperature_2m

# hourly_dataframe = pd.DataFrame(data = hourly_data)
# print(hourly_dataframe)
from __future__ import annotations

import datetime
import time
from threading import Thread
from typing import TYPE_CHECKING

import numpy as np
import requests
from requests.adapters import HTTPAdapter, Retry

from controller.data import PixelDisplay, dimensions, draw_lines_on, save_json

if TYPE_CHECKING:
    from controller import Controller


class Clock:
    _BG = np.zeros((dimensions.height, dimensions.width, 3), dtype=np.int32)

    _TIMEOUT = 5

    _TIMES = {
        1: "One",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six",
        7: "Seven",
        8: "Eight",
        9: "Nine",
        10: "Ten",
        11: "Eleven",
        12: "Twelve",
        13: "Thirteen",
        14: "Fourteen",
        15: "Fifteen",
        16: "Sixteen",
        17: "Seventeen",
        18: "Eighteen",
        19: "Nineteen",
        20: "Twenty",
        21: "Twenty One",
        22: "Twenty Two",
        23: "Twenty Three",
        24: "Twenty Four",
        25: "Twenty Five",
        26: "Twenty Six",
        27: "Twenty Seven",
        28: "Twenty Eight",
        29: "Twenty Nine",
        30: "Thirty",
        31: "Thirty One",
        32: "Thirty Two",
        33: "Thirty Three",
        34: "Thirty Four",
        35: "Thirty Five",
        36: "Thirty Six",
        37: "Thirty Seven",
        38: "Thirty Eight",
        39: "Thirty Nine",
        40: "Forty",
        41: "Forty One",
        42: "Forty Two",
        43: "Forty Three",
        44: "Forty Four",
        45: "Forty Five",
        46: "Forty Six",
        47: "Forty Seven",
        48: "Forty Eight",
        49: "Forty Nine",
        50: "Fifty",
        51: "Fifty One",
        52: "Fifty Two",
        53: "Fifty Three",
        54: "Fifty Four",
        55: "Fifty Five",
        56: "Fifty Six",
        57: "Fifty Seven",
        58: "Fifty Eight",
        59: "Fifty Nine",
        60: "Sixty",
    }

    _MONTHS = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }

    _WEEKDAYS = {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun",
    }

    def __init__(self, controller: Controller):
        self.controller = controller
        self._pixels = self._BG.copy()

        self._session = requests.Session()
        adapter = HTTPAdapter(
            max_retries=Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"],
            )
        )
        self._session.mount("https://", adapter)

        self._forecast = {}

    @property
    def pixels(self) -> PixelDisplay:
        """Return a copy of pixels."""
        return self._pixels

    def start(self):
        """Start the clock's main loop in a separate thread."""
        Thread(target=self._main_loop, daemon=True).start()
        Thread(target=self._http_loop, daemon=True).start()

    def _get(self, url: str, params: dict) -> dict:
        """Generic method to fetch data from an http API."""
        try:
            print(f"GET {url} {params}")
            response = requests.get(url, params=params, timeout=self._TIMEOUT)
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

    def _http_loop(self):
        def inner():
            self._forecast = self._get_forecast()

        while True:
            try:
                inner()
            except Exception as err:
                print(f"Error in temperature HTTP loop: {err}")

            time.sleep(120)

    def _parse_temperature(self, data: dict) -> str:
        """
        Parse and interpolate the temperature from the forecast data
        """
        if not data:
            return "-"
        try:
            times = data["hourly"]["time"]
            temps = data["hourly"]["temperature_2m"]
        except KeyError:
            print("Error parsing forecast data")
            return "-"

        time_temps = {
            datetime.datetime.fromisoformat(t).astimezone(datetime.timezone.utc): temp
            for t, temp in zip(times, temps)
        }
        now = datetime.datetime.now(datetime.timezone.utc)

        prev_hour, next_hour = None, None
        for t, temp in time_temps.items():

            if t > now:
                next_hour = t
                break
            elif t < now:
                prev_hour = t
            else:
                return temp

        if prev_hour is None or next_hour is None:
            return str(sum(temps) / len(temps))  # Fallback to average temp
        temp_delta = time_temps[next_hour] - time_temps[prev_hour]
        time_delta = now - prev_hour
        time_since = time_delta.total_seconds() / 3600

        interpolated_temp = time_temps[prev_hour] + temp_delta * time_since

        return f"{interpolated_temp:.1f}"

    def _get_forecast(self) -> dict:
        """Fetch the weather forecast. Request it in America/New_York timezone."""
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 42.365732,
            "longitude": -71.099705,
            "hourly": "temperature_2m",
            "temperature_unit": "fahrenheit",
            "timezone": "GMT",
            "past_days": 2,
            "forecast_days": 2,
        }
        return self._get(url, params)

    def _main_loop(self):
        """Main loop for updating the clock display."""
        while True:
            self._pixels = self._clock_pixels()
            # sleep until next 0.1 second
            now = datetime.datetime.now()
            sleep_time = 0.1 - now.microsecond / 1e7
            time.sleep(max(0.01, sleep_time))

    def _clock_pixels(self) -> PixelDisplay:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        hour_12 = hour % 12 or 12

        d = ""

        if minute == 0:
            lines = [self._TIMES[hour_12], "O'Clock", " ", d]
        else:
            min_word = self._TIMES[minute].split(" ")
            if len(min_word) == 1:
                lines = [
                    self._TIMES[hour_12].lower(),
                    (
                        "o' " + min_word[0].lower()
                        if minute < 10
                        else min_word[0].lower() + "  "
                    ),
                    " ",
                    d,
                ]
            else:
                lines = [
                    self._TIMES[hour_12].lower(),
                    min_word[0].lower(),
                    min_word[1].lower(),
                    d,
                ]

        pixels = np.zeros((dimensions.height, dimensions.width, 3), dtype=np.int32)
        draw_lines_on(pixels, lines)
        draw_lines_on(
            pixels,
            [" ", " ", " ", f"-right-{self._parse_temperature(self._forecast)}°F"],
            vertical_shift=1
        )
        return pixels
