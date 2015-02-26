__author__ = 'andrew'
from django.db.models import Model
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, UserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(login=username)
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return '%s %s' % (self.name, self.surname)

    login = models.CharField(max_length=30, blank=True, unique=True)
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    objects = MyUserManager()
    birth_date = models.DateField(null=True, blank=True)
    contacts = models.TextField(null=True)
    bio = models.TextField(null=True)

    USERNAME_FIELD = 'login'


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
    user = models.ForeignKey(UserProfile, blank=True, null=True)
