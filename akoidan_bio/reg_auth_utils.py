from django.core.exceptions import ValidationError

__author__ = 'andrew'
import re
from akoidan_bio.models import UserProfile


def validate_user(username):
    """
    Checks if specified username is free to register
    :return: False if user is valid, Error with specified message if not.
    """
    if username is None or username == '':
        raise ValidationError("User name can't be empty")
    if len(username) > 16:
        raise ValidationError("User is too long. Max 16 symbols")
    if not re.match('^[A-Za-z0-9-_]*$', username):
        raise ValidationError("Only letters, numbers, dashes or underlines")
    try:
        # theoretically can throw returning 'more than 1' error
        UserProfile.objects.get(login=username)
        raise ValidationError("This user name already used")
    except UserProfile.DoesNotExist:
        pass


def validate_password(password):
    if password is None or password == '':
        raise ValidationError("password can't be empty")