from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from httpproxy.views import HttpProxy
import urllib
import json
import sys
from models import JobPlotPng, CompPlotPng
from sosgui import logging

log = logging.MsgLog("PlotViews")

def parse_request(request):
    try:
        context = {}
        if 'container' in request.GET:
            container = str(request.GET['container'])
            context['container'] = urllib.unquote(container)
        else:
            raise ValueError()
        if 'schema' in request.GET:
            schema = str(request.GET['schema'])
            context['schema'] = urllib.unquote(schema)
        else:
            raise ValueError()
        if 'job_id' in request.GET:
            job_id = int(request.GET['job_id'])
            context['job_id'] = job_id
        elif 'comp_id' in request.GET:
            comp_id = str(request.GET['comp_id'])
            context['comp_id'] = comp_id
        elif 'component_id' in request.GET:
            comp_id = int(request.GET['component_id'])
            context['comp_id'] = comp_id
        else:
            raise ValueError()
        if 'metric_name' in request.GET:
            metric_name = str(request.GET['metric_name'])
            context['metric_name'] = urllib.unquote(metric_name)
        else:
            raise ValueError()
        if 'start' in request.GET:
            start = int(request.GET['start'])
            log.write(start)
        else:
            start = 0
        context['start'] = start
        if 'end' in request.GET:
            end = int(request.GET['end'])
        else:
            end = 0
        context['end'] = end
        if 'duration' in request.GET:
            duration = int(request.GET['duration'])
        else:
            duration = 3600
        context['duration'] = duration
        log.write(repr(request.GET))
        """
        context = {
            'container' : urllib.unquote(container),
            'schema' : urllib.unquote(schema),
            'job_id' : job_id,
            'comp_id' : comp_id,
            'metric_name' : urllib.unquote(metric_name),
            'start' : start,
            'end' : end,
            'duration' : duration,
        }
        """
        return context
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log.write('Exception in parse_request: '+repr(e)+' Line_no: '+repr(exc_tb.tb_lineno)+'\n')

def plot_job_comp_metrics(request):
    """
    Prepares the page that presents the graph image along with inputs
    to control the duration of the plot and navigation buttons to plot
    different time periods while the job was running.
    """
    try:
        context = parse_request(request)
        if 'job_id' in context:
            return render(request, 'plot/plot_job_comp_metrics.html', context)
        else:
            return render(request, 'plot/plot_comp_metrics.html', context)

    except Exception as e:
        log.write('plot_job_comp: '+repr(e)+'\n')
        raise Http404

def png_job_comp_metrics(request):
    """
    Prepares the actual image file itself as a image/png. Ultimately
    we will add additional configuration options to control the axis,
    labelling, etc...
    """
    try:
        context = parse_request(request)
        if 'job_id' in context:
            m = JobPlotPng(context['container'], context['job_id'],
                           context['schema'],
                           context['metric_name'],
                           context['start'], context['duration'])
        else:
            m = CompPlotPng(context['container'], context['comp_id'],
                            context['schema'],
                            context['metric_name'],
                            context['start'], context['duration'])
        metaData = m.plot()
        ret = json.dumps(metaData)
        return HttpResponse(ret, content_type="text/json")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log.write('Exception in _plot: '+repr(e)+' Line_no: '+repr(exc_tb.tb_lineno)+'\n')
        raise Http404

#@login_required
class HttpProxyAuth(HttpProxy):

    base_url = None

    def dispatch(self, request, url, *args, **kwargs):
        if request.user.is_authenticated():
            return super(HttpProxyAuth, self).dispatch(request, url, args, kwargs)
        return redirect('/')
