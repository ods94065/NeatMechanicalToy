from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import base

import bookfront.urls


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', include('bookservices.urls')),
    url(r'^$', base.RedirectView.as_view(url='/index.html'))
)
urlpatterns += patterns('',
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
)
urlpatterns += bookfront.urls.urlpatterns

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^(?P<path>(?:js|css|img|fonts|libs|partials)/.*)$', 'serve'),
        url(r'^(?P<path>.*\.html)$', 'serve')
    )
