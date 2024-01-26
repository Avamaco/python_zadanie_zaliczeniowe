import json
import os
import bus_speed


# This checks if the loaded data doesn't have any obvious mistakes.
def data_makes_sense(this_reading, prev_reading):
    if this_reading == prev_reading:
        return False
    if bus_speed.calc_speed(this_reading, prev_reading) > 100:
        return False
    return True


def find_bus_routes(day):
    dir_path = os.path.join('collected_data', day)
    if not os.path.exists(dir_path):
        print("Directory " + dir_path + "does not exist.")
        return
    bus_routes = {}
    for file_name in os.listdir(dir_path):
        in_file = open(os.path.join(dir_path, file_name), 'r')
        data = json.load(in_file)['result']
        in_file.close()
        if not isinstance(data, list):
            continue
        for bus in data:
            key = (bus['VehicleNumber'])
            value = {'Lines': bus['Lines'], 'Time': bus['Time'], 'Lat': bus['Lat'], 'Lon': bus['Lon']}
            modified_route = bus_routes.setdefault(key, [])
            if not modified_route or data_makes_sense(modified_route[-1], value):
                modified_route.append(value)

    out_dir = 'processed_data'
    os.makedirs(out_dir, exist_ok=True)
    out_file_path = os.path.join(out_dir, day + ".json")
    out_file = open(out_file_path, 'w')
    json.dump(bus_routes, out_file)
    out_file.close()


if __name__ == '__main__':
    find_bus_routes('2024-01-22')
