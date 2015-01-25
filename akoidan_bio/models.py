__author__ = 'andrew'
from django.db.models import Model
from django.db import models
from django.contrib.auth.models import User


class UserProfile(User):
    birth_date = models.DateField()
    contacts = models.TextField(null=True)
    bio = models.TextField(null=True)

    def __str__(self):
        return "%s's profile" % self.user


class Request(Model):
    time = models.DateTimeField(auto_now_add=True)
    host = models.CharField(max_length=1000)
    path = models.CharField(max_length=1000)
    method = models.CharField(max_length=50)
    user_agent = models.CharField(max_length=1000, blank=True, null=True)
    remote_addr = models.IPAddressField()
    # remote_addr_fwd = models.IPAddressField(blank=True, null=True)
    meta = models.TextField()
    cookies = models.TextField(blank=True, null=True)
    # get = models.TextField(blank=True, null=True)
    # post = models.TextField(blank=True, null=True)
    is_secure = models.NullBooleanField()
    is_ajax = models.NullBooleanField()
    user = models.ForeignKey(User, blank=True, null=True)
