__author__ = 'andrew'

import uuid
from django.db.models import Model, TextField, DateField, CharField, DateTimeField, IPAddressField, \
    NullBooleanField, ForeignKey, ImageField, PositiveIntegerField
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    """
    implementing UserProfile create, auth etc,
    """
    def create_user(self, username, password=None):
        user = self.model(login=username)
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    def get_short_name(self):
        return self.name

    def get_file_path(instance, filename):
        """
        :param instance: an instance of the being created file
        :param filename base string for generated name
        :return: a unique string filename
        """
        ext = filename.split('.')[-1]
        return "%s.%s" % (uuid.uuid4(), ext)

    def get_full_name(self):
        return '%s %s' % (self.name, self.surname)

    @property
    def is_staff(self):
        # every registered user can edit database
        return True #self.pk == DEFAULT_PROFILE_ID

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    login = CharField(max_length=30, blank=True, unique=True)
    name = CharField(max_length=30, blank=True)
    surname = CharField(max_length=30, blank=True)

    # specifies a custom create_user method
    objects = MyUserManager()

    birth_date = DateField(null=True, blank=True)
    contacts = TextField(null=True)
    bio = TextField(null=True)
    # fileField + <img instead of ImageField (removes preview link)
    photo = ImageField(upload_to=get_file_path)

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


class DatabaseLog(Model):

    TABLE_CHOICES = (
        (UserProfile._meta.db_table, UserProfile.__name__),
        (Request._meta.db_table, Request.__name__),
    )

    ACTION_CHOICES = (
        ('d', 'delete'),
        ('c', 'create'),
        ('u', 'update'),
    )

    table = CharField(choices=TABLE_CHOICES, max_length=20)
    time = DateTimeField(auto_now_add=True)
    object_id = PositiveIntegerField()
    action = CharField(max_length=1, choices=ACTION_CHOICES)

    class Meta:
        # only 1 create, 1 update and 1 delete per object
        unique_together = ('table', 'object_id', 'action')


