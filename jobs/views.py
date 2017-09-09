from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from sosgui import logging
import json
import sys

log = logging.MsgLog("job_view")

#Handles templates
@login_required
def index(request):
    try:
	return render_to_response('jobs/index.html', {})
    except Exception, e:
	log.write(e)
	raise Http404

def job_graph(request):
    try:
        return render_to_response('jobs/metric_graph.html', {})
    except Exception as e:
        log.write(e)
        raise Http404

