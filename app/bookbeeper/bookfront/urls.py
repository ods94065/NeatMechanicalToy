from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^old/index$', login_required(TemplateView.as_view(template_name='bookfront/index.html')),
        name='bookfront-home'),
    url(r'^old/login$', 'django.contrib.auth.views.login', {'template_name': 'bookfront/login.html'},
        name='bookfront-login'),
    url(r'^old/logout$', 'django.contrib.auth.views.logout', {'template_name': 'bookfront/logout.html'},
        name='bookfront-logout')
)
