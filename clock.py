import collect_data
import create_df_for_plotting
import plotting
import datetime


def register_update():
    with open('status.txt', 'w') as f:
        f.write(
            f'Data collected on {datetime.datetime.now().strftime("%d.%m.%Y")}')


def update_data():
    """
    Download new videos, analyze them and create a map.
    """
    collect_data.collect_data()
    create_df_for_plotting.create_df_for_plotting()
    plotting.save_folium_map()
    register_update()


if __name__ == "__main__":
    update_data()
