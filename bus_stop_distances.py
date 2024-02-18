import json
from geopy import distance
import pandas
import os

import create_dataframe


def get_bus_stop_dict():
    in_file_path = os.path.join("collected_data", "bus_stops.json")
    in_file = open(in_file_path, 'r')
    json_data = json.load(in_file)
    in_file.close()
    data_dict = {}
    for el in json_data["result"]:
        data_dict[(el["values"][0]["value"], el["values"][1]["value"])] = \
            (float(el["values"][4]["value"]), float(el["values"][5]["value"]))
    return data_dict


def get_route_lists():
    in_file_path = os.path.join("collected_data", "bus_line_routes.json")
    in_file = open(in_file_path, 'r')
    json_data = json.load(in_file)
    in_file.close()
    data_dict = {}
    for line in json_data["result"].keys():
        routes = json_data["result"][line]
        routes_list = []
        for r in routes.values():
            if len(r) < 3:
                continue
            stops_list = []
            for s in r.values():
                stops_list.append((s["nr_zespolu"], s["nr_przystanku"]))
            routes_list.append(stops_list)
        data_dict[line] = routes_list
    return data_dict


def get_closest_stops(lat, lon, line, bus_lists, stop_pos):
    if line not in bus_lists.keys():
        return None
    line_lists = bus_lists[line]
    distances = [[distance.distance(stop_pos[s], (lat, lon)).meters for s in route] for route in line_lists]
    closest_ids = [min(range(len(route) - 1), key=route.__getitem__) for route in distances]
    return [((line_lists[i][closest_ids[i]], distances[i][closest_ids[i]]),
             (line_lists[i][closest_ids[i] + 1], distances[i][closest_ids[i] + 1])) for i in range(len(line_lists))]


def predict_closest_stop(new_stops, old_stops):
    if new_stops is None or old_stops is None or len(old_stops) != len(new_stops):
        return None
    for i in range(len(new_stops)):
        if new_stops[i][0][0] == old_stops[i][1][0]:  # old next stop is now the closest
            return new_stops[i][0]
    for i in range(len(new_stops)):
        if new_stops[i][1][0] == old_stops[i][1][0] and new_stops[i][1][1] < old_stops[i][1][1]:  # next stop is closer
            return new_stops[i][0]
    return None  # cannot predict the closest stop


def df_closest_stop(df):
    stops = get_bus_stop_dict()
    routes = get_route_lists()
    close_stops = pandas.Series([get_closest_stops(lat, lon, line, routes, stops)
                                 for lat, lon, line in zip(df["Lat"], df["Lon"], df["Lines"])])
    df["ClosestStop"] = [predict_closest_stop(new_stops, old_stops) if new_bus == old_bus else None
                         for new_stops, old_stops, new_bus, old_bus
                         in zip(close_stops, close_stops.shift(), df["VehicleNumber"], df["VehicleNumber"].shift())]
    return df


if __name__ == "__main__":
    morning = create_dataframe.combine_into_df("2024-01-30", "10-00-07.csv", "11-00-59.csv")
    print(len(morning))
    closest_bus_stops = df_closest_stop(morning).dropna()
    print(len(closest_bus_stops))
    out_path = os.path.join("processed_data", "dist-2024-01-30.csv")
    closest_bus_stops.to_csv(out_path)
