import json
import os
import datetime
from dotenv import load_dotenv
import requests
from stations import STATIONS

URL = os.getenv("URL")


def get_current_time() -> dict:  # validated
    today = datetime.date.today()
    this_time = datetime.datetime.now()

    return {
        "date": today.strftime("%Y-%m-%d"),
        "hour": this_time.strftime("%H:%M"),
        "request_time": this_time,
    }


def get_trains(URL, from_id: str, to_id: str, time):
    # URL = https://israelrail.azurefd.net/rjpa-prod/api/v1/timetable/searchTrainLuzForDateTime?fromStation=1400&toStation=4600&date=2023-03-22&hour=08:45&scheduleType=1&systemType=2&languageId=Hebrew
    try:
        params = {
            "fromStation": from_id,
            "toStation": to_id,
            "date": time["date"],
            "hour": time["hour"],
            "scheduleType": 1,
            "systemType": 2,
            "languageId": "hebrew",
        }
        headers = {"ocp-apim-subscription-key": "4b0d355121fe4e0bb3d86e902efe9f20"}
        r = requests.get(URL, params=params, headers=headers)
    except requests.HTTPError:
        return {"error": "Something went wrong with the API"}
    return r.json()


def clean_payload(payload) -> list:
    cleaned_trains_data = []
    travels = payload["result"]["travels"]  # list of trains + metadata
    for travel in travels:
        cleaned_trains_data.append(
            {
                "departureTime": travel["departureTime"],
                "arrivalTime": travel["arrivalTime"],
            }
        )
    return cleaned_trains_data


def create_time_window(clean_payload, requested_time, current_time):
    pass


def slice_relevant_trains(
    trains, request_time: datetime, time_period: int = 3, max_trains: int = 3
):
    filtered_trains = []
    for train in trains:
        if len(filtered_trains) >= max_trains:
            break
            # TODO: fix types
        parsed_train_time = datetime.datetime.strptime(
            train["departureTime"], "%Y-%m-%dT%H:%M:%S"
        )
        time_delta = datetime.timedelta(hours=time_period)
        if parsed_train_time - request_time <= time_delta:
            filtered_trains.append(train)
    return filtered_trains


def convert_train_data_to_message(train_data) -> str:
    if len(train_data) == 0:
        return "There are no trains in the near time (Is it Shabat today?)"
    message_string = "The next trains from Home to Work are :\n"
    for train in train_data:
        message = f"Departure : {train['departureTime']}\n"
        message_string += message

    return message_string


def handle_get_current_trains(URL, mode: str, time_slice=None, units=None) -> str:
    match mode:
        case "toWork":
            time = get_current_time()
            payload = get_trains(URL, STATIONS["home"], STATIONS["work"], time=time)
            train_data = clean_payload(payload)
            trains_in_time_window = slice_relevant_trains(
                train_data, time["request_time"]
            )
            message = convert_train_data_to_message(trains_in_time_window)
            return message
        case "toHome":
            time = get_current_time()
            payload = get_trains(URL, STATIONS["work"], STATIONS["home"], time=time)
            train_data = clean_payload(payload)
            trains_in_time_window = slice_relevant_trains(
                train_data, time["request_time"]
            )
            message = convert_train_data_to_message(train_data)
            return message


if __name__ == "__main__":
    load_dotenv(".dev.env")
    URL = os.getenv("URL")

    # trains = get_trains(URL, "1400", "4600", {"date": "2023-03-26", "hour": "08:00"})
    # with open("./example.json", "w") as filename:
    #     filename.write(json.dumps(trains))
    # print(trains)
    print(handle_get_current_trains(URL, "toWork"))
