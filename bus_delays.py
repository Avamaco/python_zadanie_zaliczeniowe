import os
import time
import json
import datetime

import pandas
from api_data_collector import download_timetable


MIN_DELAY = -60
MAX_DELAY = 1200


def timetable_missing(busstop_id, busstop_nr, line):
    file_name = busstop_id + '_' + busstop_nr + '_' + line + '.json'
    path = os.path.join("collected_data", "timetables", file_name)
    if not os.path.exists(path):
        return True
    file = open(path, "r")
    if len(file.read()) < 25:
        file.close()
        return True
    file.close()
    return False


def download_required_timetables(df):
    data = df.values.tolist()
    print("Downloading " + str(len(data)) + " timetables...")
    print("%06d" % 0, end="")
    i = 1
    for arrival in data:
        busstop_id, busstop_nr, line = arrival[0], str(arrival[1]).zfill(2), arrival[2]
        if timetable_missing(busstop_id, busstop_nr, line):
            download_timetable(busstop_id, busstop_nr, line)
            time.sleep(1)
        print("\b\b\b\b\b\b", end="")
        print("%06d" % i, end="")
        i += 1


def get_arrivals():
    in_path = os.path.join("processed_data", "arrivals-2024-01-30.csv")
    df = pandas.read_csv(in_path)
    return df


def get_times(busstop_id, busstop_nr, line):
    file_name = busstop_id + "_" + busstop_nr + "_" + line + ".json"
    in_file_path = os.path.join("collected_data", "timetables", file_name)
    if not os.path.exists(in_file_path):
        return None
    in_file = open(in_file_path, 'r')
    json_data = json.load(in_file)
    in_file.close()
    return [elem["values"][5]["value"] for elem in json_data["result"]]


def find_delay(bus_time, timetable):
    time1 = datetime.datetime.fromisoformat(bus_time)
    day = bus_time[:11]
    for i in reversed(range(len(timetable))):
        if int(timetable[i][:2]) > 23:
            timetable[i] = str(int(timetable[i][:2]) - 24).zfill(2) + timetable[i][2:]
        time2 = datetime.datetime.fromisoformat(day + timetable[i])
        delay = (time1 - time2).total_seconds()
        if delay > MIN_DELAY:
            return delay
    return MIN_DELAY - 1


def find_all_delays(df):
    df["Delay"] = [find_delay(bus_time, get_times(busstop_id, str(busstop_nr).zfill(2), line))
                   for busstop_id, busstop_nr, line, bus_time
                   in df.values.tolist()]
    return df.loc[df["Delay"] < MAX_DELAY].loc[df["Delay"] > MIN_DELAY]


if __name__ == "__main__":
    arrivals = get_arrivals()
    #download_required_timetables(arrivals)
    arrivals = find_all_delays(arrivals)
    print(arrivals)
    print(arrivals["Delay"].median())
