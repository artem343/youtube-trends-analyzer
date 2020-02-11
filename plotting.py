import pandas as pd
import folium


def get_details(locale):
    """
    Create a dataframe for the details.
    """
    df = pd.read_csv('videos.csv')
    df_locale = df[df['locale'] == locale].copy()
    df_grouped = df_locale.groupby(
        'categories').count().sort_values(by='id', ascending=False)
    df_locale.fillna(0, inplace=True)
    df_locale = df_locale.astype({"likes": int, "dislikes": int})
    return df_locale, df_grouped


def create_popup_table(df, locale):
    """
    Provides html of a table to display inside the tooltip of a country.
    """
    series = df.loc[locale][5:].sort_values(ascending=False)
    popup_html = f"<b><a target='_parent' href='/details?locale={df.loc[locale]['locale2']}'>"
    popup_html += f"{df.loc[locale]['name']}</a></b>"
    popup_html += "<table>"
    for index, value in series.items():
        if value > 0:
            popup_html += f"<tr><td style='padding: 0.2em; font-size: 1.2em;'>{index}</td>"
            popup_html += f"<td style='padding: 0.2em; font-size: 1.2em;'>{int(round(value, 2) * 100)}%</td></tr>"
    popup_html = popup_html + "</table>"
    return popup_html


def save_folium_map(csv_file="main.csv"):
    """
    Create a map using the available csv file
    with country data and save it to file.
    """
    state_geo_file = "world-countries.json"
    df = pd.read_csv(csv_file)
    state_data = df

    columns = df.columns[5:]

    m = folium.Map(location=[0, 0], zoom_start=2, min_zoom=2, max_zoom=5)

    for cur_column in columns:
        chlor = folium.Choropleth(
            geo_data=state_geo_file,
            name=cur_column,
            data=state_data,
            columns=["locale3", cur_column],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            nan_fill_opacity=0.2,
            line_opacity=0.2,
            legend_name=f'%',
            nan_fill_color="grey",
            bins=[0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 1],
            highlight=False,
            overlay=False,
            show=False,
        )
        # Remove legends
        if not cur_column == columns[0]:
            for key in chlor._children:
                if key.startswith("color_map"):
                    del chlor._children[key]
        chlor.add_to(m)

    for lat, lon, locale in zip(df.lat_avg, df.lon_avg, df.index):
        popup_html = create_popup_table(df, locale)
        popup = folium.Popup(html=popup_html)
        icon = folium.features.CustomIcon("circle.png", icon_size=(8, 8))
        folium.Marker(location=[lat, lon], icon=icon, popup=popup).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    m.save('app/templates/map.html')
    with open('app/templates/map.html', 'r') as f:
        text = f.read()
    text = text.replace('"openstreetmap" : tile_layer',
                        '// "openstreetmap" : tile_layer', 1)
    with open('app/templates/map.html', 'w') as f:
        f.write(text)
    return 1


if __name__ == "__main__":
    if save_folium_map():
        print('Plotting: Map created successfully.')
