from datetime import datetime as dt

import os
import requests
from flask import Flask, render_template, request, redirect

import db

app = Flask(__name__)

db_conn = db.init_db("mel.db")


@app.route("/")
def index():
  # haal de data op van de webservice

  data = {
    "email": os.getenv("username"),
    "password": os.getenv("password"),
    "req": "getall"
  }
  print(data)
  url = os.getenv("base_url") + "/4-logs-api.php"
  response_api = requests.post(
    url=url,
    data=data,
  )
  api_data = response_api.json()["more"] or []

  # data ophalen van mijn database
  db_data = db.list_data_points(db_conn)

  # samenvoegen van de data
  merged_data = api_data + db_data

  # data sorteren
  sorted_data = sorted(merged_data, key=lambda d: d["created"])

  # gebruik de template om data weer te geven (tabel en chart)
  return render_template(
    "index.html",
    data=sorted_data,
    x_values=[_convert_timestamp_to_hours(d["created"]) for d in sorted_data],
    y_values=[int(d["value"]) for d in sorted_data],
  )


@app.route("/data", methods=["POST"])
def add_data_point():
  datetime = request.form["datetime"]
  sensor = request.form["sensor"]
  value = request.form["value"]
  db.add_data_point(db_conn, datetime, sensor, value)
  return redirect("/")


def _convert_timestamp_to_hours(stamp):
  value = dt.strptime(stamp, "%Y-%m-%d %H:%M:%S")
  jan_2019 = dt(2022, 1, 1)
  return round((value - jan_2019).total_seconds() / 3_600, 0)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=81, debug=True)
