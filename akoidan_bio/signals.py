from django.db.models.signals import post_save, post_delete
from akoidan_bio.models import UserProfile, Request, DatabaseLog, Actions


def get_action(created):
    if created is None:
        return Actions.delete
    elif created is True:
        return Actions.create
    else: # if created is False
        return Actions.update


def log(sender, instance, created=None,  *args, **kwargs):
    """
    :param created: None when called from post_delete (set to default)
                    True when a new raw is inserted called from post_save
                    False when a raw is updated called from post_save
    """
    # get object from the database if action is update and creates it if delete or create
    log, created = DatabaseLog.objects.get_or_create(table=sender._meta.db_table, object_id=instance.id, action=get_action(created))
    # updates time field is object is action is update, saves it if delete or create
    log.save()


post_save.connect(log, sender=UserProfile)
post_save.connect(log, sender=Request)

post_delete.connect(log, sender=UserProfile)
post_delete.connect(log, sender=Request)