__author__ = 'andrew'
from django.db import models
from django.contrib.auth.models import User


class UserProfile(User):
    birth_date = models.DateField()
    contacts = models.TextField(null=True)
    bio = models.TextField(null=True)

    def __str__(self):
        return "%s's profile" % self.user