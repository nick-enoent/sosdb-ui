from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import Context, loader
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .utils import template_render
import json
import sys
from . import settings, _log

log = _log.MsgLog('sosgui_views')

#Handles templates
@login_required
def home(request):
    return template_render('index.html', request, 'OVIS Monitoring GUI')
