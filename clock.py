from apscheduler.schedulers.blocking import BlockingScheduler
import collect_data
import create_df_for_plotting
import plotting
from datetime import datetime


def update_data():
    """
    Download new videos, analyze them and create a map.
    """
    collect_data.collect_data()
    create_df_for_plotting.create_df_for_plotting()
    plotting.save_folium_map()


sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun',
                     hour=19, minute=30, timezone='MSK')
def scheduled_job():
    # This job is run every day to grab the data and refresh the DataFrame
    update_data()
    with open('status.txt', 'w') as f:
        f.write(f"Data collected on \
                {datetime.now().strftime('%d.%m.%Y')}")


sched.start()
