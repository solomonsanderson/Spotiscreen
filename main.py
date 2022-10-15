''''''

import pandas as pd
import requests 
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credentials
import time
from io import BytesIO
import platform
from get_weather import get_weather
from datetime import datetime



if platform.platform() != "Windows-10-10.0.19044-SP0":
    from rgbmatrix import RGBMatrix, RGBMatrixOptions


scope = "user-read-playback-state"
redirect_uri = "http://localhost:8888/callback/"



if platform.platform() != "Windows-10-10.0.19044-SP0":
    # creating matrix object
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "regular"
    options.limit_refresh_rate_hz = 100
    options.brightness=100
    matrix = RGBMatrix(options = options)

prev_album_art_url = None
token_expiration_status = True

# Timing
now = datetime.now().time()
off_time = datetime.strptime("12:00 AM", "%I:%M %p").time()
on_time = datetime.strptime("9:00 AM", "%I:%M %p").time()
print(off_time, on_time)


if off_time <= now < on_time:
    print("off")

auth_manager = SpotifyOAuth(client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri=redirect_uri, scope=scope)
token_info = auth_manager.get_cached_token()


while True:
    now = datetime.now().time()
    print(now)
    try:
        # print(token_expiration_status)
        # print(f"INFO{token_info} ")
        if off_time <= now < on_time:
            print("Sleep!")

        if token_expiration_status == True or token_info == None:
            print("Updating Token!")
            auth_manager = SpotifyOAuth(client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri=redirect_uri, scope=scope)
            sp = spotipy.Spotify(auth_manager=auth_manager)

        
        if token_info != None:
            token_expiration_status = auth_manager.is_token_expired(token_info)
        playback = sp.current_playback()
        
        if playback == None:
            print("Paused")



        else:
            n_playback = pd.json_normalize(playback)
            playing = n_playback['is_playing'][0]
            print(playing)
            album_art_url = n_playback['item.album.images'][0][0]["url"]
            if prev_album_art_url != album_art_url:
                print("Updating Image")
                response = requests.get(album_art_url)
                cover = Image.open(BytesIO(response.content))
                if platform.platform() != "Windows-10-10.0.19044-SP0":
                    if off_time <= now < on_time:
                        cover.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
                        matrix.SetImage(cover.convert("RGB"))
                    else:
                        matrix.SetImage(None)
                prev_album_art_url = album_art_url

    except Exception as e:
        print(e)
        pass
    

    time.sleep(0.5)