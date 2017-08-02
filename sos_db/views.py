from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from models import SosDir, SosContainer, SosSchema, SosTable
from sosgui import logging
import json
import sys

log = logging.MsgLog("sosdb_views")

def directory(request):
    try:
	d = SosDir()
	d = json.dumps(d)
	return HttpResponse(d, content_type="text/json")
    except Exception as e:
	log.write(e)
	return HttpResponse('{ "directory" : [] }', content_type="text/json")

def container(request):
    try:
	s = SosContainer()
	c = s.GET(request)
	c = json.dumps(c)
	return HttpResponse(c, content_type="text/json")
    except Exception as e:
	log.write('container: '+repr(e))
	return HttpResponse('Null')

def schema(request):
    try:
        s = SosSchema()
        b = s.GET(request)
        b = json.dumps(b)
        return HttpResponse(b, content_type="text/json")
    except Exception as e:
        log.write('schema: '+repr(e)+'\n')
        return HttpResponse('Schema' + repr(e))

def query(request):
    try:
        s = SosTable()
        t = s.GET(request)
        log.write('query ret: '+repr(t))
        t = json.dumps(t)
        return HttpResponse(t, content_type="text/json")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log.write('Exception: '+repr(e)+' Line_no: '+repr(exc_tb.tb_lineno)+'\n')
	return HttpResponse(repr(e))
