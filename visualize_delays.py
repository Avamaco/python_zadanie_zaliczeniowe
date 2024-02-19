import pandas
import plotly.express as px
import bus_stop_distances
import bus_delays


def get_avg_delay(df):
    avg_delay = arrival_data.groupby(["BusstopId", "BusstopNr"])["Delay"].mean()
    return pandas.DataFrame({
        "BusstopId": arrival_data["BusstopId"],
        "BusstopNr": arrival_data["BusstopNr"],
        "AvgDelay": [avg_delay.to_dict()[(busstop_id, busstop_nr)]
                     for busstop_id, busstop_nr in zip(arrival_data["BusstopId"], arrival_data["BusstopNr"])]
    }).drop_duplicates()


def add_bus_stop_pos(df):
    stops = bus_stop_distances.get_bus_stop_dict()
    df["Lat"] = [stops[(busstop_id, str(busstop_nr).zfill(2))][0]
                 for busstop_id, busstop_nr
                 in zip(df["BusstopId"], df["BusstopNr"])]
    df["Lon"] = [stops[(busstop_id, str(busstop_nr).zfill(2))][1]
                 for busstop_id, busstop_nr
                 in zip(df["BusstopId"], df["BusstopNr"])]


def show_delay_map(df):
    lat_median = df["Lat"].median()
    lon_median = df["Lon"].median()
    fig = px.density_mapbox(df, lat='Lat', lon='Lon', z='AvgDelay', radius=10,
                            center=dict(lat=lat_median, lon=lon_median), zoom=10,
                            mapbox_style="open-street-map")
    fig.show()


if __name__ == "__main__":
    arrival_data = bus_delays.get_arrivals()
    arrival_data = bus_delays.find_all_delays(arrival_data)
    bus_stop_delays = get_avg_delay(arrival_data)
    add_bus_stop_pos(bus_stop_delays)
    show_delay_map(bus_stop_delays)
