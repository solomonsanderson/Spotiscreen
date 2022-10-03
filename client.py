from urllib import request
from flask import Flask, render_template, Response


app = Flask(__name__)
app.config['TESTING'] = True



@app.route("/background_process/")
def background_process():
    try:
        info = request.get("brightslide", 0, type=str)
        print(info)
    except Exception as e:
        return str(e)


@app.route("/", methods = ["POST","GET"])
def client():
    # if request.method == "POST":
    # state = request.form.get
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
