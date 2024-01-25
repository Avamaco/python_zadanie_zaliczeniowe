import os
import json
import numpy
import bus_speed


def print_basic_statistics(data, stat):
    stat_list = []
    for key, value in data.items():
        for snapshot in value:
            if stat in snapshot.keys():
                stat_list.append(snapshot[stat])

    arr = numpy.array(stat_list)
    print("Basic statistics for " + stat + ": ")
    print("Min: " + str(arr.min()))
    print("10th centile: " + str(numpy.quantile(arr, 0.1)))
    print("Q1: " + str(numpy.quantile(arr, 0.25)))
    print("Median: " + str(numpy.quantile(arr, 0.5)))
    print("Q3: " + str(numpy.quantile(arr, 0.75)))
    print("90th centile: " + str(numpy.quantile(arr, 0.9)))
    print("Max: " + str(arr.max()))
    print("Std: " + str(numpy.std(arr)))


if __name__ == '__main__':
    some_data = bus_speed.calc_all_speeds("2024-01-22")
    print_basic_statistics(some_data, "Lon")
