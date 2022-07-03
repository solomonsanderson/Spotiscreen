''''''

import os
import pandas as pd
import requests 
from PIL import Image
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.oauth2 as oauth2
import credentials
import time
import sys
import subprocess
# from matrix_display import display_image
# import matrix_display.display_image
from get_weather import get_weather
from datetime import datetime, timedelta, date

scope = "user-read-playback-state"
redirect = "http://localhost:7777/callback"
redirect_uri = "http://localhost:8888/callback/"
auth_manager = SpotifyOAuth(username= credentials.username, scope = scope,redirect_uri=redirect_uri, client_id = credentials.client_id, client_secret= credentials.client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

prev_album_art_url = None

call_datetime = (datetime.now() - timedelta(hours=2))
call_time = call_datetime.time()
# print(call_time)


while True:
    try:
        token_info = auth_manager.get_cached_token()
        if auth_manager.is_token_expired(token_info) == True:
            auth_manager = SpotifyOAuth(username= credentials.username, scope = scope,redirect_uri=redirect_uri, client_id = credentials.client_id, client_secret= credentials.client_secret)
            sp = spotipy.Spotify(auth_manager=auth_manager)
            print("token refreshed")
        #    print(auth_manager.get_access_token(as_dict=False))


        playback = sp.current_playback()
        if playback == None:
            playing = False
            # print("none")
        elif playback != False:
            n_playback = pd.json_normalize(playback) 
            playing = n_playback['is_playing'][0]


        if playing == False:
            print("paused")
            now = datetime.now().time()
            dt = datetime.combine(date.today(), now) - datetime.combine(date.today(), call_time)
            interval = timedelta(seconds = 20)


            if ( dt > interval):
                get_weather("B296BP")
                call_time = datetime.now().time()
            
            # display_image("weather_icon.png")


        elif playing == True:
            album_art_url = n_playback['item.album.images'][0][0]["url"]
            if album_art_url == prev_album_art_url:
                print("Playing, No Change")
            elif album_art_url != prev_album_art_url:
                print("Downloading Album Cover")
                print(n_playback['item.album.images'][0][0]["url"])
                # display_image("album_art.png")
            prev_album_art_url = album_art_url
    except:
        print(f"An {sys.exc_info()} error occured")
    

    time.sleep(1)