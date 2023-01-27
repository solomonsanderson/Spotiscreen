'''Code to get weather data from weatherapi.com and return an image and other information to be shown on the matrix display'''


import requests
import pandas as pd
import geocoder
import sys


def get_weather(location):
    if location == "auto":
        g = geocoder.ip('me')
        # print(g)
        # print(g.latlng)
        latlng = str(g.latlng)
        for i in ["[", "]"," "]:
            latlng = latlng.replace(i, "")
        # print(latlng)
        response = requests.get("http://api.weatherapi.com/v1/current.json?key=e3052fb6b4594c309bb234000220207&q=" + str(latlng))

    else:
        response = requests.get("http://api.weatherapi.com/v1/current.json?key=e3052fb6b4594c309bb234000220207&q=" + str(location))

    norm_response = pd.json_normalize(response.json())
    icon_url = "https:" + norm_response["current.condition.icon"]
    print(icon_url)
    return icon_url[0]

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit(f"1 args required, {len(sys.argv)-1} given")
    get_weather(sys.argv)