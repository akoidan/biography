__author__ = 'andrew'
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from akoidan_bio.forms import UserProfileForm
from akoidan_bio.models import UserProfile, Request
from django.http import Http404
from akoidan_bio.reg_auth_utils import validate_user
from akoidan_bio.settings import REQUESTS_COUNT, DEFAULT_PROFILE_ID
from django.contrib.auth import get_user_model


def home(request):
    """
    Displays UserProfile if user isn't logged
    provides a way to edit if logged
    """
    params = csrf(request)
    if request.user.is_authenticated():
        try:
            user_profile = UserProfile.objects.get(pk=request.user.id)
            params['form'] = UserProfileForm(instance=user_profile, empty_permitted=True)
            # csrf is already set in nested home method
        except ObjectDoesNotExist:
            user_profile = None
            params['form'] = UserProfileForm(empty_permitted=True)
        params['user'] = user_profile
        return render_to_response('akoidan_bio/change_form.html', params, context_instance=RequestContext(request))
    else:
        try:
            params['profile'] = UserProfile.objects.get(pk=DEFAULT_PROFILE_ID)
        except UserProfile.DoesNotExist:
            pass
        return render_to_response('akoidan_bio/read_form.html', params, context_instance=RequestContext(request))


def requests(request):
    """
    Shows last 10 requests page
    """
    last_requests = Request.objects.all().order_by('-pk')[:REQUESTS_COUNT]
    return render_to_response("akoidan_bio/requests.html",
                              {'requests': last_requests},
                              context_instance=RequestContext(request))


def change_form(request):
    """
    Accepts a UserProfileForm and saves it if it's validate
    """
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
    Logs in into system.
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
    """
    Accepts a Registration form and registers a new user if form is valid.
    """
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
            login(request, authed_user)
            message = 'you successfully registered'
        return render_to_response("akoidan_bio/response.html",
                                  {'message': message},
                                  context_instance=RequestContext(request))
    else:
        raise Http404