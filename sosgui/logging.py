import time
import sys
import traceback
from datetime import datetime
from sosgui import settings

class MsgLog(object):
    def __init__(self, prefix):
        self.prefix = prefix
        self.fp = open(settings.LOG_FILE, 'a')
        self.dt_fmt = settings.LOG_DATE_FMT

    def write(self, obj):
        now = datetime.now()
        pfx = now.strftime(self.dt_fmt)
        pfx = pfx + ":" + self.prefix + ":"
        if isinstance(obj, Exception):
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.fp.write(pfx + "\n")
            traceback.print_exception(exc_type, exc_obj, exc_tb, 10, self.fp)
        else:
            self.fp.write(pfx + str(obj) + "\n")
        self.fp.flush()

    def __del__(self):
        if self.fp:
            self.fp.close()
        self.fp = None
