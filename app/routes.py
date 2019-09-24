from flask import render_template
from app import app
import plotting
import os


@app.route("/")
@app.route("/index")
def index():
    try:
        with open('static/status.txt', 'w') as f:
            status_line = f.read()
    except Exception as e:
        status_line = e
    return render_template("index.html", title="Home", status_line=status_line)


@app.route("/map")
def map():
    folium_map = plotting.get_folium_map()
    return folium_map.get_root().render()

