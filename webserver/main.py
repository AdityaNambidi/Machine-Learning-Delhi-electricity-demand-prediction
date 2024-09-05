from flask import Flask , render_template,request,jsonify
import datetime
from loadmodel import scaler, model
import requests
import pandas as pd
import os

app = Flask(__name__)
APIKEY = "ZB4Y226LCUMVPKCCYVZS63SEG"


@app.route("/temp")
def temp():
    return render_template("temp.html")

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/specifictime', methods=['POST'])
def specific_time():
    data = request.get_json()
    selected_date = data['date']
    selected_time = data['time']

    print(selected_date, selected_time)

    datetime_input = datetime.datetime.strptime(f"{selected_date} {selected_time}", '%Y-%m-%d %H:%M')
    
    weather_url = str("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/28.7041,77.1025/" + str(selected_date) + "T" + str(datetime_input.hour) + ":00:00?key=" + APIKEY + "&include=current")
    res = requests.get(weather_url)
    wdata = res.json()
    print(wdata)

    april19 = 2833.3958333333335

    inputdata = pd.DataFrame({
        'month' : [datetime_input.month],
        'hour' : [datetime_input.hour],
        'temp' : [wdata['days'][0]['temp']],
        'wind_speed' : [wdata['days'][0]['windspeed']],
        'preasure': [wdata['days'][0]['pressure']],
        'prev_avg_e': [april19]

    })

    inputdata[['month', 'hour', 'temp', 'wind_speed', 'preasure', 'prev_avg_e']] = scaler.transform(inputdata[['month', 'hour', 'temp', 'wind_speed', 'preasure', 'prev_avg_e']])
    result = model.predict(inputdata)[0]
    print(result)


    
    return jsonify({'result': result})


@app.route('/rangetime', methods=['POST'])
def range_time():
    data = request.get_json()
    startDate = data['date1']
    endDate = data['date2']
    time = str(str(datetime.datetime.now().hour) + ":" +  str(datetime.datetime.now().minute))

    start_input = datetime.datetime.strptime(f"{startDate} {time}", '%Y-%m-%d %H:%M')
    end_input = datetime.datetime.strptime(f"{endDate} {time}", '%Y-%m-%d %H:%M')
    
    weather_url = str("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/28.7041,77.1025/" + str(startDate) + "T" + str(start_input.hour) + ":00:00/" + str(endDate) + "T" + str(end_input.hour) + ":00:00?key=" + APIKEY + "&include=current")
    res = requests.get(weather_url)
    print(startDate, endDate)
    wdata = res.json()

    #making a list of all the days
    date_list = []
    current_date = start_input

    while current_date <= end_input:
        date_list.append(current_date)
        current_date += datetime.timedelta(days=1)


    prevE = 2833.3958333333335
    _i = 0
    preds = []
    days = []
    for day in date_list:
        _wd = wdata['days'][_i]

        inputdata = pd.DataFrame({
            'month' : [day.month],
            'hour' : [day.hour],
            'temp' : [_wd['temp']],
            'wind_speed' : [_wd['windspeed']],
            'preasure': [_wd['pressure']],
            'prev_avg_e': [prevE]

        })

        inputdata[['month', 'hour', 'temp', 'wind_speed', 'preasure', 'prev_avg_e']] = scaler.transform(inputdata[['month', 'hour', 'temp', 'wind_speed', 'preasure', 'prev_avg_e']])
        result = model.predict(inputdata)[0]
        pervE = result
        preds.append(result)
        days.append(day.day)

        _i += 1
    
    print(preds)
    
    return jsonify({'result': preds, 'days': days})


@app.route('/nexthour')
def next_hour():
    now = datetime.datetime.now()

    weather_url = str("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/28.7041,77.1025/" + str(now.date()) + "T" + str(now.hour + 1) + ":00:00?key=" + APIKEY)
    res = requests.get(weather_url)
    wdata = res.json()

    april19 = 2833.3958333333335

    nh = now.hour + 1
    if nh > 23:
        nh = 0

    inputdata = pd.DataFrame({
        'month' : [now.month],
        'hour' : [nh],
        'temp' : [wdata['days'][0]['hours'][nh]['temp']],
        'wind_speed' : [wdata['days'][0]['hours'][nh]['windspeed']],
        'preasure': [wdata['days'][0]['hours'][nh]['pressure']],
        'prev_avg_e': [april19]

    })

    inputdata[['month', 'hour', 'temp', 'wind_speed', 'preasure', 'prev_avg_e']] = scaler.transform(inputdata[['month', 'hour', 'temp', 'wind_speed', 'preasure', 'prev_avg_e']])
    result = model.predict(inputdata)[0]
    print(result)

    return jsonify({'result': result})


if __name__ == "__main__":
    app.run(debug=True)