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
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

scope = "user-read-playback-state"
redirect_uri = "http://localhost:8888/callback/"


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
            self.matrix = RGBMatrix(options = options)
        
        self.pause_time = None

        self.auth_manager = SpotifyOAuth(client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri=redirect_uri, scope=scope)
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)


    def update_brightness(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")
        if int(config["settings"]["brightness"]) != self.brightness:
            print("brightness changed")
            self.brightness = int(config["settings"]["brightness"])
            if platform.platform() != "Windows-10-10.0.19044-SP0":
                options = RGBMatrixOptions()
                options.rows = self.width
                options.chain_length = 1
                options.parallel = 1
                options.hardware_mapping = "regular"
                options.limit_refresh_rate_hz = 100
                options.brightness = int(config["settings"]["brightness"])
                self.matrix = RGBMatrix(options = options)


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
        config = configparser.ConfigParser()
        config.read("settings.ini")
        idle_display = str(config["settings"]["idle_display"])
        
        # try:
        # print(self.token_status)
        if self.token_status == True:
            print("Updating Token!")
            self.auth_manager = SpotifyOAuth(client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri=redirect_uri, scope=scope)
            self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

        token_info = self.auth_manager.get_cached_token()
        self.token_status = self.auth_manager.is_token_expired(token_info)
        playback = self.sp.current_playback()
        
        status = self.play_status(playback)
        
        if status == False:
            icon_url = None
            print("Paused")
            current_t = datetime.datetime.now()
         
            if self.pause_time == None:
                self.pause_time = datetime.datetime.now()
            
            diff = current_t - self.pause_time
            if diff > datetime.timedelta(minutes=0, seconds = 1):
                if idle_display == "weather":
                    print("Show weather")
                    if diff.seconds == 1:
                        print("Update Weather")
                        icon_url = get_weather("auto")

                    elif diff.seconds % 30 == 0:
                        print("Update Weather")
                        icon_url = get_weather("auto")

                    if icon_url != None:
                        print("display weather")
                        response = requests.get(icon_url)
                        cover = Image.open(BytesIO(response.content))
                        if platform.platform() != "Windows-10-10.0.19044-SP0":
                            cover.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
                            self.matrix.SetImage(cover.convert("RGB"))

                elif idle_display == "image":
                    print("display image")


                elif idle_display == "time":
                    print("display time")

                    white = graphics.Color(0, 0, 0)
                    time = datetime.datetime.now()
                    print(time)
                    font = graphics.Font()
                    font.LoadFont("../../../fonts/7x13.bdf")
                    graphics.DrawText(self.matrix, font, 2, 10, white, time)


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
                    cover.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
                    self.matrix.SetImage(cover.convert("RGB"))
                self.prev_art_url = self.art_url
        # except Exception as e:
        #     print(e)
        #     pass


if __name__ == "__main__":
    mat = matrix()
    while True:
        mat.update()
        time.sleep(0.5)





