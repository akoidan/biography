import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from akoidan_bio.forms import UserProfileReadOnlyForm, RequestsForm, UserProfileForm
from akoidan_bio.models import UserProfile, Request
from django.http import Http404
from akoidan_bio.settings import REQUESTS_COUNT, DEFAULT_PROFILE_ID
from django.contrib.auth import get_user_model
__author__ = 'andrew'


def create_login_out_page(request, c):
    if request.user.is_authenticated():
        page = 'akoidan_bio/logout.html'
        c.update({'username': request.user.login})
    else:
        page = 'akoidan_bio/registerAndLogin.html'
    c.update({'log_in_out_page': page})


def create_form_page(request, c):
    if request.user.is_authenticated():
        try:
            user_profile = UserProfile.objects.get(pk=request.user.id)
            form = UserProfileForm(instance=user_profile)
            # csrf is already set in nested home method
        except ObjectDoesNotExist:
            form = UserProfileForm()
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


def home(request):
    params = csrf(request)
    create_login_out_page(request, params)
    create_form_page(request, params)
    return render_to_response("akoidan_bio/home.html", params)


def requests(request):
    RequestsFormSet = modelformset_factory(Request, form=RequestsForm)
    form = RequestsFormSet(queryset=Request.objects.all().order_by('-pk')[:REQUESTS_COUNT])
    return render_to_response("akoidan_bio/requests.html", {'formset': form})


def change_form(request):
    if request.method == 'POST' and request.user.is_authenticated():
        user_profile = UserProfile.objects.get(pk=request.user.id)
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            # TODO USER ID
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("sorry, form is not valid", content_type='text/plain')

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
            return HttpResponseRedirect("form")
        else:
            message = "Login or password is wrong"
        return HttpResponse(message, content_type='text/plain')
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
            authenticate(username=username, password=password)
            return HttpResponse("you successfully registered", content_type='text/plain')
        return HttpResponse(message, content_type='text/plain')
    else:
        raise Http404


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
