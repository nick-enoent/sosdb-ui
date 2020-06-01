from django.conf import settings
from django.shortcuts import render_to_response
from django.http import Http404
import settings, logging

log = logging.MsgLog("sosgui_utils")

def ViewContext(request = None, template_name = None, **kwargs):
    """Create a view context, `kwargs` extend the default parameters"""
    ret = {
        'request' : request,
        'settings': settings,
        'ldms_nav': 'ldms_control' in settings.INSTALLED_APPS,
        'baler_nav': 'balerd' in settings.INSTALLED_APPS,
        'template_name': template_name,
    }
    ret.update(kwargs)
    return ret

def template_render(template_path, request = None, template_name = None, **kwargs):
    """Render a template, parametersr in `kwargs` will be in the view context"""
    try:
	return render_to_response(template_path,
                                  ViewContext(request, template_name, **kwargs)) 
    except Exception, e:
        if settings.DEBUG:
            raise
	log.write(repr(e)+'\n')
	raise Http404
