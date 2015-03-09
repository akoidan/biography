__author__ = 'andrew'
import json
from akoidan_bio import models


class RequestMiddleware(object):
    """
    Saves every request to database
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        setattr(request, 'hide_post', view_kwargs.pop('hide_post', False))

    def process_request(self, request):
        if request.path.endswith('/favicon.ico'):
            return request
        if hasattr(request, 'user') and not request.user.is_anonymous():
            user = request.user
        else:
            user = None

        meta = request.META.copy()
        meta.pop('QUERY_STRING', None)
        meta.pop('HTTP_COOKIE', None)

        if 'HTTP_X_FORWARDED_FOR' in meta:
            remote_addr_fwd = meta['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
            if remote_addr_fwd == meta['HTTP_X_FORWARDED_FOR']:
                meta.pop('HTTP_X_FORWARDED_FOR')

        models.Request(
            host=request.get_host(),
            path=request.path,
            method=request.method,
            user_agent=meta.pop('HTTP_USER_AGENT', None),
            remote_addr=meta.pop('REMOTE_ADDR', None),
            meta=meta,
            cookies=request.COOKIES,
            user=user
        ).save()