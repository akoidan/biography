from django.core.exceptions import ValidationError

__author__ = 'andrew'
import re
from akoidan_bio.models import UserProfile


def validate_user(username):
    """
    Checks if specified username is free to register
    :raises ValidationError exception if username is not valid
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
    """
    Checks if password is secure
    :raises ValidationError exception if password is not valid
    """
    if password is None or password == '':
        raise ValidationError("password can't be empty")
    if len(password) < 3:
        raise ValidationError("password should be at least 3 symbols")