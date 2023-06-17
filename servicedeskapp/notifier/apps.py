from django.apps import AppConfig


class NotifierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifier'

    def ready(self):
        from notifier.notifier import start
        start()
