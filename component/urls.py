from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    #url(r'^jobs/$', 'objbrowser.views.jobs', name='jobs'),
    #url(r'^SOS/directory/$', 'objbrowser.views.directory'),
    #url(r'^SOS/info/$', 'objbrowser.views.info'),
    #url(r'^SOS/container/[A-Za-z0-9-]+[ 0-9A-Za-z#$%=@!{},~&*()<>?.:;_|^/+\t\r\n\[\]"-]*$', 'objbrowser.views.container'),
    #url(r'^SOS/schema/[A-Za-z0-9-]+[ 0-9A-Za-z#$%=@!{},~&*()<>?.:;_|^/+\t\r\n\[\]"-]*$', 'objbrowser.views.schema'),
    #url(r'^request/[A-Za-z0-9-]+[ 0-9A-Za-z#$%=@!{},~&*()<>?.:;_|^/+\t\r\n\[\]"-]*$', 'objbrowser.views.ajax_request'),
    #url(r'^SOS/container/$', 'objbrowser.models.SosContainer'),
    #url(r'^SOS/schema/$', 'objbrowser.models.SosSchema'),
    #url(r'^SOS/graph/$', 'objbrowser.models.SosGraph'),
    #url(r'^SOS/directory', 'objbrowser.models.SosDir'),
]
