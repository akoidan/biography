__author__ = 'andrew'
import re
from akoidan_bio.models import UserProfile


def validate_user(username):
    """
    Checks if specified username is free to register
    :return: False if user is valid, Error with specified message if not.
    """
    if username is None or username == '':
        return "User name can't be empty"
    elif len(username) > 16:
        return "User is too long. Max 16 symbols"
    if not re.match('^[A-Za-z0-9-_]*$', username):
        return "Only letters, numbers, dashes or underlines"
    try:
        # theoretically can throw returning 'more than 1' error
        UserProfile.objects.get(login=username)
        return 'This user name already used'
    except UserProfile.DoesNotExist:
        return False
