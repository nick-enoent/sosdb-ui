from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^directory/$', views.directory),
    #url(r'^info/$', views.info),
    url(r'^container/.*$', views.container),
    url(r'^schema/.*$', views.schema),
    url(r'^query/.*$', views.query),
]
