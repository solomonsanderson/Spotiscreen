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
import sys
import subprocess


scope = "user-read-playback-state"
redirect = "http://localhost:7777/callback"
redirect_uri = "http://localhost:8888/callback/"
token = util.prompt_for_user_token(username= credentials.username, scope = scope,redirect_uri=  redirect_uri, client_id = credentials.client_id, client_secret= credentials.client_secret)
sp = spotipy.Spotify(auth=token)
print(sys.argv)
prev_album_art_url = None
token_time = 0 
while True:
    try:
        playback = sp.current_playback()
        if playback == None:
            print("paused")
        else:
            n_playback = pd.json_normalize(playback)
            playing = n_playback['is_playing'][0]
            if playing == False:
                print("paused")
            elif playing == True:
                album_art_url = n_playback['item.album.images'][0][0]["url"]
                if album_art_url == prev_album_art_url:
                    print("Playing, No Change")
                elif album_art_url != prev_album_art_url:
                    print("Downloading Album Cover")
                    print(n_playback['item.album.images'][0][0]["url"])
                    response = requests.get(album_art_url)
                    file = open("album_art.png", "wb")
                    file.write(response.content)
                    file.close()
                    image = subprocess.Popen("fim -a album_art.png", shell = True)
                prev_album_art_url = album_art_url
    except:
        print(f"An {sys.exc_info()[0]} error occured")
    
    token_time += 1 
    if token_time == 1000:
        print(token)
        sp = spotipy.Spotify(auth=token)
        print(sp)
        print("token refreshed")
        token_time = 0 
    time.sleep(1)