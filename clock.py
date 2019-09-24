from apscheduler.schedulers.blocking import BlockingScheduler
import collect_data
import convert_to_df
from datetime import datetime

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=13)
def scheduled_job():
    print('This job is run every day at 3pm/Berlin to grab \
        the data and refresh the DataFrame.')
    collect_data.collect_data()
    convert_to_df.create_df_for_plotting()
    with open('app/static/status.txt', 'w') as f:
        f.write(f"Data collected on {datetime.now().strftime('%d-%m-%Y at %H:%M')}")

sched.start()