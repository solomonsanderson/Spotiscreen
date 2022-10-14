# from urllib3 import request
# import urllib3
from flask import Flask, render_template, Response, request


app = Flask(__name__)
app.config['TESTING'] = True



@app.route("/", methods = ["POST","GET"])
def client():
    # if request.method == "POST":
    # state = request.form.get
    return render_template("index.html")

@app.route("/onoff/", methods=["POST", "GET"])
def handle_onoff():
    onoff = request.args("onoffbox")
    print(onoff)
    return render_template("index.html", onoff=onoff)

if __name__ == "__main__":
    app.run()
