from django.shortcuts import render_to_response
from akoidan_bio.forms import UserProfileForm
from akoidan_bio.models import UserProfile

__author__ = 'andrew'


def home(request):
    if request.method == 'GET':
        # TODO remove hardcoded id
        form = UserProfileForm(instance=UserProfile.objects.get(id=1))
        return render_to_response("akoidan_bio/home.html", {'form': form})



