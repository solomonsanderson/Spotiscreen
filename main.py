''''''

import pandas as pd
import requests 
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credentials
import time
from io import BytesIO
from rgbmatrix import RGBMatrix, RGBMatrixOptions



scope = "user-read-playback-state"
redirect = "http://localhost:7777/callback"
redirect_uri = "http://localhost:8888/callback/"
auth_manager = SpotifyOAuth(username= credentials.username, scope = scope,redirect_uri=redirect_uri, client_id = credentials.client_id, client_secret= credentials.client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

prev_album_art_url = None

# creating matrix object
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "regular"
options.limit_refresh_rate_hz = 60
matrix = RGBMatrix(options = options)


while True:
    #try:
    token_info = auth_manager.get_cached_token()
    if auth_manager.is_token_expired(token_info) == True:
        auth_manager = SpotifyOAuth(username= credentials.username, scope = scope,redirect_uri=redirect_uri, client_id = credentials.client_id, client_secret= credentials.client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        print("token refreshed")
    #    print(auth_manager.get_access_token(as_dict=False))
    
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
            
            if prev_album_art_url != album_art_url:
                
                response = requests.get(album_art_url)
                cover = Image.open(BytesIO(response.content))
                cover.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
                matrix.SetImage(cover.convert("RGB"))
                prev_album_art_url = album_art_url
            

    time.sleep(1)