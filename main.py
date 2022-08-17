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

pause_timer = 0

while True:
    try:
        if token_expiration_status == True:
            print("Updating Token!")
            auth_manager = SpotifyOAuth(client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri=redirect_uri, scope=scope)
            sp = spotipy.Spotify(auth_manager=auth_manager)

        token_info = auth_manager.get_cached_token()
        token_expiration_status = auth_manager.is_token_expired(token_info)
        playback = sp.current_playback()
        
        if playback == None:
            print("Paused")
            # if pause_timer > 20:
            #     pass
            # pause_timer += 1

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
                    cover.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
                    matrix.SetImage(cover.convert("RGB"))
                prev_album_art_url = album_art_url

    except Exception as e:
        print(e)
        pass
    

    time.sleep(0.5)