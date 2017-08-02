#!/usr/bin/env python
import sys
import os
import math
import argparse
from datetime import datetime
import tempfile
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.ticker import Formatter
import StringIO
import urllib, base64
from sosgui import settings, logging

log = logging.MsgLog("PlotModel")

class MyXFormatter(Formatter):
    def __init__(self, fmt='%H:%M:%S'):
        self.fmt = fmt

    def __call__(self, x, pos=0):
        #Display Local Timezone from GMT
        x = int(x) + settings.TIMEZONE
        dt = datetime.fromtimestamp(x)
        return dt.strftime(self.fmt)

class MyYFormatter(Formatter):
    def __init__(self, fmt='%.2f%s'):
        self.fmt = fmt

    def __call__(self, x, pos=0):
        if (x < 1.0e3):
            return self.fmt%(x, ' ')
        if (x < 1.0e6):
            return self.fmt%(x / 1.0e3, 'K')
        if (x < 1.0e9):
            return self.fmt%(x / 1.0e6, 'M')
        if (x < 1.0e12):
            return self.fmt%(x / 1.0e9, 'G')
        return self.fmt%(x / 1.0e12, 'T')

class Plot(object):
    def __init__(self, output='gui'):
        self.output = output

    def render(self, figure, plt, startTs=0, lastTs=0):
        if self.output == 'gui':
            plt.show()
            return None
        try:
            os.remove(settings.GRAPH_IMG)
        except:
            pass
        canvas = FigureCanvasAgg(figure)
        #imgdata = StringIO.StringIO()
        canvas.print_png(settings.GRAPH_IMG, dpi=150)
        #data = imgdata.getvalue()
        #figure.savefig(settings.GRAPH_IMG) 
        metaPlot = {"startTs":startTs, "lastTs":lastTs}
        return metaPlot

    def plot_error(self, msg):
        figure = Figure(figsize=(10,2.5),facecolor='w')
        props = dict(boxstyle='round', facecolor='red', alpha=1.0)
        axis = figure.add_axes([0.1, 0.225, 0.875, 0.65], axisbg='w')
        axis.legend(loc='best', fancybox=True, framealpha=0.5)
        axis.text(.05, .5, str(msg), transform=axis.transAxes,
                  fontsize=18, verticalalignment='top',
                  bbox=props)
        return self.render(figure, plt)

    def plot(self):
        return self.plot_error("Not Implemented")

