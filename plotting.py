import pandas as pd
import convert_to_df
import folium
import html
import pickle


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
    popup_html = f"<b><a target='_parent' href='/details?locale={df.loc[locale]['locale2']}'>{df.loc[locale]['name']}</a></b>"
    popup_html += "<table>"
    for index, value in series.items():
        if value > 0:
            popup_html += f"<tr><td style='padding: 0.2em; font-size: 1.2em;'>{index}</td>"
            popup_html += f"<td style='padding: 0.2em; font-size: 1.2em;'>{int(round(value, 2) * 100)}%</td></tr>"
    popup_html = popup_html + "</table>"
    return popup_html


def save_folium_map(csv_file="main.csv"):
    """
    Create a map using the available csv file with country data and save it to file.  
    """
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
        popup_html = create_popup_table(df, locale)
        popup = folium.Popup(html=popup_html)
        icon = folium.features.CustomIcon("circle.png", icon_size=(8, 8))
        folium.Marker(location=[lat, lon], icon=icon, popup=popup).add_to(m)

    folium.LayerControl().add_to(m)
    m.save('app/templates/map.html')
    return 1


if __name__ == "__main__":
    if save_folium_map():
        print('Plotting: Map created successfully.')
