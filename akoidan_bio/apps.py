from django.apps import AppConfig


class DefaultSettingsConfig(AppConfig):
    """
    Creates directory for storing uploaded photos
    """
    name = 'akoidan_bio'
    verbose_name = 'autobio'

    def ready(self):
        # TODO init here
        pass