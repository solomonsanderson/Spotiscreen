from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route("/")
def client():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
