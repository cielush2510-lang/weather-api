from flask import Flask, render_template
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<word>")
def apicall(station, date):
    filename = "data_big/TG_STAID" + str(station).zfill(6) + ".txt"
    pd.read_csv("data_big/yossi.txt")

    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df['TG0'] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
    df['TG'] = df['TG0'] / 10
    temperature = df.loc[df['    DATE']==date]['TG'].squeeze()
    result = {"Station": station, "Date": date, "Temperature": temperature}
    return result


if __name__ == "__main__":
    app.run(debug=True)
