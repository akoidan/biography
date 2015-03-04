from django.forms import ImageField, DateField

__author__ = 'andrew'
from django import forms
from akoidan_bio.models import UserProfile, Request
from django.forms.extras.widgets import SelectDateWidget


class UserProfileReadOnlyForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('name', 'surname', 'birth_date', 'contacts', 'bio')


class UserProfileForm(forms.ModelForm):

    birth_date = DateField(widget=SelectDateWidget(years=range(1950, 2006)))
    # the widget gets rid of <a href=
    photo = ImageField(widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('surname', 'birth_date', 'contacts', 'bio', 'photo')


class RequestsForm(forms.ModelForm):
    """Base class for making a form readonly."""

    class Meta:
        model = Request