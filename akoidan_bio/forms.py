from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django.contrib.admin import widgets

__author__ = 'andrew'
from django.forms import ImageField, DateField
from django import forms
from akoidan_bio.models import UserProfile, Request
from django.forms.extras.widgets import SelectDateWidget

class CalendarWidget(forms.TextInput):
    def _media(self):
        return forms.Media(css={'all': ('pretty.css',)},
                           js=('animations.js', 'actions.js'))
    media = property(_media)

class UserProfileForm(forms.ModelForm):
    """
    A form that provides a way to edit UserProfile
    """
    # TODO datepicker widget
    birth_date = DateField(widget=SelectDateWidget(years=range(1950, 2006)))
    # the widget gets rid of <a href=
    photo = ImageField(widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('name', 'surname', 'birth_date', 'contacts', 'bio', 'photo')


    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_action = '/form'

        self.helper.add_input(Submit('Save', 'Save'))
        super(UserProfileForm, self).__init__(*args, **kwargs)