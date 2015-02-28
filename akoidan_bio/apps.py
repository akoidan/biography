import os
from django.apps import AppConfig
from akoidan_bio.settings import PHOTO_DIRECTORY


class DefaultSettingsConfig(AppConfig):
    """
    Creates directory for storing uploaded photos
    """
    name = 'akoidan_bio'
    verbose_name = 'autobio'

    def ready(self):
        if not os.path.exists(PHOTO_DIRECTORY):
            os.mkdir(PHOTO_DIRECTORY)