import os
import time

import pandas
from api_data_collector import download_timetable


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


if __name__ == "__main__":
    arrivals = get_arrivals()
    download_required_timetables(arrivals)
