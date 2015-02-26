__author__ = 'andrew'
from django import forms
from akoidan_bio.models import UserProfile, Request
from django.forms.extras.widgets import SelectDateWidget


class UserProfileReadOnlyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'surname', 'birth_date', 'contacts', 'bio')

    """Base class for making a form readonly."""
    def __init__(self, *args, **kwargs):
        from django.utils.translation import ugettext as _
        from django.forms.widgets import Select
        super(UserProfileReadOnlyForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].label = _(self.fields[f].label)
            if isinstance(self.fields[f].widget, Select):
                self.fields[f].widget.attrs['disabled'] = 'disabled'
            else:
                self.fields[f].widget.attrs['readonly'] = 'readonly'


class UserProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=SelectDateWidget(years=range(1950, 2006)))
    class Meta:
        model = UserProfile
        fields = ('name', 'surname', 'birth_date', 'contacts', 'bio')


class RequestsForm(forms.ModelForm):
    """Base class for making a form readonly."""
    def __init__(self, *args, **kwargs):
        from django.utils.translation import ugettext as _
        from django.forms.widgets import Select
        super(RequestsForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].label = _(self.fields[f].label)
            if isinstance(self.fields[f].widget, Select):
                self.fields[f].widget.attrs['disabled'] = 'disabled'
            else:
                self.fields[f].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Request