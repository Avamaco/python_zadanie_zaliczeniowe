import requests
import os
import datetime


def download_online_data():
    payload = {'resource_id': 'f2e5503e-927d-4ad3-9500-4ab9e55deb59',
               'apikey': '9d0f0f07-df51-4744-af50-a758edde8a00',
               'type': '1'}
    response = requests.get('https://api.um.warszawa.pl/api/action/busestrams_get', params=payload)
    current_datetime = str(datetime.datetime.now())
    dir_name = 'collected_data'
    subdir_name = current_datetime[:10]        # YYYY-MM-DD
    file_name = current_datetime[11:19].replace(':', '-') + ".json"  # hh-mm-ss.json
    if not os.path.exists(os.path.join(dir_name, subdir_name)):
        os.makedirs(os.path.join(dir_name, subdir_name))
    out_file_path = os.path.join(dir_name, subdir_name, file_name)
    out_file = open(out_file_path, 'w')
    out_file.write(response.text)
    out_file.close()


if __name__ == "__main__":
    download_online_data()
