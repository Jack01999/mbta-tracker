import datetime, requests, copy
import src.data.state as state

from src.algs import draw_text
from src.programs.display_error import display_error

# Example URLs
# redline_centralsq_outbound_url = 'https://api-v3.mbta.com/predictions?filter[stop]=place-cntsq&filter[direction_id]=1&page[limit]=3'
# redline_centralsq_inbound_url = 'https://api-v3.mbta.com/predictions?filter[stop]=place-cntsq&filter[direction_id]=0&page[limit]=3'
try:
    with open("credentials.txt", "r") as file:
        api_key = file.read().strip()
except:
    api_key = None

headers = {"Accept": "application/json", "x-api-key": api_key}

def fetch_predictions_data(stop: str, direction: int, limit: int):
    try:
        # Fetch
        response = requests.get(
            url=f"https://api-v3.mbta.com/predictions?filter[stop]={stop}&filter[direction_id]={direction}&page[limit]={limit}",
            headers=headers,
            auth=None,
        )
    except Exception as e:
        if int(response.headers["x-ratelimit-remaining"]) <= 0:
            display_error(["ERROR : ", "Invalid API", "key"])
            print(f"{e}, Invalid API key.")
        display_error(["ERROR : ", "Unable to", "fetch data"])
        print(f"{e}, Unable to fetch predictions data.")
    else:
        # Stringify the promise to data
        data = response.json()
        return data


def mock_fetch_predictions_data():
    return {
        "data": [
            {
                "attributes": {
                    "arrival_time": "2023-07-18T22:58:28-04:00",
                    "departure_time": "2023-07-18T21:59:25-04:00",
                    "direction_id": 0,
                    "schedule_relationship": "ADDED",
                    "status": "FIRE",
                    "stop_sequence": 40,
                },
                "id": "prediction-ADDED-1581584541-70069-40",
                "relationships": {
                    "route": {"data": {"id": "Red", "type": "route"}},
                    "stop": {"data": {"id": "70069", "type": "stop"}},
                    "trip": {"data": {"id": "ADDED-1581584541", "type": "trip"}},
                    "vehicle": {"data": {"id": "R-5477AEE4", "type": "vehicle"}},
                },
                "type": "prediction",
            },
            {
                "attributes": {
                    "arrival_time": "2023-07-18T22:05:57-04:00",
                    "departure_time": "2023-07-18T22:06:54-04:00",
                    "direction_id": 0,
                    "schedule_relationship": None,
                    "status": None,
                    "stop_sequence": 40,
                },
                "id": "prediction-57599385-70069-40",
                "relationships": {
                    "route": {"data": {"id": "Red", "type": "route"}},
                    "stop": {"data": {"id": "70069", "type": "stop"}},
                    "trip": {"data": {"id": "57599385", "type": "trip"}},
                    "vehicle": {"data": {"id": "R-5477AF12", "type": "vehicle"}},
                },
                "type": "prediction",
            },
        ],
        "jsonapi": {"version": "1.0"},
        "links": {
            "first": "https://api-v3.mbta.com/predictions?filter[direction_id]=0&filter[stop]=place-cntsq&page[limit]=2&page[offset]=0",
            "last": "https://api-v3.mbta.com/predictions?filter[direction_id]=0&filter[stop]=place-cntsq&page[limit]=2&page[offset]=6",
            "next": "https://api-v3.mbta.com/predictions?filter[direction_id]=0&filter[stop]=place-cntsq&page[limit]=2&page[offset]=2",
        },
    }


def fetch_vehicles_data(id: str):
    try:
        # Fetch
        response = requests.get(
            url=f"https://api-v3.mbta.com/vehicles/{id}",
            headers=headers,
            auth=None,
        )
    except Exception as e:
        display_error(["ERROR : ", "Unable to", "fetch vehicle", "data"])
        print(f"{e}, Unable to fetch vehicle data.")
    else:
        # Stringify the promise to data
        data = response.json()
        return data


def mock_fetch_vehicles_data():
    return {
        "data": {
            "attributes": {"current_status": "IN_TRANSIT_TO"},
            "id": "R-5477B048",
            "links": {"self": "/vehicles/R-5477B048"},
            "relationships": {
                "route": {"data": {"id": "Red", "type": "route"}},
                "stop": {"data": {"id": "70063", "type": "stop"}},
                "trip": {"data": {"id": "ADDED-1581584581", "type": "trip"}},
            },
            "type": "vehicle",
        },
        "jsonapi": {"version": "1.0"},
    }


def get_arrival_times(stop: str, direction: int, limit: int):
    data = fetch_predictions_data(stop, direction, limit)
    # data = mock_fetch_predictions_data()

    currTime = datetime.datetime.now()
    arrivalTimes = []

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
            arrivalTimes.append(prediction_status)
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

        # If seconds < 0
        # Do not display this prediction, since the vehicle has already left the stop
        if seconds < 0:
            continue

        # If seconds <= 90, and the `status` of the associated `vehicle` is "STOPPED_AT", and the vehicle’s `stop` is the same as the prediction’s `stop`:
        # Display "Boarding" (abbrev. "BRD")
        if seconds <= 90:
            vehicle_data = fetch_vehicles_data(prediction_vehicle_id)["data"]
            if (
                vehicle_data["attributes"]["current_status"] == "STOPPED_AT"
                and vehicle_data["relationships"]["stop"] == prediction_stop_id
            ):
                arrivalTimes.append("Boarding")

        # If seconds is <= 30
        # Display "Arriving" (abbrev. "ARR")
        if seconds <= 30:
            arrivalTimes.append("Arriving")

        # If seconds is <= 60
        # Display "Approaching" (abbrev. "1 min")
        if seconds <= 60:
            arrivalTimes.append("1 min")

        # Round the seconds value to the nearest whole number of minutes, rounding up if exactly in-between.
        minutes = round(seconds / 60)

        # If minutes > 20
        # Display “20+ minutes” (abbrev. “20+ min”)
        if minutes > 20:
            arrivalTimes.append("20+ minutes")

        arrivalTimes.append(str(minutes) + "min")
    return arrivalTimes


def print_text(lines):
    """Update the display with this, return immediatly"""

    # lines: List[str] = ["Hello World,", "how are you?"]

    pixels = copy.deepcopy(state.BACKGROUND)

    pixels = draw_text(pixels=pixels, lines=lines)

    state.display.display_matrix(pixels)


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
limit: Number of next "x" arrival times you want to see. Should be 2 to fit into the board.
"""


def display_train_arrival_times(
    begin_time=datetime.datetime.now(), display_inbound=True
):
    curr_time = datetime.datetime.now()
    # Flip between Inbound and Outbound every 10 seconds
    print('curr_time : ', curr_time)
    print('begin_time : ', begin_time)
    print('display_inbound : ', display_inbound)
    print('Time to flip : ', (curr_time - begin_time).total_seconds() > 10)
    # if (curr_time - begin_time).total_seconds() > 10:
    #     begin_time = curr_time
    #     display_inbound = display_inbound ^ 1
    if display_inbound:
        arrival_time_inbound = get_arrival_times("place-cntsq", 0, 4)
        lines_inbound = [
                "    Central SQ.",
                "Outbound",
                f"{arrival_time_inbound[0]}",
                f"{arrival_time_inbound[1]}",
            ]
        print_text(lines=lines_inbound)
    else:
        arrival_time_outbound = get_arrival_times("place-cntsq", 1, 4)
        lines_outbound = [
                "    Central SQ.",
                "Outbound",
                f"{arrival_time_outbound[0]}",
                f"{arrival_time_outbound[1]}",
            ]
        print_text(lines=lines_outbound)
