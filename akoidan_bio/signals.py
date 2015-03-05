from django.db.models.signals import post_save
from akoidan_bio.models import UserProfile, Request, DatabaseLog


def send_update(sender, instance, created, **kwargs):
    log = DatabaseLog(table=sender.__name__, object_id = instance.id, action='create')
    log.save()


post_save.connect(send_update, sender=UserProfile)
post_save.connect(send_update, sender=Request)