class CompPlot(Plot):
    def __init__(self, container, comp_id, schema, metric,
                 start=0, duration=3600, output='gui'):
        super(CompPlot, self).__init__(output)
        self.containerName = settings.SOS_ROOT + '/' + container
        self.schemaName = schema
        self.metricName = metric.split(",")
        self.compId = comp_id.split(",")
        self.compId = map(int, self.compId)
        self.duration = duration
        self.startSecs = int(start)
        self.lastSec = start + duration
        self.iter = None
        self.container = None

    def plot(self):
        try:
            return self.__plot()
        except Exception as e:
            if self.iter:
                self.iter.release()
            if self.container:
                self.container.close()
            return self.plot_error(e)

    def __plot(self):
        start_dt = datetime.now()
        mfc = [ 'b', 'g', 'r', 'c', 'm', 'y', 'k' ]
        ls = []
        for c in mfc:
            ls.append(c + 'o-')

        self.container = SOS.Container(self.containerName, mode=SOS.Container.RO)
        figure = Figure(figsize=(10,2.5),facecolor='w')
        i = 0
        dur = datetime.now() - start_dt
        secs0 = dur.seconds + (dur.microseconds / 1.0e6);
        for c in self.compId:
            self.iter = SOS.Iterator(self.container, self.schemaName, "comp_time")
            sample_key = self.iter.key()
            self.iter.key_set(sample_key, str((c << 32) | self.startSecs))
            for n in self.metricName:
                x_axis = []
                y_axis = []

                sample_obj = self.iter.sup(sample_key)
                sample = SOS.Object(sample_obj)

                if self.startSecs == 0:
                    self.startSecs = int(sample.timestamp)

                if not sample_obj:
                    self.iter.release()
                    self.container.close()
                    return self.plot_error('There are no samples for the specified component')
                while sample_obj is not None:
                    sample = SOS.Object(sample_obj)
                    if int(sample.component_id) != c:
                        break
                    ts = int(sample.timestamp)
                    if ts - self.startSecs > abs(self.duration):
                        break
                    x_axis.append(ts)
                    y_axis.append(float(sample[n]))
                    self.lastSec = ts + abs(self.duration)
                    sample_obj = self.iter.next()


                #if self.output == 'gui':
                #    figure = plt.figure(figsize=(10,2.5),facecolor='w')
                #else:
                #    figure = Figure(figsize=(10,2.5),facecolor='w')
                axis = figure.add_axes([0.1, 0.225, 0.875, 0.65], axisbg='w')
                x_axis_len = len(x_axis)
                y_axis_len = len(y_axis)
                axis_len = min(x_axis_len, y_axis_len)
                axis.tick_params(labelsize=10, direction='out')
                if len(self.compId) > 1:
                    line, = axis.plot(x_axis[:axis_len], y_axis[:axis_len],
                                      ls[0], markersize=6, markerfacecolor=mfc[i],
                                      linewidth=1, label=c)
                else:
                    line, = axis.plot(x_axis[:axis_len], y_axis[:axis_len],
                                      ls[0], markersize=6, markerfacecolor=mfc[i],
                                      linewidth=1, label=n)
                axis.set_title(n, fontsize=10)
                axis.set_ylabel('{0} records'.format(x_axis_len))
                plot_durTs = self.startSecs + abs(self.duration)
                axis.set_xlim([self.startSecs, plot_durTs])
                axis.xaxis.set_major_formatter(MyXFormatter())
                axis.yaxis.set_major_formatter(MyYFormatter())
                axis.grid(True)
                figure.autofmt_xdate()
                #dur = datetime.now() - start_dt
                #secs = dur.seconds + (dur.microseconds / 1.0e6);
                #textstr = 'Render Time: %.2f / %.2f (s)'%(secs0, secs)
                #props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                #axis.text(0.050, 1.1, textstr, transform=axis.transAxes,
                #          fontsize=10, verticalalignment='top', bbox=props)
                #if x_axis_len == 0:
                #    axis.text(.05, .5, "No sample data found for this component", transform=axis.transAxes,
                #              fontsize=18, verticalalignment='top',
                #              bbox=props)
                i = i + 1
                axis.legend()
        self.iter.release()
        dur = datetime.now() - start_dt
        secs = dur.seconds + (dur.microseconds / 1.0e6);
        textstr = 'Render Time: %.2f / %.2f (s)'%(secs0, secs)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        axis.text(0.050, 1.1, textstr, transform=axis.transAxes,
                  fontsize=10, verticalalignment='top', bbox=props)
        if x_axis_len == 0:
            axis.text(.05, .5, "No sample data found for this component", transform=axis.transAxes,
                      fontsize=18, verticalalignment='top',
                      bbox=props)

        self.container.close()
        return self.render(figure, plt, self.startSecs, self.lastSec)

