from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from models import SosDir, SosContainer, SosSchema, SosTable
from sosgui import logging
import json
import sys

log = logging.MsgLog("sosdb_views")

def directory(request):
    if request.user.is_authenticated:
        try:
            d = SosDir()
            d['authenticated'] = True
            d = json.dumps(d)
            return HttpResponse(d, content_type="text/json")
        except Exception as e:
            log.write(e)
            return HttpResponse('{ "directory" : [] }', content_type="text/json")
    else:
        resp = {}
        resp['authenticated'] = False
        return HttpResponse(json.dumps(resp), content_type="text/json")

def container(request):
    if request.user.is_authenticated:
        try:
            s = SosContainer()
            c = s.GET(request)
            c['authenticated'] = True
            c = json.dumps(c)
            return HttpResponse(c, content_type="text/json")
        except Exception as e:
            log.write('container: '+repr(e))
            return HttpResponse('Null')
    else:
        resp = {}
        resp['authenticated'] = False
        return HttpResponse(json.dumps(resp), content_type="text/json")

def schema(request):
    if request.user.is_authenticated:
        try:
            s = SosSchema()
            b = s.GET(request)
            b['authenticated'] = True
            b = json.dumps(b)
            return HttpResponse(b, content_type="text/json")
        except Exception as e:
            log.write('schema: '+repr(e)+'\n')
            return HttpResponse('Schema' + repr(e))
    else:
        resp = {}
        resp['authenticated'] = False
        return HttpResponse(json.dumps(resp), content_type="text/json")

def query(request):
    if request.user.is_authenticated:
        try:
            s = SosTable()
            t = s.GET(request)
            t['authenticated'] = True
            t = json.dumps(t)
            return HttpResponse(t, content_type="text/json")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            log.write('Exception: '+repr(e)+' Line_no: '+repr(exc_tb.tb_lineno)+'\n')
	    return HttpResponse(repr(e))
    else:
        resp = {}
        resp['authenticated'] = False
        return HttpResponse(json.dumps(resp), content_type="text/json")

def insert(request):
    if request.user.is_authenticated:
        try:
            s = SosTable()
            resp = s.INSERT(request)
            resp['authenticated'] = True
            t = json.dumps(resp)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            log.write('Insert Obj Exception: '+repr(e)+' Line_no: '+repr(exc_tb.tb_lineno)+'\n')
	    return HttpResponse(repr(e))
    else:
        resp = {}
        resp['authenticated'] = False
        return HttpResponse(json.dumps(resp), content_type="text/json")
