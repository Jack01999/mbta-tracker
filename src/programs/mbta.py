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

def fetch_data(stop: str, direction: int, limit: int):
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
        print(f"{e}, Unable to fetch data.")
    else:
        # Stringify the promise to data
        data = response.json()
        return data
    
def mock_fetch_data():
    return {'data': [{'attributes': {'arrival_time': '2023-07-18T22:58:28-04:00', 'departure_time': '2023-07-18T21:59:25-04:00', 'direction_id': 0, 'schedule_relationship': 'ADDED', 'status': None, 'stop_sequence': 40}, 'id': 'prediction-ADDED-1581584541-70069-40', 'relationships': {'route': {'data': {'id': 'Red', 'type': 'route'}}, 'stop': {'data': {'id': '70069', 'type': 'stop'}}, 'trip': {'data': {'id': 'ADDED-1581584541', 'type': 'trip'}}, 'vehicle': {'data': {'id': 'R-5477AEE4', 'type': 'vehicle'}}}, 'type': 'prediction'}, {'attributes': {'arrival_time': '2023-07-18T22:05:57-04:00', 'departure_time': '2023-07-18T22:06:54-04:00', 'direction_id': 0, 'schedule_relationship': None, 'status': None, 'stop_sequence': 40}, 'id': 'prediction-57599385-70069-40', 'relationships': {'route': {'data': {'id': 'Red', 'type': 'route'}}, 'stop': {'data': {'id': '70069', 'type': 'stop'}}, 'trip': {'data': {'id': '57599385', 'type': 'trip'}}, 'vehicle': {'data': {'id': 'R-5477AF12', 'type': 'vehicle'}}}, 'type': 'prediction'}], 'jsonapi': {'version': '1.0'}, 'links': {'first': 'https://api-v3.mbta.com/predictions?filter[direction_id]=0&filter[stop]=place-cntsq&page[limit]=2&page[offset]=0', 'last': 'https://api-v3.mbta.com/predictions?filter[direction_id]=0&filter[stop]=place-cntsq&page[limit]=2&page[offset]=6', 'next': 'https://api-v3.mbta.com/predictions?filter[direction_id]=0&filter[stop]=place-cntsq&page[limit]=2&page[offset]=2'}}

def get_arrival_times(stop: str, direction: int, limit: int):
    #data = fetch_data(stop, direction, limit)
    data = mock_fetch_data()

    # We don't need to worry about 'null' data for the arrival_time because the station we're predicting is not a 'first stop' station
    # If there is something wrong, we can use the 'schedule_relationship' field to figure out why.
    print('data : ', data)
    # Get current time
    currTime = datetime.datetime.now()
    arrivalTimes = []
    for stop in data["data"]:
        # If `status` is non-null:
	    # Display this value as-is
        if stop.status is not None:
            print('There is a status')
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


def display_train_arrival_times(
    begin_time=datetime.datetime.now(), display_inbound=True
):
    curr_time = datetime.datetime.now()
    # Flip between Inbound and Outbound every 10 seconds
    if (curr_time - begin_time).total_seconds() > 10:
        begin_time = curr_time
        display_inbound = display_inbound ^ 1
    if display_inbound:
        arrival_time_inbound = get_arrival_times("place-cntsq", 0, 2)
        lines_inbound = [
            "    Central SQ.",
            "Inbound",
            f"{arrival_time_inbound[0]}",
            f"{arrival_time_inbound[1]}",
        ]
        print_text(lines=lines_inbound)
    else:
        arrival_time_outbound = get_arrival_times("place-cntsq", 1, 2)
        lines_outbound = [
            "    Central SQ.",
            "Outbound",
            f"{arrival_time_outbound[0]}",
            f"{arrival_time_outbound[1]}",
        ]
        print_text(lines=lines_outbound)
