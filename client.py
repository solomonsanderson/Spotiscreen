# from urllib3 import request
# import urllib3
from flask import Flask, render_template, Response, request, jsonify
import configparser
import pandas as pd
from fileinput import filename
from multiprocessing import Process, Value
import main
from main import matrix
import time
import os

app = Flask(__name__)
app.config['TESTING'] = True

config = configparser.ConfigParser()
config.read("settings.ini")


def get_config():
    screen_height = config["properties"]["screen_height"]
    screen_width = config["properties"]["screen_width"]

    onoff = config["settings"]["onoff"]
    brightness = config["settings"]["brightness"]
    idle_display = config["settings"]["idle_display"]

    return (screen_height, screen_width), onoff, brightness, idle_display


@app.route("/", methods = ["POST","GET"])   
def client():
    # if request.method == "POST":
    # state = request.form.get
    screen_size, onoff, brightness, idle_display = get_config()
    dirs = []
    for dir in os.listdir("idle_images"):
        dirs.append({'name': dir})

    # print(onoff, brightness, idle_display)
    return render_template("index.html", onoff=onoff, brightness=int(brightness), idle_display=idle_display, data = dirs)


@app.route("/onoff/", methods=["POST", "GET"])
def handle_onoff():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        onoff = data[0]["onoff"]
        brightness = data[1]["brightness"]
        idle_display = data[2]["idle_display"]
    # onoff = request.args("onoffbox")
        config["settings"]["onoff"] = str(onoff)
        config["settings"]["brightness"] = str(brightness)
        config["settings"]["idle_display"] = idle_display
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

    screen_size, onoff, brightness, idle_display = get_config()

    return render_template("index.html", onoff=onoff, brightness=int(brightness), idle_display=idle_display)


# @app.route("/", methods = ["POST", "GET"])
# def 


@app.route("/success", methods=["POST"])
def success():
    if request.method == "POST":
        f = request.files["fileupload"]
        f.save("idle_images/" + f.filename)

    dirs = []
    for dir in os.listdir("idle_images"):
        dirs.append({'name': dir})

    screen_size, onoff, brightness, idle_display = get_config()
    return render_template("index.html", onoff=onoff, brightness=int(brightness), idle_display=idle_display, data = dirs)
        

@app.route("/selected/", methods = ["POST"])
def select_image():
    if request.method == "POST":
        data = request.get_json()
        print(data)
# @app.route("/brightness/", methods=["POST", "GET"])
# def handle_brightness():
#     if request.method == "POST":
#         data = request.get_json()
#         print(brightness)
    
#     config["settings"]["brightness"] = brightness
#     screen_size, onoff, brightness, idle_display = get_config()
#     return render_template("index.html", onoff=onoff, brightness=brightness, idle_display=idle_display)


# @app.route("/idle_display/", methods=["POST", "GET"])
# def handle_idle_display():
#     # onoff = request.args("onoffbox")
#     config["settings"]["idle_display"] = idle_display
#     screen_size, onoff, brightness, idle_display = get_config()
#     return render_template("index.html", onoff=onoff, brightness=brightness, idle_display=idle_display)


def matrix_loop():
    mat = matrix()
    while True:
        mat.update()
        mat.update_brightness()
        mat.update_onoff()
        time.sleep(0.5)

if __name__ == "__main__":
    # recording_on = 
    p = Process(target = matrix_loop)
    p.start()
    app.run(host="192.168.0.14", port = 5000, debug=True, use_reloader = False)
    p.join()
    
