"""sosgui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from __future__ import absolute_import
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.urls import path
from django.views.generic import TemplateView
from django.contrib import admin
from . import settings
from . import views
from . import _log

log = _log.MsgLog('sosgui.urls')

urlpatterns = [
    url(r'^$', views.home),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^container/', include('container.urls')),
    url(r'^sos_db/', include('sos_db.urls')),
    url(r'^objbrowser/', include('objbrowser.urls')),
    url(r'^jobs/', include('jobs.urls')),
]
if 'grafana' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^grafana/', include('grafana.urls')))
else:
    _log.write('no grafana')
    pass
if 'balerd' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^balerd/', include('balerd.urls')))
    urlpatterns.append(url(r'^heatpattern/', include('heatpattern.urls')))
    urlpatterns.append(url(r'^msg_browser/', include('msg_browser.urls')))
    urlpatterns.append(url(r'^ptn_browser/', include('ptn_browser.urls')))
    urlpatterns.append(url(r'^tkn_browser/', include('tkn_browser.urls')))
    urlpatterns.append(url(r'^opie/', include('opie.urls')))
    urlpatterns.append(url(r'^heatmap/', include('heatmap.urls')))
else:
    pass
if 'ldms_control' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^ldms/', include('ldms_control.urls')))
    urlpatterns.append(url(r'^ldms_err/', include('ldms_err.urls')))
else:
    pass
