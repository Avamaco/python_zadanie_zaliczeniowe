import pandas
import os
from bus_speed import speed
from ast import literal_eval


def arrived(df):
    dist = [tup[1] for tup in df["ClosestStop"]]
    return [x < 15 for x in dist]


def get_arriving_buses(file_name):
    in_path = os.path.join("../processed_data", "dist-" + file_name + ".csv")
    df = pandas.read_csv(in_path)
    df["ClosestStop"] = [literal_eval(s) for s in df["ClosestStop"]]
    speed.calc_all(df)
    df = speed.cut_incorrect_speed(df)
    df = df.loc[df["Speed"] > 1]
    df = df.loc[arrived(df)]
    return df


def save_arrivals(df, file_name):
    data_dict = {
        "BusstopId": [tup[0][0] for tup in df["ClosestStop"]],
        "BusstopNr": [tup[0][1] for tup in df["ClosestStop"]],
        "Line": df["Lines"],
        "Time": df["Time"]
    }
    to_save = pandas.DataFrame(data_dict)
    out_path = os.path.join("../processed_data", "arrivals-" + file_name + ".csv")
    to_save.to_csv(out_path, index=False)


if __name__ == "__main__":
    data = get_arriving_buses("2024-01-30")
    save_arrivals(data, "2024-01-30")
