from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from utils import template_render
import json
import sys
import settings, logging

log = logging.MsgLog('sosgui_views')

#Handles templates
@login_required
def home(request):
    return template_render('index.html', request, 'OVIS Monitoring GUI')
