#!/usr/bin/env python

import os
import sys
import time
import shutil

from sosdb import Sos

HOST_ID_BASE = 10000
NUM_HOSTS = 256

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
TS_INC = 60 # 1 minute metric data interval

STORE_PATH = os.getcwd() + "/ldms.sos"

# Remove old store
shutil.rmtree(STORE_PATH, ignore_errors = True)

# Create the store
cont = Sos.Container()
cont.create(STORE_PATH)
cont.open(STORE_PATH)
cont.part_create("ROOT")
part = cont.part_by_name("ROOT")
part.state_set("PRIMARY")
del part

# Schema

def simple_schema_create(name, mlist):
    # mlist - [ (name, type), ... ]
    global cont
    tmp = [
        { "name": "timestamp", "type": "timestamp", "index": {} },
        { "name": "component_id", "type": "uint64", "index": {} },
        { "name": "job_id", "type": "uint64", "index": {} },
    ]
    tmp.extend([ {"name": n, "type": t} for n,t in mlist ])
    tmp.extend([
        { "name": "comp_time", "type": "join",
          "join_attrs": ["component_id", "timestamp"], "index": {} },
        { "name": "job_comp_time", "type": "join",
          "join_attrs": ["job_id", "component_id", "timestamp"], "index": {} },
        { "name": "job_time_comp", "type": "join",
          "join_attrs": ["job_id", "timestamp", "component_id"], "index": {} },
    ])
    sc = Sos.Schema()
    sc.from_template(name, tmp)
    sc.add(cont)
    return sc

schema0 = simple_schema_create("schema0", [ ("metric0", "uint64"),
                                            ("metric1", "uint64") ] )

schema1 = simple_schema_create("schema1", [ ("metric0", "uint64"),
                                            ("metric1", "uint64"),
                                            ("metric2", "uint64") ] )

# Populate data
count = 0
for sec in range(TS_BEGIN, TS_BEGIN + TS_DURATION, TS_INC):
    ts = (sec, 0)
    for comp_id in range(HOST_ID_BASE, HOST_ID_BASE + NUM_HOSTS):
        count += 1
        data = [ ts, comp_id, 0, sec, comp_id, count ]
        o0 = schema0.alloc()
        o0[:] = data[:-1]
        o0.index_add()
        o1 = schema1.alloc()
        o1[:] = data
        o1.index_add()
        del o0
        del o1
        if count % 10000 == 0:
            print "count:", count
            percent = (0.0 + sec - TS_BEGIN)/TS_DURATION *100
            print "percent: %.02f%%" % percent

print "DONE"

# cleanup
del schema0
del schema1
cont.close()
