from apscheduler.schedulers.blocking import BlockingScheduler
import collect_data
import convert_to_df

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=13)
def scheduled_job():
    print('This job is run every day at 3pm/Berlin to grab \
        the data and refresh the DataFrame.')
    collect_data.collect_data()
    convert_to_df.create_df_for_plotting()

sched.start()