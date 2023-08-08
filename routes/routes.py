from flask import Flask
from threading import Thread
import requests
import pandas as pd
from routes.constants import API_KEY_WEATHER

app = Flask('')


@app.route('/')
def home():
    return "I'm alive"


def run():
    app.run(host='0.0.0.0', port=80)


def keep_alive():
    t = Thread(target=run)
    t.start()


def get_weather_json(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + API_KEY_WEATHER
    print(url)
    return requests.get(url).json()


def get_english_name(city_name):
    df = pd.read_csv('patterns/weather_bot/data/cities_ru_en.csv', names=['russian', 'english'])
    row = df[df['russian'] == city_name]
    if len(row) == 0:
        return city_name
    else:
        return row.iloc[0]['english']


def get_weather_readable(message, json):
    print(json)
    if json['cod'] == '404':
        return 'Город не найден'
    return 'Данные о погоде в городе ' + message.text + ':\n' + \
           'Температура: ' + str(json['main']['temp'] - 273.15) + '°C\n' + \
           'Чувствуется как: ' + str(json['main']['feels_like'] - 273.15) + '°C\n' + \
           'Давление: ' + str(json['main']['pressure']) + ' мм.рт.ст\n' + \
           'Влажность: ' + str(json['main']['humidity']) + '%\n' + \
           'Сила ветра: ' + str(json['wind']['speed']) + ' м/с\n'


def execute(bot, message):
    bot.send_message(message.from_user.id, get_weather_readable(
        message, get_weather_json(get_english_name(message.text)))
    )
