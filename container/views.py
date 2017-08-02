from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from sosgui import logging, settings
import json
import sys

log = open('/tmp/container_views','a')

#Handles templates
def overview(request):
    try:
        ldms_nav = False
        if 'ldms_control' in settings.INSTALLED_APPS:
            ldms_nav = True
	return render_to_response('container/overview.html', { 'ldms_nav' : ldms_nav })
    except Exception, e:
	log.write(repr(e)+'\n')
	raise Http404

