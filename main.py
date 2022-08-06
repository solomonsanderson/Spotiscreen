''''''

import pandas as pd
import requests 
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credentials
import time
from io import BytesIO
# from rgbmatrix import RGBMatrix, RGBMatrixOptions
import sys
import subprocess
from get_weather import get_weather
from datetime import datetime, timedelta, date

scope = "user-read-playback-state"
redirect_uri = "http://localhost:8888/callback/"
auth_manager = SpotifyOAuth(username= credentials.username, scope = scope,redirect_uri=redirect_uri, client_id = credentials.client_id, client_secret= credentials.client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

prev_album_art_url = None

# creating matrix object
# options = RGBMatrixOptions()
# options.rows = 32
# options.chain_length = 1
# options.parallel = 1
# options.hardware_mapping = "regular"
# options.limit_refresh_rate_hz = 100
# options.brightness=100
# matrix = RGBMatrix(options = options)


call_datetime = (datetime.now() - timedelta(hours=2))
call_time = call_datetime.time()
# print(call_time)


while True:
    try:
        token_info = auth_manager.get_cached_token()
        if auth_manager.is_token_expired(token_info) == True or (token_info == None):
            auth_manager = SpotifyOAuth(username= credentials.username, scope = scope,redirect_uri=redirect_uri, client_id = credentials.client_id, client_secret= credentials.client_secret)
            sp = spotipy.Spotify(auth_manager=auth_manager)
            print("token refreshed")
    except:
        auth_manager = SpotifyOAuth(username= credentials.username, scope = scope,redirect_uri=redirect_uri, client_id = credentials.client_id, client_secret= credentials.client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)
    #    print(auth_manager.get_access_token(as_dict=False))
    
    playback = sp.current_playback()
    if playback == None:
        print("paused")
    else:
        n_playback = pd.json_normalize(playback)
        playing = n_playback['is_playing'][0]
        if playing == False:
            print("paused")
            t=0
            weather_delay = 0
            while t <= weather_delay:
                print(t)
                t = t++1
                time.sleep(1)
            
            weather = get_weather("B296BP")
            weather_icon_url = weather["current.condition.icon"][0]
            weather_icon_url = weather_icon_url.replace("64x64","128x128")
            response = requests.get("http:" + weather_icon_url)
            weather_icon = Image.open(BytesIO(response.content))
            # weather_icon.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
            # matrix.SetImage(weather_icon.convert("RGB"))

        elif playing == True:
            print("Playing")
            t=0
            album_art_url = n_playback['item.album.images'][0][0]["url"]
            if prev_album_art_url != album_art_url:
                response = requests.get(album_art_url)
                cover = Image.open(BytesIO(response.content))
                # cover.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
                # matrix.SetImage(cover.convert("RGB"))
                prev_album_art_url = album_art_url
    # except:
    #     print(f"An {sys.exc_info()} error occured")


        # elif playback != False:
        #     n_playback = pd.json_normalize(playback) 
        #     playing = n_playback['is_playing'][0]


        # if playing == False:
        #     print("paused")
        #     now = datetime.now().time()
        #     dt = datetime.combine(date.today(), now) - datetime.combine(date.today(), call_time)
        #     interval = timedelta(seconds = 20)
        #     if ( dt > interval):
        #         get_weather("Austrailia")
        #         call_time = datetime.now().time()
            
            # display_image("weather_icon.png")


        # elif playing == True:
        #     album_art_url = n_playback['item.album.images'][0][0]["url"]
        #     if album_art_url == prev_album_art_url:
        #         print("Playing, No Change")
        #     elif album_art_url != prev_album_art_url:
        #         print("Downloading Album Cover")
        #         print(n_playback['item.album.images'][0][0]["url"])
        #         # display_image("album_art.png")
        #     prev_album_art_url = album_art_url
    # except:
    #     print(f"An {sys.exc_info()} error occured")
    

    time.sleep(1)