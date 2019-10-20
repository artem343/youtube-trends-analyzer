from apscheduler.schedulers.blocking import BlockingScheduler
import collect_data
import convert_to_df
import plotting
from datetime import datetime

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=18, minute=55, timezone='EST')
def scheduled_job():
    # This job is run every day to grab the data and refresh the DataFrame
    with open('status.txt', 'w') as f:
        f.write(
            f"Data collected on {datetime.now().strftime('%d.%m.%Y at %H:%M')}")
    collect_data.collect_data()
    convert_to_df.create_df_for_plotting()
    plotting.save_folium_map()

sched.start()
