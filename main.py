import requests
from flask import Flask, render_template, request, redirect

import db

app = Flask(__name__)

TEMPERATURE_SERVICE = "https://po-meten.arhc.informatica.gsf.nl/4-logs-api.php"

db_conn = db.init_db("mel.db")


@app.route("/")
def index():
    # krijg de data van de webservice
    response_api = requests.post(
        TEMPERATURE_SERVICE,
        data={"req": "getall"},
    )
    api_data = response_api.json()["more"]

    # krijg de data van mijn database
    db_data = db.list_data_points(db_conn)

    # samenvoegen van de data
    merged_data = api_data + db_data

    # data sorteren
    sorted_data = sorted(merged_data, key=lambda d: d["created"])

    # gebruik de template om data weer te geven
    return render_template("index.html", data=sorted_data)


@app.route("/data", methods=["POST"])
def add_data_point():
    datetime = request.form["datetime"]
    sensor = request.form["sensor"]
    value = request.form["value"]
    db.add_data_point(db_conn, datetime, sensor, value)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)
