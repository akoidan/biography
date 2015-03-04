__author__ = 'andrew'
import re
from django.core.exceptions import ObjectDoesNotExist
from akoidan_bio.forms import UserProfileForm, UserProfileReadOnlyForm
from akoidan_bio.models import UserProfile
from akoidan_bio.settings import DEFAULT_PROFILE_ID


def validate_user(username):
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


def create_form_page(request, c):
    if request.user.is_authenticated():
        try:
            user_profile = UserProfile.objects.get(pk=request.user.id)
            form = UserProfileForm(instance=user_profile, empty_permitted=True)
            # csrf is already set in nested home method
        except ObjectDoesNotExist:
            user_profile = None
            form = UserProfileForm(empty_permitted=True)
        c['user'] = user_profile
        page = 'akoidan_bio/change_form.html'
    else:
        try:
            user_profile = UserProfile.objects.get(pk=DEFAULT_PROFILE_ID)
            form = UserProfileReadOnlyForm(instance=user_profile)
        except UserProfile.DoesNotExist:
            form = UserProfileReadOnlyForm()
        page = 'akoidan_bio/read_form.html'
    c.update({'form': form})
    c.update({'form_page': page})