from akoidan_bio.urls import PHOTO_URL

__author__ = 'andrew'

from django import template
register = template.Library()


@register.filter(name="render_admin_link")
def get_object_link(object):
    return 'http://127.0.0.1:8000/admin/akoidan_bio/%s/%d' % (object.__class__.__name__.lower(), object.pk)

