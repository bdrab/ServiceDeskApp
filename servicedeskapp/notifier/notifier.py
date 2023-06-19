from apscheduler.schedulers.background import BackgroundScheduler
from incident.models import Notification
import requests


def new_notifications():
    all_notifications = Notification.objects.all().filter(has_been_sent=False)

    if all_notifications:
        for notification in all_notifications:
            phones = list(filter(lambda x: x is not None,
                                 [user.profile.phone_number
                                  for user in notification.inc.assignment_group.members.all()]))

            phones_string = " ".join(phones)
            # workaround to stop sending 2 SMSs in developing mode.
            notification.has_been_sent = True
            notification.save()

            data = {"text": "New INC has been assigned to your queue.Please check it.",
                    "phones": phones_string}

            new_request = requests.post("http://192.168.0.130/sms", data=data)

            if new_request.status_code != 200:
                notification.has_been_sent = False
                notification.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(new_notifications, 'interval', minutes=1)
    scheduler.start()
