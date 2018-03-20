from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
import json
import sys
import settings, logging

log = logging.MsgLog('sosgui_views')

#Handles templates
@login_required
def home(request):
    try:
        ldms_nav = False
        baler_nav = False
        if 'ldms_control' in settings.INSTALLED_APPS:
            ldms_nav = True
        if 'balerd' in settings.INSTALLED_APPS:
            baler_nav = True
	return render_to_response('index.html', { "ldms_nav" : ldms_nav, "baler_nav" : baler_nav, "template_name": "OVIS Monitoring GUI" })
    except Exception, e:
	log.write(repr(e)+'\n')
	raise Http404

