from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from bookservices import views


urlpatterns = patterns('',
    url(r'^library/$',views.LibraryBookList.as_view()),
    url(r'^library/(?P<pk>[0-9]{13})/$',views.LibraryBookIndividual.as_view()),
    url(r'^library/import/(?P<pk>[0-9]{13})/$', views.LibraryBookImporterView.as_view()),
    url(r'^store/$',views.StoreList.as_view()),
    url(r'^store/(?P<pk>[0-9]+)/$',views.StoreIndividual.as_view()),
    url(r'^inventory/$',views.InventoryList.as_view()),
    url(r'^inventory/(?P<pk>[0-9]+)/$',views.InventoryIndividual.as_view()),
    url(r'^userToStore/$',views.StoreToUserList.as_view()),
    url(r'^userToStore/(?P<pk>[0-9]+)/$',views.StoreToUserIndividual.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$',views.UserIndividual.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
