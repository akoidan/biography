from django.forms import modelformset_factory
from django.shortcuts import render_to_response
from akoidan_bio.forms import UserProfileForm, RequestsForm
from akoidan_bio.models import UserProfile, Request

__author__ = 'andrew'


def home(request):
    if request.method == 'GET':
        # TODO remove hardcoded id
        form = UserProfileForm(instance=UserProfile.objects.get(id=1))
        return render_to_response("akoidan_bio/home.html", {'form': form})

def requests(request):
    RequestsFormSet = modelformset_factory(Request, form=RequestsForm)
    form = RequestsFormSet(queryset=Request.objects.all().order_by('-pk')[:10])
    return render_to_response("akoidan_bio/requests.html", {'formset': form})


