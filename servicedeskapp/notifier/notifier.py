from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from incident.models import Notification
import json
import requests


def new_notifications():
    all_notifications = Notification.objects.all()

    data = json.dumps({"notifications": "ok"})
    print(all_notifications)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(new_notifications, 'interval', minutes=1)
    scheduler.start()