class JobPlot(Plot):
    def __init__(self, container, job_id, schema, metric, start=0, duration=3600, output='gui'):
        super(JobPlot, self).__init__(output)
        self.containerName = settings.SOS_ROOT + '/' + container
        self.schemaName = schema
        self.metricName = metric
        self.jobId = job_id
        self.startSecs = start
        self.duration = duration
        self.iter = None
        self.container = None

    def plot(self):
        try:
            return self.__plot()
        except Exception as e:
            if self.iter:
                self.iter.release()
            if self.container:
                self.container.close()
            #log.write(e)
            return self.plot_error(repr(e))

    def __plot(self):
        start_dt = datetime.now()
        mfc = [ 'b', 'g', 'r', 'c', 'm', 'y', 'k' ]
        ls = []
        for c in mfc:
            ls.append(c + 'o-')
        self.startSecs = self.startSecs
        x_axis = []

        self.container = SOS.Container(self.containerName,
                                       mode=SOS.Container.RO)
        self.iter = SOS.Iterator(self.container, self.schemaName, "job_time")
        sample_key = self.iter.key()

        self.iter.key_set(sample_key, str((self.jobId << 32) | self.startSecs))
        sample_obj = self.iter.sup(sample_key)
        if not sample_obj:
            self.iter.release()
            self.container.close()
            return self.plot_error('There are no samples for the specified job')

        sample = bwx.job_sample(sample_obj)
        if self.startSecs == 0:
            self.startSecs = float(sample.job_time.secs)
        series = {}
        metric_id = sample.idx(self.metricName)
        if metric_id < 0:
            self.iter.release()
            self.container.close()
            return self.plot_error("'{0}' is an invalid metric name."
                                   .format(self.metricName))
        x_axis_comp = sample.CompId
        while sample_obj is not None:
            sample = bwx.job_sample(sample_obj)
            if sample.job_time.job_id != self.jobId:
                break

            comp_id = sample.CompId
            cur_secs = float(sample.job_time.secs)
            if cur_secs - self.startSecs > self.duration:
                break

            if comp_id == x_axis_comp:
                x_axis.append(cur_secs)

            if comp_id not in series:
                y_axis = []
                series[comp_id] = y_axis
            else:
                y_axis = series[comp_id]

            y_axis.append(sample[metric_id])
            #sos.sos_obj_put(sample_obj)
            sample_obj = self.iter.next()

        dur = datetime.now() - start_dt
        secs0 = dur.seconds + (dur.microseconds / 1.0e6);

        if self.output == 'gui':
            figure = plt.figure(figsize=(10,2.5),facecolor='w')
        else:
            figure = Figure(figsize=(10,2.5),facecolor='w')
        axis = figure.add_axes([0.1, 0.225, 0.875, 0.65], axisbg='w')
        x_axis_len = len(x_axis)
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
        axis.set_title(self.metricName + '[' + str(len(series)) + ']', fontsize=10)
        axis.set_ylabel('{0} records'.format(x_axis_len))
        axis.xaxis.set_major_formatter(MyXFormatter())
        axis.yaxis.set_major_formatter(MyYFormatter())
        axis.grid(True)
        figure.autofmt_xdate()
        dur = datetime.now() - start_dt
        secs = dur.seconds + (dur.microseconds / 1.0e6);
        textstr = 'Render Time: %.2f / %.2f (s)'%(secs0, secs)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        axis.text(0.050, 1.1, textstr, transform=axis.transAxes,
                  fontsize=10, verticalalignment='top', bbox=props)
        if x_axis_len == 0:
            axis.text(.05, .5, "No sample data found for this Job", transform=axis.transAxes,
                      fontsize=18, verticalalignment='top',
                      bbox=props)
        self.iter.release()
        self.container.close()

        return self.render(figure, plt)

class JobPlotPng(JobPlot):
    def __init__(self, container, job_id, schema, metric, start=0, duration=3600):
        super(JobPlotPng, self).__init__(container, job_id,
                                         schema, metric,
                                         start, duration, output='png')

class CompPlotPng(CompPlot):
    def __init__(self, container, comp_id, schema, metric, start=0, duration=3600):
        super(CompPlotPng, self).__init__(container, comp_id,
                                          schema, metric,
                                          start, duration, output='png')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot a Job's metric data.")
    parser.add_argument("--container", default="BWX_Job_Data",
                        help="Specify the container path")
    parser.add_argument("--plot", help="Specify job or for comp leave blank")
    parser.add_argument("--comp-id", type=int,
                        help="Specify Comp Id")
    parser.add_argument("--job-id", type=int,
                        help="Specify the Job Id")
    parser.add_argument("--metric-name", default="current_freemem",
                        help="Specify The metric name to be plotted")
    parser.add_argument("--start-time",
                        help="Specify the start time, format is YYYY/MM/DD HH:MM:SS")
    parser.add_argument("--duration",
                        type=int, default=int(3600),
                        help="Specify the duration, format is seconds ")
    args = parser.parse_args()
    if args.start_time:
        dt = datetime.strptime(args.start_time, "%Y/%m/%d %H:%M:%S")
        start_secs = int(dt.strftime("%s"))
    else:
        start_secs = 0
    if args.plot == "job":
        jobPlot = JobPlot(args.container, args.job_id, args.metric_name,
                      start_secs, args.duration, 'gui')
        jobPlot.plot()
    else:
        compPlot = CompPlot(args.container, args.job_id, args.metric_name,
                            start_secs, args.duration, 'gui')
        compPlot.plot()
