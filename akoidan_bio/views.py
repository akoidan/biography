from django.shortcuts import render_to_response
from akoidan_bio.forms import UserProfileForm
from akoidan_bio.models import UserProfile

__author__ = 'andrew'


def home(request):
    if request.method == 'GET':
        form = UserProfileForm(UserProfile.objects.all())
        return render_to_response("akoidan_bio/home.html", {'form': form})