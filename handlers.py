import datetime
import requests

def get_current_time() -> dict:  # validated
    today = datetime.date.today()
    this_time = datetime.datetime.now()

    return {
        "date": today.strftime("%Y%m%d"),
        "hour": this_time.strftime("%H%M"),
        "request_time": this_time,
    } 


def get_trains(from_id: str, to_id: str, time):
    try:
        r = requests.get(
            f"https://www.rail.co.il/apiinfo/api/Plan/GetRoutes?OId={from_id}&TId={to_id}&Date={time['date']}&Hour={time['hour']}&isGoing=true"
        )
    except requests.HTTPError:
        return {"error": "Something went wrong with the API"}
    return r.json()


def get_basic_train_info(train_payload):  # Validated. TODO: handle no trains available
    trains_today_data = train_payload["Data"]["Routes"]

    trains = []
    for train in trains_today_data:
        actual_data = train["Train"][0]
        trains.append(
            {
                "DepartureTime": actual_data["DepartureTime"],
                "ArrivalTime": actual_data["ArrivalTime"],
                "Late": False,
            }
        )

    return trains


def slice_relevant_trains(
    trains, request_time, time_period: int = None, max_trains: int = 3
):
    filtered_trains = []
    for train in trains:
        if len(filtered_trains) > max_trains:
            break
        # TODO: fix types
        if train["DepartureTime"] <= request_time["request_time"] + time_period:
            filtered_trains.append(train)
    return filtered_trains


def convert_station_to_id(station: str) -> int:
    return STATIONS[station]


def convert_train_data_to_message(train_data):
    if len(train_data) == 0:
        return "There are no trains in the near time (Is it Shabat today?)"
    message_string = "The next trains from Home to Work are :\n"
    for train in train_data:
        message = f"Departure : {train['DepartureTime']}\n"
        message_string += message

    return message_string


def handle_get_current_trains(mode):
    match mode:
        case "toWork":
            time = get_current_time()
            payload = get_trains("1400", "4600", time=time)
            train_data = get_basic_train_info(payload)
            message = convert_train_data_to_message(train_data)
            return message
        case "toHome":
            time = get_current_time()
            payload = get_trains("4600", "1400", time=time)
            train_data = get_basic_train_info(payload)
            message = convert_train_data_to_message(train_data)
            return message


if __name__ == "__main__":
    # r = requests.get(
    #     "https://www.rail.co.il/apiinfo/api/Plan/GetRoutes?OId=1400&TId=4600&Date=20230129&Hour=1000&isGoing=true&c=1674968266239"
    # )
    # with open("example.json", "wb") as f:
    #     for chunk in r.iter_content(chunk_size=128):
    #         f.write(chunk)
    time = get_current_time()
    payload = get_trains("1400", "4600", time=time)
    proccessed_payload = get_basic_train_info(payload)
    print(proccessed_payload)
