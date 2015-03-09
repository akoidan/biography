__author__ = 'andrew'
import json
from akoidan_bio import models


class RequestMiddleware(object):
    """
    Saves every request to database
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        setattr(request, 'hide_post', view_kwargs.pop('hide_post', False))

    def get_user(self, request):
        """
        :return: None if user is anonymous
        """
        if hasattr(request, 'user') and not request.user.is_anonymous():
            user = request.user
        else:
            user = None
        return user

    def get_meta(self, request):
        """
        meta information about passed request
        :return:
        """
        meta = request.META.copy()
        meta.pop('QUERY_STRING', None)
        meta.pop('HTTP_COOKIE', None)
        if 'HTTP_X_FORWARDED_FOR' in meta:
            remote_addr_fwd = meta['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
            if remote_addr_fwd == meta['HTTP_X_FORWARDED_FOR']:
                meta.pop('HTTP_X_FORWARDED_FOR')
        return meta

    def process_request(self, request):
        """
        :param request:
        :return:
        """
        if request.path.endswith('/favicon.ico'):
            return request

        meta = self.get_meta(request)

        models.Request(
            host=request.get_host(),
            path=request.path,
            method=request.method,
            user_agent=meta.pop('HTTP_USER_AGENT', None),
            remote_addr=meta.pop('REMOTE_ADDR', None),
            meta=meta,
            cookies=request.COOKIES,
            user=self.get_user(request)
        ).save()