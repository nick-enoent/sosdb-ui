import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from sosgui import logging, settings
from sosgui.utils import template_render
import json
import sys

log = logging.MsgLog("objbrowser_views")

@login_required
def index(request):
    return template_render('objbrowser/index.html',
                           request,
                           'Object Browser')
