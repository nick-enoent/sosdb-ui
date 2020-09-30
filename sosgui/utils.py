from django.conf import settings
from django.shortcuts import render
from django.http import Http404
from . import settings, _log

log = _log.MsgLog("sosgui_utils")

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
        return render(request, template_path, ViewContext(request, template_name, **kwargs)) 
    except Exception as e:
        if settings.DEBUG:
            raise
        log.write(repr(e)+'\n')
        raise Http404
