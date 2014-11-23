from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

import bookfront.urls


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', include('bookservices.urls')),
)
urlpatterns += patterns('',
    url(r'^api-auth',include('rest_framework.urls',namespace='rest_framework')),
)
urlpatterns += bookfront.urls.urlpatterns

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^(?P<path>(?:js|css|img)/.*)$', 'serve')
    )
