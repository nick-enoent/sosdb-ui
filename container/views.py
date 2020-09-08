from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import Context, loader
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from sosgui import _log, settings
from sosgui.utils import template_render
import json
import sys

log = _log.MsgLog('container views')

#Handles templates
@login_required
def overview(request):
    return template_render('container/overview.html',
                           request,
                           'Containers')
