from akoidan_bio.urls import PHOTO_URL

__author__ = 'andrew'

from django import template
register = template.Library()

# TODO
@register.simple_tag(name="photo")
def get_photo_url(param1):
    return PHOTO_URL + param1[2:]

