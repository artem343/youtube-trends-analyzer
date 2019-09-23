import pandas as pd
import convert_to_df
import folium
import html


def get_folium_map(csv_file="main.csv"):
    state_geo = "world-countries.json"
    df = pd.read_csv(csv_file)
    state_data = df

    columns = df.columns[5:]

    m = folium.Map(location=[0, 0], zoom_start=2, min_zoom=2, max_zoom=5)

    for cur_column in columns:
        chlor = folium.Choropleth(
            geo_data=state_geo,
            name=cur_column,
            data=state_data,
            columns=["locale3", cur_column],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            nan_fill_opacity=0.2,
            line_opacity=0.2,
            #         legend_name=f'{cur_column} %',
            nan_fill_color="grey",
            highlight=True,
            overlay=True,
            show=False,
        )
        # Remove legends
        for key in chlor._children:
            if key.startswith("color_map"):
                del chlor._children[key]
        chlor.add_to(m)

    for lat, lon, locale in zip(df.lat_avg, df.lon_avg, df.index):
        popup_html = f"<b>{df.loc[locale]['name']}</b>"
        popup_html += "<table border=1>"
        for cur_column in columns:
            val = df.loc[locale][cur_column]
            if val > 0:
                popup_html += f"<tr><td>{cur_column}</td>"
                popup_html += f"<td>{round(val, 2)}</td></tr>"
        popup_html = popup_html + "</table>"

        popup = folium.Popup(html=popup_html)
        icon = folium.features.CustomIcon("circle.png", icon_size=(8, 8))
        folium.Marker(location=[lat, lon], icon=icon, popup=popup).add_to(m)

    # folium.Marker([26.80,80.76],popup=html.escape("Hey!")).add_to(m)

    folium.LayerControl(autoZIndex=False, collapsed=False).add_to(m)
    # save map in this line if needed
    return m


if __name__ == "__main__":
    map_html = get_folium_map()
