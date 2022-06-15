''''''

import os
import pandas as pd
import requests 
from PIL import Image
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import credentials


scope = "user-read-playback-state"
redirect = "http://localhost:7777/callback"
redirect_uri = "http://localhost:8888/callback/"
token = util.prompt_for_user_token(username= credentials.username, scope = scope,redirect_uri=  redirect_uri, client_id = credentials.client_id, client_secret= credentials.client_secret)
sp = spotipy.Spotify(auth=token)


playback = sp.current_playback()

if playback == None:
    #put some function here, potentiall display weather data or similar
    pass

else:
    # print(playback)
    n_playback = pd.json_normalize(playback)
    album_art_url = n_playback['item.album.images'][0][0]["url"]
    print(n_playback['item.album.images'][0][0]["url"])
    response = requests.get(album_art_url)
    file = open("album_art.png", "wb")
    file.write(response.content)
    file.close()

