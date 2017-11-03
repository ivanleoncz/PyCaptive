#!/usr/bin/python3

""" Application main module. """

from app import app
from apscheduler.schedulers.background import BackgroundScheduler
from app.modules import scheduler

app.config.from_object('config')

if __name__ == "__main__":
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(scheduler.ses,'interval',seconds=60)
    sched.start()
    app.run(host="127.0.0.1",port=14900)
    
