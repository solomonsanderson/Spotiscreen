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
import configparser
import datetime


if platform.platform() != "Windows-10-10.0.19044-SP0":
    from rgbmatrix import RGBMatrix, RGBMatrixOptions


scope = "user-read-playback-state"
redirect_uri = "http://localhost:8888/callback/"



# if platform.platform() != "Windows-10-10.0.19044-SP0":
#     # creating matrix object
#     options = RGBMatrixOptions()
#     options.rows = 32
#     options.chain_length = 1
#     options.parallel = 1
#     options.hardware_mapping = "regular"
#     options.limit_refresh_rate_hz = 100
#     options.brightness=100
#     matrix = RGBMatrix(options = options)

# prev_album_art_url = None
# token_expiration_status = True

# pause_timer = 0

# while True:
#     try:
#         if token_expiration_status == True:
#             print("Updating Token!")
#             auth_manager = SpotifyOAuth(client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri=redirect_uri, scope=scope)
#             sp = spotipy.Spotify(auth_manager=auth_manager)

#         token_info = auth_manager.get_cached_token()
#         token_expiration_status = auth_manager.is_token_expired(token_info)
#         playback = sp.current_playback()
        
#         if playback == None:
#             print("Paused")
#             current_t = datetime.now()
             
#             if pause_time == None:
#                 pause_time = datetime.now()
            
            

#         else:
#             pause_time = None
#             n_playback = pd.json_normalize(playback)
#             playing = n_playback['is_playing'][0]
#             print(playing)
#             album_art_url = n_playback['item.album.images'][0][0]["url"]
#             if prev_album_art_url != album_art_url:
#                 print("Updating Image")
#                 response = requests.get(album_art_url)
#                 cover = Image.open(BytesIO(response.content))
#                 if platform.platform() != "Windows-10-10.0.19044-SP0":
#                     cover.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
#                     matrix.SetImage(cover.convert("RGB"))
#                 prev_album_art_url = album_art_url

#     except Exception as e:
#         print(e)
#         pass
    

#     time.sleep(0.5)

class matrix:
    ''' A class representing an LED matrix'''


    def __init__(self):
        ''''''

        config = configparser.ConfigParser()
        config.read("settings.ini")

        self.width = int(config["properties"]["screen_width"])
        self.height = int(config["properties"]["screen_height"])
        self.brightness = int(config["settings"]["brightness"])
        self.chain_length = 1
        self.parallel = 1
        self.hardware_mapping = "regular"
        self.limit_refresh_rate_hz = 100

        self.art_url = None
        self.prev_art_url = None
        self.token_status = True

        if platform.platform() != "Windows-10-10.0.19044-SP0":
            options = RGBMatrixOptions()
            options.rows = self.width
            options.chain_length = 1
            options.parallel = 1
            options.hardware_mapping = "regular"
            options.limit_refresh_rate_hz = 100
            options.brightness = self.brightness
            matrix = RGBMatrix(options = options)
        
        self.pause_time = None

        self.auth_manager = SpotifyOAuth(client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri=redirect_uri, scope=scope)
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)


    def play_status(self, playback):
        '''Gets the playback state of the spotify account, returns False if paused and True if playing '''
    

        if playback == None:
            return False
        
        else:
            n_playback = pd.json_normalize(playback)
            playing = n_playback['is_playing'][0]
            return playing 


    def update(self):
        ''''''
        # try:
        print(self.token_status)
        if self.token_status == True:
            print("Updating Token!")
            self.auth_manager = SpotifyOAuth(client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri=redirect_uri, scope=scope)
            self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

        token_info = self.auth_manager.get_cached_token()
        self.token_status = self.auth_manager.is_token_expired(token_info)
        playback = self.sp.current_playback()
        
        status = self.play_status(playback)
        
        if status == False:
            print("Paused")
            current_t = datetime.datetime.now()
         
            if self.pause_time == None:
                self.pause_time = datetime.datetime.now()
            
            diff = current_t - self.pause_time
            if diff > datetime.timedelta(minutes=0, seconds = 1):
                print("Show weather")
                if diff.seconds % 30 == 0:
                    print("Update Weather")
                    weather_json = get_weather("england")
                

        else:
            print("playing")
            self.pause_time = None
            n_playback = pd.json_normalize(playback)
            # playing = n_playback['is_playing'][0]
            # print(playing)
            self.art_url = n_playback['item.album.images'][0][0]["url"]
            if self.prev_art_url != self.art_url:
                print("Updating Image")
                response = requests.get(self.art_url)
                cover = Image.open(BytesIO(response.content))
                if platform.platform() != "Windows-10-10.0.19044-SP0":
                    cover.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
                    matrix.SetImage(cover.convert("RGB"))
                self.prev_art_url = self.art_url
        # except Exception as e:
        #     print(e)
        #     pass


if __name__ == "__main__":
    mat = matrix()
    while True:
        mat.update()
        time.sleep(0.5)





