__author__ = 'andrew'
from akoidan_bio.settings import HOST_ADDR
from django import template
register = template.Library()


@register.filter(name="render_admin_link")
def get_object_link(model_object):
    return '%s/admin/akoidan_bio/%s/%d' % (HOST_ADDR, model_object.__class__.__name__.lower(), model_object.pk)