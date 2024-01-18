import json
import os

in_file = open(os.path.join('collected_data', 'bus.json'), 'r')
data = json.load(in_file)
in_file.close()
buses = data['result']
for b in buses:
    if b['Lines'] == '504':
        print(b)
