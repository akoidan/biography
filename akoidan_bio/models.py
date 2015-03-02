from django.core.files.storage import FileSystemStorage

__author__ = 'andrew'
import os
import uuid
from akoidan_bio.settings import PHOTO_DIRECTORY
from django.db.models import Model, TextField, DateField, CharField, DateTimeField, IPAddressField, \
    NullBooleanField, ForeignKey, ImageField, FileField
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(login=username)
        user.set_password(password)
        user.save(using=self._db)
        return user


photo_storage = FileSystemStorage(location=PHOTO_DIRECTORY)


class UserProfile(AbstractBaseUser):
    def get_short_name(self):
        return self.name

    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join(PHOTO_DIRECTORY, filename)

    def get_full_name(self):
        return '%s %s' % (self.name, self.surname)

    login = CharField(max_length=30, blank=True, unique=True)
    name = CharField(max_length=30, blank=True)
    surname = CharField(max_length=30, blank=True)
    objects = MyUserManager()
    birth_date = DateField(null=True, blank=True)
    contacts = TextField(null=True)
    bio = TextField(null=True)
    # fileField + <img instead of ImageField (removes preview link)
    photo = FileField(storage=photo_storage)

    USERNAME_FIELD = 'login'


class Request(Model):
    time = DateTimeField(auto_now_add=True)
    host = CharField(max_length=1000)
    path = CharField(max_length=1000)
    method = CharField(max_length=50)
    user_agent = CharField(max_length=1000, blank=True, null=True)
    remote_addr = IPAddressField()
    # remote_addr_fwd = IPAddressField(blank=True, null=True)
    meta = TextField()
    cookies = TextField(blank=True, null=True)
    # get = TextField(blank=True, null=True)
    # post = TextField(blank=True, null=True)
    is_secure = NullBooleanField()
    is_ajax = NullBooleanField()
    user = ForeignKey(UserProfile, blank=True, null=True)
