__author__ = 'andrew'
from django.core.management import BaseCommand
from django.db import models


class Command(BaseCommand):
    help = 'Prints all project models and counts objects in the each one'

    can_import_settings = True

    def handle(self, *args, **options):
        all_models = models.get_models(include_auto_created=True)
        for member in all_models:
            output = '%s has %d objects' % (member.__name__, member.objects.count())
            self.stdout.write(output)
            self.stderr.write('error: %s' % output)