from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from sosgui import logging, settings
import json
import sys

log = logging.MsgLog("objbrowser_views")

def index(request):
	try:
		ldms_nav = False
		if 'ldms_control' in settings.INSTALLED_APPS:
			ldms_nav = True
		return render_to_response('objbrowser/index.html', {"ldms_nav" : ldms_nav})
	except Exception as e:
		log.write(e)
		raise Http404
