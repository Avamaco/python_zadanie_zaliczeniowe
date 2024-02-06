import json
import os
from geopy import distance
import datetime
import pandas


def seconds_passed(time1, time2):
    time1 = datetime.datetime.fromisoformat(time1)
    time2 = datetime.datetime.fromisoformat(time2)
    time_delta = time2 - time1
    return time_delta.total_seconds()


def dist_in_meters(lat1, lon1, lat2, lon2):
    return distance.distance((lat1, lon1), (lat2, lon2)).meters


def speed_in_kmh(meters, seconds):
    return meters / seconds * 3.6


def calc_seconds_passed(df):
    return [seconds_passed(t2, t1) for t1, t2 in zip(df.Time, df.Time.shift(fill_value="2000-01-01 08:00:00"))]


def calc_dist(df):
    return [dist_in_meters(lat1, lon1, lat2, lon2)
            for lat1, lon1, lat2, lon2
            in zip(df.Lat, df.Lon, df.Lat.shift(fill_value=0), df.Lon.shift(fill_value=0))]


def calc_speed(df):
    return speed_in_kmh(df.MetersPassed, df.SecondsPassed)


def calc_all(df):
    df["SecondsPassed"] = calc_seconds_passed(df)
    df["MetersPassed"] = calc_dist(df)
    df["Speed"] = calc_speed(df)


def is_speed_correct(df):
    return ((df["VehicleNumber"] == df["VehicleNumber"].shift())
            & (df["Speed"] <= 100)
            & (df["SecondsPassed"] <= 150))


def cut_incorrect_speed(df):
    return df.loc[is_speed_correct(df)]
