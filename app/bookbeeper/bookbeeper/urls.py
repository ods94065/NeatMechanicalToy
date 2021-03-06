from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from bookservices import views
from django.conf.urls import include
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/library/$',views.LibraryBookList.as_view()),
    url(r'^api/library/(?P<pk>[0-9]{13})/$',views.LibraryBookIndividual.as_view()),
    url(r'^api/library/import/(?P<pk>[0-9]{13})/$', views.LibraryBookImporterView.as_view()),
    url(r'^api/store/$',views.StoreList.as_view()),
    url(r'^api/store/(?P<pk>[0-9]+)/$',views.StoreIndividual.as_view()),
    url(r'^api/inventory/$',views.InventoryList.as_view()),
    url(r'^api/inventory/(?P<pk>[0-9]+)/$',views.InventoryIndividual.as_view()),
    url(r'^api/userToStore/$',views.StoreToUserList.as_view()),
    url(r'^api/userToStore/(?P<pk>[0-9]+)/$',views.StoreToUserIndividual.as_view()),
    url(r'^api/users/$', views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$',views.UserIndividual.as_view())
)
urlpatterns += patterns('',
                        url(r'^api-auth',include('rest_framework.urls',namespace='rest_framework')),
                        )
urlpatterns = format_suffix_patterns(urlpatterns)