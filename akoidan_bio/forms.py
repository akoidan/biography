__author__ = 'andrew'
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ImageField, CharField
from django import forms
from akoidan_bio.models import UserProfile
from string import Template


class ContactsWidget(forms.widgets.Textarea):
    """
    The simple widget that renders the same html as the default one
    """
    def render(self, name, value, attrs=None):
        html = Template("""
        <input class="textinput textInput" id="id_contacts" maxlength="100" name="contacts" type="text" value="$value">
        """)
        return mark_safe(html.substitute(value=value))


class UserProfileForm(forms.ModelForm):
    """
    A form that provides a way to edit UserProfile
    """
    # the widget gets rid of <a href=
    photo = ImageField(widget=forms.FileInput)
    contacts = CharField(widget=ContactsWidget)

    class Meta:  # pylint: disable=C1001
        model = UserProfile
        fields = ('name', 'surname', 'birth_date', 'contacts', 'bio', 'photo')

    def __init__(self, *args, **kwargs):
        """
        Creates the entire form for changing UserProfile.
        """
        self.helper = FormHelper()
        self.helper.form_action = '/form'

        self.helper.add_input(Submit('Save', 'Save'))
        super(UserProfileForm, self).__init__(*args, **kwargs)