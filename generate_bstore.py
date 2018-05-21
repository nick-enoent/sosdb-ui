#!/usr/bin/env python

import os
import re
import sys
import time
import shutil
import socket
import logging
import unittest
import subprocess

TOP_DIR = sys.path[0]
if not TOP_DIR:
    TOP_DIR = os.getcwd()

STORE_PATH = TOP_DIR + "/store"
BALERD_CFG_PATH = TOP_DIR + "/balerd.cfg"
BIN_TCP_PORT = "10514"
BALERD_HOST_LIST = TOP_DIR + "/host.list"
BALERD_WORD_LIST = TOP_DIR + "/eng-dictionary"
BALERD_CFG = """
tokens type=HOSTNAME path=%(host_list)s
tokens type=WORD path=%(word_list)s
plugin name=bout_store_msg
plugin name=bout_store_hist tkn=1 ptn=1 ptn_tkn=1
plugin name=bin_tcp port=%(bin_tcp_port)s parser=syslog_parser
""" % {
    "host_list": BALERD_HOST_LIST,
    "word_list": BALERD_WORD_LIST,
    "bin_tcp_port": BIN_TCP_PORT,
}
BALERD_LOG_PATH = TOP_DIR + "/balerd.log"

# This generates the following list of hosts:
#   'node00000'  with ID 10000 (BASE 10000 + host number 00000)
#   'node00001'  with ID 10001
#   ...
#   'node00255'  with ID 10255 (BASE 10000 + host number 00255)
HOST_ID_BASE = 10000
NUM_HOSTS = 256

PATTERNS = [
    "Pattern Zero:",
    "Pattern One:",
    "Pattern Three:",
    "Pattern Four:",
    "Pattern Five:",
    "Pattern Six:",
    "Pattern Seven:",
]

time.tzset()
TZ = time.altzone if time.daylight else time.timezone
TZ_TEXT = "%+03d:%02d" % (-TZ / 3600, -TZ % 3600)
def midnight_yesterday():
    DAY_SEC = 24 * 3600
    # midnight yesterday in GMT
    t = int(time.time() - DAY_SEC) / DAY_SEC * DAY_SEC
    # make it midnight localtime
    t += time.altzone if time.daylight else time.timezone
    return t

TS_BEGIN = midnight_yesterday()
TS_DURATION = 24 * 3600
TS_INC = 600

ALL_TS = [ time.strftime("%FT%T.000000"+TZ_TEXT, time.localtime(ts))
                    for ts in range(TS_BEGIN, TS_BEGIN + TS_DURATION, TS_INC)]

logging.basicConfig(level = logging.INFO)

log = logging.getLogger(__name__)

class Debug(object): pass

DEBUG = Debug()

def purge_store():
    shutil.rmtree(STORE_PATH, ignore_errors = True)

def proc_stat(pid):
    """Get /proc/`pid`/stat entries"""
    with open('/proc/%d/stat' % pid, 'r') as f:
        return f.readline().strip().split(' ')

def proc_stat_cpu(pid):
    """Get `pid` CPU time (utime + stime)"""
    s = proc_stat(pid)
    return int(s[13]) + int(s[14]) # utime + stime

def proc_wait_cpu(pid, dt = 1.0):
    """Wait until `pid` is not so busy cranking numbers"""
    a = 0
    b = proc_stat_cpu(pid)
    while b - a:
        time.sleep(dt)
        a = b
        b = proc_stat_cpu(pid)

def make_store():
    log.info("------- making the store -------")
    cfg = open(BALERD_CFG_PATH, "w")
    print >>cfg, BALERD_CFG
    cfg.close()

    # clear blog
    blog = open(BALERD_LOG_PATH, "w")
    blog.close()

    hfile = open(BALERD_HOST_LIST, "w")
    with open(BALERD_HOST_LIST, "w") as f:
        for i in range(0, NUM_HOSTS):
            _id = HOST_ID_BASE + i
            name = "node%05d" % i
            print >>f, name, _id

    hosts = ["node%05d" % i for i in range(0, NUM_HOSTS)]

    bcmd = "balerd -F -S bstore_sos -s %(store_path)s -C %(cfg_path)s \
            -l %(log_path)s -v INFO" % {
                "store_path": STORE_PATH,
                "cfg_path": BALERD_CFG_PATH,
                "log_path": BALERD_LOG_PATH,
            }
    log.info("balerd cmd: " + bcmd)
    balerd = subprocess.Popen("exec " + bcmd, shell=True)
    try:
        pos = 0
        is_ready = False
        ready_re = re.compile(".* Baler is ready..*")
        # look for "Baler is ready" in the log
        while True:
            x = balerd.poll()
            if balerd.returncode != None:
                # balerd terminated
                break
            blog = open(BALERD_LOG_PATH, "r")
            blog.seek(pos, 0)
            ln = blog.readline()
            if not ln:
                pos = blog.tell()
                blog.close()
                time.sleep(0.1)
                continue
            m = ready_re.match(ln)
            if m:
                is_ready = True
                blog.close()
                break
            pos = blog.tell()
            blog.close()

        if not is_ready:
            raise Exception("Something bad happened to balerd")

        # now, feed some data to the daemon
        log.info("Feeding data to balerd")
        sock = socket.create_connection(("localhost", BIN_TCP_PORT))
        ts_idx = 0
        h_idx = 0
        ptn_idx = 0
        for ts in ALL_TS:
            h_idx = 0
            for h in hosts:
                ptn_idx = 0
                for ptn in PATTERNS:
                    if 0 == ((ts_idx + h_idx + ptn_idx) % len(PATTERNS)):
                        for i in range(0, h_idx + 1):
                            msg = "<1>1 %s %s %s\n" % (ts, h, ptn)
                            sock.send(msg)
                    ptn_idx += 1
                h_idx += 1
            ts_idx += 1
            log.info("Progress: %.02f %%" % (100.0*ts_idx/len(ALL_TS)))
        sock.close()
        proc_wait_cpu(balerd.pid)
    finally:
        log.info("Terminating balerd")
        while balerd.poll() is None:
            balerd.terminate()
            time.sleep(1)

if __name__ == "__main__":
    purge_store()
    make_store()
