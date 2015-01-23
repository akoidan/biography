import json
from django.contrib.auth.models import User
from akoidan_bio import models

__author__ = 'andrew'


def dumps(value):
    if value is None:
        return None
    else:
        return json.dumps(value, default=lambda o: None)


class RequestMiddleware(object):
    """
    http://stackoverflow.com/questions/5609924/django-saving-the-whole-request-for-statistics-whats-available
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        setattr(request, 'hide_post', view_kwargs.pop('hide_post', False))

    def process_request(self, request):
        if request.path.endswith('/favicon.ico'):
            return request
        if hasattr(request, 'user'):
            user = request.user if type(request.user) == User else None
        else:
            user = None

        meta = request.META.copy()
        meta.pop('QUERY_STRING', None)
        meta.pop('HTTP_COOKIE', None)
        remote_addr_fwd = None

        if 'HTTP_X_FORWARDED_FOR' in meta:
            remote_addr_fwd = meta['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
            if remote_addr_fwd == meta['HTTP_X_FORWARDED_FOR']:
                meta.pop('HTTP_X_FORWARDED_FOR')

        post = None
        uri = request.build_absolute_uri()
        if request.POST and uri != '/login/':
            post = dumps(request.POST)

        models.Request(
            host=request.get_host(),
            path=request.path,
            method=request.method,
            uri=request.build_absolute_uri(),
            user_agent=meta.pop('HTTP_USER_AGENT', None),
            remote_addr=meta.pop('REMOTE_ADDR', None),
            # remote_addr_fwd=remote_addr_fwd,
            meta=meta,
            cookies=request.COOKIES,
            # get=request.GET,
            # post=post,
            is_secure=request.is_secure(),
            is_ajax=request.is_ajax(),
            user=user
        ).save()