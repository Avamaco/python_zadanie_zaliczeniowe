import os
import pandas


def combine_into_df(day, first_reading, last_reading):
    dir_path = os.path.join('collected_data', day)
    if not os.path.exists(dir_path):
        print("Directory " + dir_path + "does not exist.")
        return
    file_names = os.listdir(dir_path)
    file_names.sort()
    if first_reading not in file_names or last_reading not in file_names:
        print("Specified reading does not exist.")
        return
    first_index = file_names.index(first_reading)
    last_index = file_names.index(last_reading)
    df_list = []
    timeframe = file_names[first_index:last_index+1]
    for reading in timeframe:
        df_list.append(pandas.read_csv(os.path.join(dir_path, reading), header=0))
    result = pandas.concat(df_list)
    return result.drop_duplicates().sort_values(by=["VehicleNumber", "Time"])
