__author__ = 'andrew'
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ImageField, DateField
from django import forms
from akoidan_bio.models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    A form that provides a way to edit UserProfile
    """
    birth_date = DateField()
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