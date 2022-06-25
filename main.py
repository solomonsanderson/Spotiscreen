''''''

import os
import pandas as pd
import requests 
from PIL import Image
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import credentials
import time


scope = "user-read-playback-state"
redirect = "http://localhost:7777/callback"
redirect_uri = "http://localhost:8888/callback/"
token = util.prompt_for_user_token(username= credentials.username, scope = scope,redirect_uri=  redirect_uri, client_id = credentials.client_id, client_secret= credentials.client_secret)
sp = spotipy.Spotify(auth=token)

prev_album_art_url = None
while not False:
    playback = sp.current_playback()
    n_playback = pd.json_normalize(playback)
    playing = n_playback['is_playing'][0]
    # print(playing)
    # n_playback.to_csv('test.csv')
    if playing == False:
        print("paused")

    elif playing == True:
        album_art_url = n_playback['item.album.images'][0][0]["url"]
        if album_art_url == prev_album_art_url:
            pass
        elif album_art_url != prev_album_art_url:
            print("Downloading Album Cover")
            print(n_playback['item.album.images'][0][0]["url"])
            response = requests.get(album_art_url)
            file = open("album_art.png", "wb")
            file.write(response.content)
            file.close()
            print("playing")
        prev_album_art_url = album_art_url
    time.sleep(1)