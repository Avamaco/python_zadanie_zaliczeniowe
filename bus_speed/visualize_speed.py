from bus_data import create_dataframe
from bus_speed import speed
import plotly.express as px
import pandas


def read_and_calc_data():
    morning = create_dataframe.combine_into_df("2024-01-30", "10-00-07.csv", "11-00-59.csv")
    rush_hour = create_dataframe.combine_into_df("2024-01-30", "15-03-46.csv", "16-03-09.csv")
    evening = create_dataframe.combine_into_df("2024-01-30", "19-59-14.csv", "21-00-11.csv")
    speed.calc_all(morning)
    speed.calc_all(rush_hour)
    speed.calc_all(evening)
    morning = speed.cut_incorrect_speed(morning)
    rush_hour = speed.cut_incorrect_speed(rush_hour)
    evening = speed.cut_incorrect_speed(evening)
    return morning, rush_hour, evening


def show_speed_map(speed_data):
    lat_median = speed_data["Lat"].median()
    lon_median = speed_data["Lon"].median()
    fig = px.density_mapbox(speed_data.loc[speed_data["Speed"] > 50], lat='Lat', lon='Lon', z='Speed', radius=10,
                            center=dict(lat=lat_median, lon=lon_median), zoom=10,
                            mapbox_style="open-street-map")
    fig.show()


if __name__ == "__main__":
    morning, rush_hour, evening = read_and_calc_data()
    all_data = pandas.concat((morning, rush_hour, evening))
    show_speed_map(all_data)
    print("Liczba autobusów, które przekroczyły 50 km/h: " + str(len(all_data.loc[all_data["Speed"] > 50])))
    print("Szybkość średnia rano: " + str(morning["Speed"].mean()))
    print("Szybkość średnia w godzinach szczytu: " + str(rush_hour["Speed"].mean()))
    print("Szybkość średnia wieczorem: " + str(evening["Speed"].mean()))
