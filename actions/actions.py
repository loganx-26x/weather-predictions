from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import spacy
import requests

from dotenv import load_dotenv
import os
load_dotenv()

# get the latest current weather for a city using OpenWeatherMap's API here
def get_weather(city, api_key):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city, api_key)
    response = requests.get(url)
    data = response.json()
    weather = {
        "description": data["weather"][0]["description"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }
    return weather

# function to get rainfall prediction for a city using OpenWeatherMap API
def get_rainfall(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    rain = []
    for item in data["list"]:
        if "rain" in item and "3h" in item["rain"]:
            rain.append(item["rain"]["3h"])
        else:
            rain.append(0)
    return sum(rain) / len(rain)


def get_message(query, text):
    # our API key
    api_key = os.getenv("API_KEY")

    # Getting the location
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    loc = None
    for ent in doc.ents:
        # a geopolitical entity is found so we'll save it
        if ent.label_ == "GPE" or ent.label_ == "LOC":
            loc = ent.text
            break
    
    # checkout the location
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(loc, api_key)
    response = requests.get(url).json()
    
    if loc == None or response["cod"] == "404":
        message = "Sorry, but I can't identify the location specified. Please enter another location!"
        return message
    
    if query == "weather":
        weather = get_weather(loc, api_key)
        message = f"Weather in {loc}: {weather['temperature']}°C, {weather['humidity']}% humidity, {weather['wind_speed']} m/s windspeed and {weather['description']}."

    elif query == "rainfall":
        rainfall = get_rainfall(loc, api_key)
        message = f"Rainfall prediction for {loc} in the next 5 days: {rainfall} mm."

    else:
        message = "Sorry, but I cannot understand your query. Please enter a specific locationfor  the weather or rainfall prediction "
    
    return message


# for weather conditions
class ActionAskWeather(Action):
    def name(self) -> Text:
        return "action_ask_weather"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = get_message("weather", (tracker.latest_message)['text'])
        dispatcher.utter_message(text=message)

        return []


# for rainfall conditions
class ActionAskRainfall(Action):
    def name(self) -> Text:
        return "action_ask_rainfall"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = get_message("rainfall", (tracker.latest_message)['text'])
        dispatcher.utter_message(text=message)

        return []
