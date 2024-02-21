from zadanie_zaliczeniowe.warsaw_buses.bus_data import create_dataframe
from zadanie_zaliczeniowe.warsaw_buses.bus_speed import speed
import plotly.express as px
import pandas


def read_and_calc_data(day, first_reading, last_reading):
    df = create_dataframe.combine_into_df(day, first_reading, last_reading)
    speed.calc_all(df)
    return speed.cut_incorrect_speed(df)


def show_speed_map(speed_data):
    lat_median = speed_data["Lat"].median()
    lon_median = speed_data["Lon"].median()
    fig = px.density_mapbox(speed_data.loc[speed_data["Speed"] > 50], lat='Lat', lon='Lon', z='Speed', radius=10,
                            center=dict(lat=lat_median, lon=lon_median), zoom=10,
                            mapbox_style="open-street-map")
    fig.show()


if __name__ == "__main__":
    morning = read_and_calc_data("2024-01-30", "10-00-07.csv", "11-00-59.csv")
    rush_hour = read_and_calc_data("2024-01-30", "15-03-46.csv", "16-03-09.csv")
    evening = read_and_calc_data("2024-01-30", "19-59-14.csv", "21-00-11.csv")
    all_data = pandas.concat((morning, rush_hour, evening))
    show_speed_map(all_data)
    print("Liczba autobusów, które przekroczyły 50 km/h: " + str(len(all_data.loc[all_data["Speed"] > 50])))
    print("Szybkość średnia rano: " + str(morning["Speed"].mean()))
    print("Szybkość średnia w godzinach szczytu: " + str(rush_hour["Speed"].mean()))
    print("Szybkość średnia wieczorem: " + str(evening["Speed"].mean()))
