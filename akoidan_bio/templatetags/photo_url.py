from akoidan_bio.urls import PHOTO_URL

__author__ = 'andrew'

from django import template
register = template.Library()

# TODO
@register.tag(name="photo")
def get_photo_url(base_url, taken):
    return PHOTO_URL + base_url

