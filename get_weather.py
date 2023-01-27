'''Code to get weather data from weatherapi.com and return an image and other information to be shown on the matrix display'''


import requests
import pandas as pd
import geocoder
import sys


def get_weather(location):
    if location == "auto":
        g = geocoder.ip('me')
        print(g.latlng)
        latlng = str(g.latlng)
        for i in ["[", "]"," "]:
            latlng = latlng.replace(i, "")
        print(latlng)
        response = requests.get("http://api.weatherapi.com/v1/current.json?key=e3052fb6b4594c309bb234000220207&q=" + str(latlng))

    else:
        response = requests.get("http://api.weatherapi.com/v1/current.json?key=e3052fb6b4594c309bb234000220207&q=" + str(location))

    # print(response.status_code)
    print(response.json())

    norm_response = pd.json_normalize(response.json())
    # # print(norm_response)
    # current_temp = norm_response["current.temp_c"]
    # current_condition = norm_response["current.condition.text"]
    # # # print(current_temp)
    # # # print(norm_response["current.condition.icon"])

    # # icon_url = (norm_response["current.condition.icon"][0])
    # # # print(icon)
    # # # print(icon_url)
    # # icon = requests.get("http:" + icon_url)
    # # file = open("weather_icon.png", "wb")
    # # file.write(icon.content)
    # # file.close()
    return norm_response

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit(f"1 args required, {len(sys.argv)-1} given")
    get_weather(sys.argv)