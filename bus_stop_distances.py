import json
import pandas
import os


def get_bus_stop_dataframe():
    in_file_path = os.path.join("collected_data", "bus_stops.json")
    in_file = open(in_file_path, 'r')
    json_data = json.load(in_file)
    in_file.close()
    data_list = []
    for el in json_data["result"]:
        data_list.append([el["values"][0]["value"],
                          el["values"][1]["value"],
                          el["values"][4]["value"],
                          el["values"][5]["value"]])
    return pandas.DataFrame(data_list, columns=["GroupId", "StopId", "Lat", "Lon"])


def get_bus_line_route_dataframes():
    in_file_path = os.path.join("collected_data", "bus_line_routes.json")
    in_file = open(in_file_path, 'r')
    json_data = json.load(in_file)
    in_file.close()
    data_dict = {}
    for line in json_data["result"].keys():
        routes = json_data["result"][line]
        stops_set = set()
        for r in routes.values():
            for s in r.values():
                stops_set.add((s["nr_zespolu"], s["nr_przystanku"]))
        data_dict[line] = pandas.DataFrame(list(stops_set), columns=["GroupId", "StopId"])
    return data_dict


if __name__ == "__main__":
    print(get_bus_stop_dataframe())
    print(get_bus_line_route_dataframes()["504"])
