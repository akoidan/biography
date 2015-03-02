from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView
from akoidan_bio import settings

PHOTO_URL='photos/'

urlpatterns = patterns(
    '',
    url(r'^$', 'akoidan_bio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'auth', 'akoidan_bio.views.auth'),
    url(r'request', 'akoidan_bio.views.requests'),
    # TODO
    # url(r'^favicon\.ico$', lambda x: HttpResponseRedirect(settings.STATIC_URL+'favicon.ico')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^form/', 'akoidan_bio.views.change_form'),
    url(r'^register', 'akoidan_bio.views.register'),
    url(r'^logout/$', 'akoidan_bio.views.log_out'),
)
