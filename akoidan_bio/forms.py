from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

__author__ = 'andrew'
from django.forms import ImageField, DateField
from django import forms
from akoidan_bio.models import UserProfile, Request
from django.forms.extras.widgets import SelectDateWidget


class UserProfileReadOnlyForm(forms.ModelForm):
    """
    A form just to display UserProfile
    """
    class Meta:
        model = UserProfile
        fields = ('name', 'surname', 'birth_date', 'contacts', 'bio')


class UserProfileForm(forms.ModelForm):
    """
    A form that provides a way to edit UserProfile
    """
    birth_date = DateField(widget=SelectDateWidget(years=range(1950, 2006)))
    # the widget gets rid of <a href=
    photo = ImageField(widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('surname', 'birth_date', 'contacts', 'bio', 'photo')


class RequestsForm(forms.ModelForm):

    helper = FormHelper()
    helper.template = 'bootstrap/table_inline_formset.html'

    """Base class for making a form readonly."""

    class Meta:
        model = Request
        # all fields by default is deprecated so using fields specifying all
        # fields = ('time', 'host', 'path', 'method', 'user_agent', 'remote_addr', 'meta', 'is_secure', 'is_ajax', 'user')