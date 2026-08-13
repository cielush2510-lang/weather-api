from flask import Flask, render_template
import pandas as pd
import numpy as np


def get_station(station):
    filename = "data_big/stations.txt"
    df_local = pd.read_csv(filename, skiprows=17)
    station_name = df_local.loc[df_local['STAID']==station]['STANAME                                 '].squeeze().strip()
    return station_name


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<int:station>/<date>")
def apicall(station, date):
    filename = "data_big/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df['TG0'] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
    df['TG'] = df['TG0'] / 10
    temperature = df.loc[df['    DATE']==date]['TG'].squeeze()
    fahrenheit = round(temperature * (9 / 5) + 32, 2)
    station_name = get_station(station)
    result = {"Station": station_name, "Date": date, "Temperature": temperature, "Fahrenheit": fahrenheit}
    return result


if __name__ == "__main__":
    app.run(debug=True)
