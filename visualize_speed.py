import create_dataframe
import bus_speed
import plotly.express as px


def is_speed_correct(df):
    return ((df["VehicleNumber"] == df["VehicleNumber"].shift())
            & (df["Speed"] <= 100)
            & (df["SecondsPassed"] <= 150))


def show_speed_map():
    df = create_dataframe.combine_into_df("2024-01-22", "07-34-22.csv", "07-37-23.csv")
    bus_speed.calc_all(df)
    speed_data = df.loc[is_speed_correct(df)]
    lat_median = speed_data["Lat"].median()
    lon_median = speed_data["Lon"].median()
    fig = px.density_mapbox(speed_data.loc[speed_data["Speed"] > 50], lat='Lat', lon='Lon', z='Speed', radius=10,
                            center=dict(lat=lat_median, lon=lon_median), zoom=10,
                            mapbox_style="open-street-map")
    fig.show()


if __name__ == "__main__":
    show_speed_map()
