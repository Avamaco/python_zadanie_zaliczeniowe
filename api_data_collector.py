import requests
import os

payload = {'resource_id': 'f2e5503e-927d-4ad3-9500-4ab9e55deb59',
           'apikey': '9d0f0f07-df51-4744-af50-a758edde8a00',
           'type': '1'}
response = requests.get('https://api.um.warszawa.pl/api/action/busestrams_get', params=payload)
dir_name = 'collected_data'
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
out_file_path = os.path.join(dir_name, 'bus.json')
out_file = open(out_file_path, 'w')
out_file.write(response.text)
out_file.close()
