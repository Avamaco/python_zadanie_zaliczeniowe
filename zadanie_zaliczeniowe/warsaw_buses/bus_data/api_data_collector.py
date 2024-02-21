import time
import requests
import os
import datetime
import json
import csv


def write_to_file(directory_path, file_name, text):
    os.makedirs(directory_path, exist_ok=True)
    out_file_path = os.path.join(directory_path, file_name)
    out_file = open(out_file_path, 'w')
    out_file.write(text)
    out_file.close()


def write_csv(directory_path, file_name, json_text):
    data = json.loads(json_text)["result"]
    if not isinstance(data, list) or not data:
        return
    os.makedirs(directory_path, exist_ok=True)
    out_file_path = os.path.join(directory_path, file_name)
    out_file = open(out_file_path, 'w', newline='')
    writer = csv.writer(out_file)
    writer.writerow(data[0].keys())
    for d in data:
        writer.writerow(d.values())
    out_file.close()


def download_online_data():
    payload = {'resource_id': 'f2e5503e-927d-4ad3-9500-4ab9e55deb59',
               'apikey': '9d0f0f07-df51-4744-af50-a758edde8a00',
               'type': '1'}
    response = requests.get('https://api.um.warszawa.pl/api/action/busestrams_get', params=payload)
    current_datetime = str(datetime.datetime.now())
    dir_name = '../../../collected_data'
    subdir_name = current_datetime[:10]                                          # YYYY-MM-DD
    file_name = current_datetime[11:19].replace(':', '-') + ".csv"  # hh-mm-ss.csv
    write_csv(os.path.join(dir_name, subdir_name), file_name, response.text)


def download_bus_stop_positions():
    payload = {'id': 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3',
               'apikey': '9d0f0f07-df51-4744-af50-a758edde8a00'}
    response = requests.get('https://api.um.warszawa.pl/api/action/dbstore_get/?', params=payload)
    dir_name = '../../../collected_data'
    file_name = 'bus_stops.json'
    write_to_file(dir_name, file_name, response.text)


def download_bus_routes():
    payload = {'apikey': '9d0f0f07-df51-4744-af50-a758edde8a00'}
    response = requests.get('https://api.um.warszawa.pl/api/action/public_transport_routes/?', params=payload)
    dir_name = '../../../collected_data'
    file_name = 'bus_line_routes.json'
    write_to_file(dir_name, file_name, response.text)


def download_timetable(busstop_id, busstop_nr, line):
    payload = {'apikey': '9d0f0f07-df51-4744-af50-a758edde8a00',
               'id': 'e923fa0e-d96c-43f9-ae6e-60518c9f3238',
               'busstopId': busstop_id,
               'busstopNr': busstop_nr,
               'line': line}
    response = requests.get('https://api.um.warszawa.pl/api/action/dbtimetable_get/?', params=payload)
    dir_name = '../../../collected_data'
    subdir_name = 'timetables'
    file_name = busstop_id + '_' + busstop_nr + '_' + line + '.json'
    write_to_file(os.path.join(dir_name, subdir_name), file_name, response.text)


def collect_online(how_much, delay):
    print("Downloading online data " + str(how_much) + " times....")
    print("%06d" % 0, end="")
    for i in range(how_much):
        download_online_data()
        print("\b\b\b\b\b\b", end="")
        print("%06d" % (i + 1), end="")
        time.sleep(delay)
    print("\nFinished!")


if __name__ == "__main__":
    collect_online(120, 30)
