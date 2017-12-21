import sys
import os
import datetime, time
import tempfile
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import StringIO
import json
import urlparse
from sos_db.models import *
from sosgui import settings, logging
log = logging.MsgLog("Component")

class MyFormatter(matplotlib.ticker.Formatter):
    def __init__(self, fmt='%H:%M:%S'):
        self.fmt = fmt

    def __call__(self, x, pos=0):
        dt = datetime.datetime.fromtimestamp(x)
        # sys.stderr.write('%d %s\n'%(x, dt.strftime(self.fmt)))
        return dt.strftime(self.fmt)


def open_test(path):
    try:
        c = SOS.Container(str(path))
        c.close()
        return True
    except:
        return False

class SosGraph(SosQuery):
    def GET(self, request):
        rc, msg, obj = self.parse_query(request)
        if rc != 0:
            log.write(msg)
            return msg

        x_axis = []
        series = {}
        for attr_name in self.view_cols:
            series[attr_name] = []

        count = 0
        maxDt = datetime.datetime.fromtimestamp(0)
        minDt = datetime.datetime.now()
        try:
            while obj and count < self.count:
                if str(self.x_axis) == 'Time':
                    t = str(obj[self.x_axis])
                    t = time.mktime(datetime.datetime.strptime(t, "%Y/%m/%d %I:%M:%S").timetuple())
                    dt = datetime.datetime.fromtimestamp(t) + datetime.timedelta(seconds=count)
                else:
                    return None
                if dt < minDt:
                    minDt = dt
                if dt > maxDt:
                    maxDt = dt
                x_axis.append(dt)
                for attr_name in self.view_cols:
                    if attr_name == self.index_name:
                        continue
                    try:
                        value = float(obj[attr_name])
                    except:
                        value = 0.0
                    series[attr_name].append(value)
                count = count + 1
                obj = self.filt.next()
                if obj:
                    obj.release()
        except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            log.write(e)
            return repr(e)

        try:
            figure = Figure(figsize=(14,5))
            axis = figure.add_axes([0.1, 0.3, 0.8, .6])
            mfc = [ 'b', 'g', 'r', 'c', 'm', 'y', 'k' ]
            ls = []
            for c in mfc:
                ls.append(c + 'o-')
            line_no = 0
            axis.set_xmargin(.01)
            for attr_name in self.view_cols:
                if line_no >= len(mfc):
                    line_no = 0
                line,  = axis.plot(x_axis, series[attr_name],
                                   ls[line_no], markersize=6, markerfacecolor=mfc[line_no],
                                   label=attr_name, linewidth=1)
                line_no = line_no + 1
            axis.legend()
            axis.set_title(self.schema().name())
            axis.set_ylabel('Binkus: {0} recs'.format(len(x_axis)))
            minutes = mdates.MinuteLocator()
            seconds = mdates.SecondLocator()
            dateFmt = mdates.DateFormatter("%H")
            # axis.xaxis.set_major_locator(mdates.MinuteLocator())
            # axis.xaxis.set_major_formatter(mdates.DateFormatter("%M"))
            # axis.xaxis.set_minor_locator(mdates.SecondLocator())
            # axis.xaxis.set_minor_formatter(mdates.DateFormatter("%S"))


            # axis.format_xdata = mdates.DateFormatter("%H:%M:%S")
            axis.grid(True)
            figure.autofmt_xdate()

            canvas = FigureCanvasAgg(figure)
            imgdata = StringIO.StringIO()
            canvas.print_png(imgdata, dpi=150)
        except Exception, e:
            log.write(e)
        return imgdata.getvalue()

class JobPlot(SosQuery):
    def GET(self, request):
        try:
            start_dt = datetime.datetime.now()

            rc, msg, obj = self.parse_query(request)
            if rc != 0:
                log.write(msg)
                return msg

            mfc = [ 'b', 'g', 'r', 'c', 'm', 'y', 'k' ]
            ls = []
            for c in mfc:
                ls.append(c + 'o-')

            x_axis = []

            if not self.job_id:
                return(5, 'A job_id must be specified.')
            schema = request.GET['schema'].encode('utf-8')
            self.iter_ = SOS.Iterator(self.container_, schema, self.index_name)
            sample_key = self.iter_.key()
            self.iter_.key_set(sample_key, str(self.job_id << 32))
            sample_obj = self.iter_.sup(sample_key)
            if not sample_obj:
                return (1, 'The specified job was not found')

            sample = bwx.job_sample(sample_obj)
            start_secs = float(sample.JobTime.secs)
            series = {}
            metric_name = self.view_cols
            #metric_id = sample.idx('JobTime')
            metric_id = sample.idx(str(self.view_cols))
            x_axis_comp = sample.CompId
            while sample_obj is not None:
                sample = bwx.job_sample(sample_obj)
                sys.stderr.write('%d==%d time %d\n'%(sample.JobTime.id, self.job_id, sample.JobTime.secs))
                if sample.JobTime.id != self.job_id:
                    break
                comp_id = sample.CompId
                cur_secs = float(sample.JobTime.secs)
                if cur_secs - start_secs > 3600:
                    break

                if comp_id == x_axis_comp:
                    x_axis.append(cur_secs)

                if comp_id not in series:
                    y_axis = []
                    series[comp_id] = y_axis
                else:
                    y_axis = series[comp_id]

                y_axis.append(sample[metric_id])
                sos.sos_obj_put(sample_obj)
                sample_obj = self.iter_.next()

            dur = datetime.datetime.now() - start_dt
            secs0 = dur.seconds + (dur.microseconds / 1.0e6);

            figure = Figure(figsize=(10,2.5),facecolor='w')
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            axis = figure.add_axes([0.1, 0.225, 0.875, 0.65], axisbg='w')
            x_axis_len = len(x_axis)
            textstr = 'Components: %d, Job: %d'%(len(series), int(self.job_id))
            axis.text(0.050, 1.1, textstr, transform=axis.transAxes,
                      fontsize=10, verticalalignment='top', bbox=props)
            axis.tick_params(labelsize=10, direction='out')
            plot_no = 0
            for comp_id in series:
                y_axis = series[comp_id]
                y_axis_len = len(y_axis)
                axis_len = min(x_axis_len, y_axis_len)
                plot_no = plot_no + 1
                if plot_no > len(ls) - 1:
                    plot_no = 0
                line,  = axis.plot(x_axis[:axis_len], y_axis[:axis_len],
                                   ls[plot_no], markersize=6, markerfacecolor=mfc[plot_no],
                                   linewidth=1)
            axis.legend(loc='best', fancybox=True, framealpha=0.5)
            axis.set_ylabel('{0} records'.format(len(x_axis)))
            axis.xaxis.set_major_formatter(MyFormatter())
            axis.grid(True)
            figure.autofmt_xdate()
            dur = datetime.datetime.now() - start_dt
            secs = dur.seconds + (dur.microseconds / 1.0e6);
            textstr = 'Render Time: %.2f / %.2f (s)'%(secs0, secs)
            axis.text(0.050, 0.0, textstr, transform=axis.transAxes,
                      fontsize=10, verticalalignment='top', bbox=props)

            canvas = FigureCanvasAgg(figure)
            imgdata = StringIO.StringIO()
            canvas.print_png(imgdata, dpi=150)
            return imgdata.getvalue()
        except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            log.write(e)
            return repr('JobGraph Except: '+repr(e))


