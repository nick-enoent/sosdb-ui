"""
WSGI config for sosgui project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
import os
import sys
import traceback
import signal
from sosgui import settings, _log
from django.core.wsgi import get_wsgi_application

log = _log.MsgLog('WSGI Err: ')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sosgui.settings")
try:
    os.environ['ODS_LOG_FILE'] = str(settings.ODS_LOG_FILE)
except:
    pass
try:
    os.environ['ODS_LOG_MASK'] = str(settings.ODS_LOG_MASK)
except:
    pass
try:
    os.environ['ODS_GC_TIMEOUT'] = str(settings.ODS_GC_TIMEOUT)
except:
    pass

application = get_wsgi_application()
