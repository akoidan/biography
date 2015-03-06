__author__ = 'andrew'
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from akoidan_bio.forms import RequestsForm, UserProfileForm
from akoidan_bio.models import UserProfile, Request
from django.http import Http404
from akoidan_bio.reg_auth_utils import validate_user, create_form_page
from akoidan_bio.settings import REQUESTS_COUNT
from django.contrib.auth import get_user_model


def home(request):
    params = csrf(request)
    create_form_page(request, params)
    return render_to_response("akoidan_bio/home.html",
                              params,
                              context_instance=RequestContext(request))


def requests(request):
    RequestsFormSet = modelformset_factory(Request, form=RequestsForm)
    form = RequestsFormSet(queryset=Request.objects.all().order_by('-pk')[:REQUESTS_COUNT])
    return render_to_response("akoidan_bio/requests.html",
                              {'formset': form},
                              context_instance=RequestContext(request))


def change_form(request):
    if request.method == 'POST' and request.user.is_authenticated():
        user_profile = UserProfile.objects.get(pk=request.user.id)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return render_to_response("akoidan_bio/response.html",
                                      {'message': form.errors},
                                      context_instance=RequestContext(request))
    else:
        raise PermissionDenied


def auth(request):
    """
    POST only. Logs in into system.
    """
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            message = "Login or password is wrong"
        return render_to_response("akoidan_bio/response.html",
                                  {'message': message},
                                  context_instance=RequestContext(request))
    else:
        raise Http404


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        message = False
        if password is None or password == '':
            message = "Password can't be empty"
        if message is False:
            message = validate_user(username)
        if message is False:
            user = get_user_model().objects.create_user(username=username, password=password)
            user.save()
            authed_user = authenticate(username=username, password=password)
            # TODO UNIQUE constraint failed: akoidan_bio_databaselog.table,
            # akoidan_bio_databaselog.object_id, akoidan_bio_databaselog.action
            login(request, authed_user)
            message = 'you successfully registered'
        return render_to_response("akoidan_bio/response.html",
                                  {'message': message},
                                  context_instance=RequestContext(request))
    else:
        raise Http404