import json
import os
from geopy import distance
import datetime


def calc_speed(bus_data1, bus_data2):
    pos1 = (float(bus_data1['Lat']), float(bus_data1['Lon']))
    pos2 = (float(bus_data2['Lat']), float(bus_data2['Lon']))
    time1 = datetime.datetime.fromisoformat(bus_data1['Time'])
    time2 = datetime.datetime.fromisoformat(bus_data2['Time'])
    time_delta = time2 - time1
    seconds = time_delta.total_seconds()
    meters = distance.distance(pos1, pos2).meters
    mps = meters / seconds
    return mps * 3.6       # m/s to km/h


def calc_all_speeds(day):
    file_path = os.path.join('processed_data', day + '.json')
    if not os.path.exists(file_path):
        print("File " + file_path + "does not exist.")
        return
    in_file = open(file_path, 'r')
    data = json.load(in_file)
    in_file.close()
    for key, value in data.items():
        for i in range(len(value) - 1):
            speed = calc_speed(value[i], value[i + 1])
            value[i]['Speed'] = speed
    return data


some_data = calc_all_speeds('2024-01-22')
for b in some_data['1508']:
    print(b.get('Speed'))
