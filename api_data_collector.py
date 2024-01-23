import requests
import os
import datetime


def write_to_file(directory_path, file_name, text):
    os.makedirs(directory_path, exist_ok=True)
    out_file_path = os.path.join(directory_path, file_name)
    out_file = open(out_file_path, 'w')
    out_file.write(text)
    out_file.close()


def download_online_data():
    payload = {'resource_id': 'f2e5503e-927d-4ad3-9500-4ab9e55deb59',
               'apikey': '9d0f0f07-df51-4744-af50-a758edde8a00',
               'type': '1'}
    response = requests.get('https://api.um.warszawa.pl/api/action/busestrams_get', params=payload)
    current_datetime = str(datetime.datetime.now())
    dir_name = 'collected_data'
    subdir_name = current_datetime[:10]                                          # YYYY-MM-DD
    file_name = current_datetime[11:19].replace(':', '-') + ".json"  # hh-mm-ss.json
    write_to_file(os.path.join(dir_name, subdir_name), file_name, response.text)


def download_bus_stop_positions():
    payload = {'id': 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3',
               'apikey': '9d0f0f07-df51-4744-af50-a758edde8a00'}
    response = requests.get('https://api.um.warszawa.pl/api/action/dbstore_get/?', params=payload)
    dir_name = 'collected_data'
    file_name = 'bus_stops.json'
    write_to_file(dir_name, file_name, response.text)


def download_bus_routes():
    payload = {'apikey': '9d0f0f07-df51-4744-af50-a758edde8a00'}
    response = requests.get('https://api.um.warszawa.pl/api/action/public_transport_routes/?', params=payload)
    dir_name = 'collected_data'
    file_name = 'bus_line_routes.json'
    write_to_file(dir_name, file_name, response.text)


def download_timetable(busstop_id, busstop_nr, line):
    payload = {'apikey': '9d0f0f07-df51-4744-af50-a758edde8a00',
               'id': 'e923fa0e-d96c-43f9-ae6e-60518c9f3238',
               'busstopId': busstop_id,
               'busstopNr': busstop_nr,
               'line': line}
    response = requests.get('https://api.um.warszawa.pl/api/action/dbtimetable_get/?', params=payload)
    dir_name = 'collected_data'
    subdir_name = 'timetables'
    file_name = busstop_id + '_' + busstop_nr + '_' + line + '.json'
    write_to_file(os.path.join(dir_name, subdir_name), file_name, response.text)


if __name__ == "__main__":
    download_timetable('3134', '01', '504')
