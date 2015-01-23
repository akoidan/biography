__author__ = 'andrew'
from django import forms
from akoidan_bio.models import UserProfile, Request


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'birth_date', 'contacts', 'bio')

class RequestsForm(forms.ModelForm):
    class Meta:
        model = Request