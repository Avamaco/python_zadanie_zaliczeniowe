import pandas
import os
import bus_speed
from ast import literal_eval


def arrived(df):
    dist = [tup[1] for tup in df["ClosestStop"]]
    return [x < 15 for x in dist]


def get_arriving_buses():
    in_path = os.path.join("processed_data", "dist-2024-01-30.csv")
    df = pandas.read_csv(in_path)
    df["ClosestStop"] = [literal_eval(s) for s in df["ClosestStop"]]
    bus_speed.calc_all(df)
    df = bus_speed.cut_incorrect_speed(df)
    df = df.loc[df["Speed"] > 1]
    df = df.loc[arrived(df)]
    return df


def save_arrivals(df):
    data = {
        "BusstopId": [tup[0][0] for tup in df["ClosestStop"]],
        "BusstopNr": [tup[0][1] for tup in df["ClosestStop"]],
        "Line": df["Lines"],
        "Time": df["Time"]
    }
    to_save = pandas.DataFrame(data)
    out_path = os.path.join("processed_data", "arrivals-2024-01-30.csv")
    to_save.to_csv(out_path, index=False)


if __name__ == "__main__":
    df = get_arriving_buses()
    save_arrivals(df)
