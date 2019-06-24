import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def show_image():
    image_path = os.sep.join(["static", "co2.png"])
    return render_template("index.html", co2_graph_path=image_path)
