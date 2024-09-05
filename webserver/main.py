from flask import Flask , render_template,request,jsonify
import datetime
from loadmodel import scaler, model
import requests
import pandas as pd
import os

app = Flask(__name__)
APIKEY = "ZB4Y226LCUMVPKCCYVZS63SEG"

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/specifictime', methods=['POST'])
def specific_time():
    data = request.get_json()
    selected_date = data['date']
    selected_time = data['time']

    datetime_input = datetime.datetime.strptime(f"{selected_date} {selected_time}", '%Y-%m-%d %H:%M')
    
    weather_url = str("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/28.7041,77.1025/" + str(selected_date) + "T" + str(datetime_input.hour) + ":00:00?key=" + APIKEY)
    res = requests.get(weather_url)
    wdata = res.json()

    april19 = 2833.3958333333335

    inputdata = pd.DataFrame({
        'month' : [datetime_input.month],
        'hour' : [datetime_input.hour],
        'temp' : [wdata['days'][0]['hours'][datetime_input.hour]['temp']],
        'wind_speed' : [wdata['days'][0]['hours'][datetime_input.hour]['windspeed']],
        'preasure': [wdata['days'][0]['hours'][datetime_input.hour]['pressure']],
        'prev_avg_e': [april19]

    })

    inputdata[['month', 'hour', 'temp', 'wind_speed', 'preasure', 'prev_avg_e']] = scaler.transform(inputdata[['month', 'hour', 'temp', 'wind_speed', 'preasure', 'prev_avg_e']])
    result = model.predict(inputdata)[0]
    print(result)
    
    return jsonify({'result': result})


@app.route('/rangetime', methods=['POST'])
def range_time():
    return 0


@app.route('/nexthour')
def next_hour():
    now = datetime.datetime.now()

    weather_url = str("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/28.7041,77.1025/" + str(now.date()) + "T" + str(now.hour + 1) + ":00:00?key=" + APIKEY)
    res = requests.get(weather_url)
    wdata = res.json()

    april19 = 2833.3958333333335

    inputdata = pd.DataFrame({
        'month' : [now.month],
        'hour' : [now.hour + 1],
        'temp' : [wdata['days'][0]['hours'][now.hour]['temp']],
        'wind_speed' : [wdata['days'][0]['hours'][now.hour + 1]['windspeed']],
        'preasure': [wdata['days'][0]['hours'][now.hour + 1]['pressure']],
        'prev_avg_e': [april19]

    })

    inputdata[['month', 'hour', 'temp', 'wind_speed', 'preasure', 'prev_avg_e']] = scaler.transform(inputdata[['month', 'hour', 'temp', 'wind_speed', 'preasure', 'prev_avg_e']])
    result = model.predict(inputdata)[0]
    print(result)

    return jsonify({'result': result})


if __name__ == "__main__":
    app.run(debug=True)