from flask import render_template
from app import app
import plotting
import os


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


@app.route("/map")
def map():
    folium_map = plotting.get_folium_map()
    return folium_map.get_root().render()

