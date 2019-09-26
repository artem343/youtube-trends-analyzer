from flask import render_template, request
from app import app
import plotting
import os


@app.route("/")
@app.route("/index")
def index():
    try:
        with open('status.txt', 'r') as f:
            status_line = f.read()
    except Exception as e:
        status_line = e
    return render_template("index.html", title="Home", status_line=status_line)


@app.route("/map")
def map():
    folium_map = plotting.get_folium_map()
    return folium_map.get_root().render()


@app.route("/details", methods=['GET'])
def details():
    locale = request.args.get('locale')
    df_locale, df_grouped = plotting.get_details(locale)
    return render_template(
        "details.html",
        title="Details",
        locale=locale, 
        df_locale=df_locale,
        df_grouped=df_grouped
        )

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')