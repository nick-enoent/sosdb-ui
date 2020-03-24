from future import standard_library
standard_library.install_aliases()
from builtins import next
from builtins import str
from builtins import object
import sys
import os
import datetime, time
import tempfile
import json
import urllib.parse
from sosdb import Sos
from sosgui import settings, _log

log = _log.MsgLog("sosdb_models")

sos_filt_cond = {
    "gt" : Sos.COND_GT,
    "ge" : Sos.COND_GE,
    "ne" : Sos.COND_NE,
    "eq" : Sos.COND_EQ,
    "le" : Sos.COND_LE,
    "lt" : Sos.COND_LT
}

def open_test(path):
    try:
        c = Sos.Container(str(path))
        c.close()
        return True
    except Exception as e:
        log.write('open_test err: '+repr(e))
        return False

def SosDir():
    """
    Given the SOS_ROOT, search the directory structure to find all
    of the containers available for use. Note that even if the
    directory is there, this will skip the container if the
    requesting user does not have access rights.

    The OVIS store is organized like this:
    {sos_root}/{container_name}/{timestamped version}
    """
    rows = []
    try:
        dirs = os.listdir(settings.SOS_ROOT)
        # Check each subdirectory for files that constitute a container
        for ovc in dirs:
            try:
                ovc_path = settings.SOS_ROOT + '/' + ovc
                try:
                    files = os.listdir(ovc_path)
                    if '.__schemas.OBJ' in files:
                        if open_test(ovc_path):
                            rows.append( { "name" : ovc } )
                except Exception as e:
                    log.write(e)
            except Exception as e:
                log.write(e)
        return { "directory" : rows }
    except Exception as e:
        # return render.table_json('directory', [ 'name' ], [], 0)
        return SosErrorReply(e)


class timezone(object):
    def __init__(self):
        self.dst = 0

    def parse_tz(self, ct, tz, dst=0):
        self.dst = dst
        self.tz = tz + dst
        self.tz = self.tz * 3600
        self.ct = ct - self.tz
        return self.ct

class SosRequest(object):
    """
    This base class handles the 'container', 'encoding' and 'schema',
    'start', and 'count' keywords. For DataTables compatability, 'iDisplayStart'
    is a synonym of 'start' and 'iDisplayCount' is a synonym of 'count'.
    """
    JSON = 0
    TABLE = 1
    def __init__(self):
        self.encoding_ = self.JSON
        self.container_ = None
        self.schema_ = None
        self.start = 0
        self.count = 10

    def release(self):
        if self.container_:
            self.container_.close()
        self.container_ = None

    def __del__(self):
        self.release()

    def container(self):
        return self.container_

    def encoding(self):
        return self.encoding_

    def schema(self):
        return self.schema_

    def parse_request(self, input_):
        #
        # Open the container or get it from our directory
        #
        self.input_ = input_
        if 'container' in input_:
            container = input_['container'].encode('utf-8')
            try:
                self.container_ = Sos.Container(str(settings.SOS_ROOT + '/' + container))
            except Exception as e:
                log.write(e)
                return { "Sos Error" : "Container "+repr(container)+" could not be opened" }
        else:
            return { "Sos Error" : "Container clause is mandatory" }

        #
        # Encoding
        #
        #if 'encoding' in input:
        #    if input.encoding.lower() == 'table':
        #        self.encoding_ = self.TABLE
        #else:
        #    self.encoding_ = self.JSON

        #
        # Schema
        #
        if 'schema' in input_:
             try:
                schema = input_['schema'].encode('utf-8')
                #schema = schema.encode('utf-8')
                if self.container():
                    self.schema_ = self.container().schema_by_name(schema)
             except Exception as e:
                 log.write("Schema Error "+repr(e))
                 return { "Error": "Schema does not exist" }
                 

        #
        # iDisplayStart (dataTable), start
        #
        if 'start' in input_:
            self.start = input_['start'].encode('utf-8')
            self.start = int(self.start)
        # overrides start if specified
        if 'iDisplayStart' in input_:
            self.start = input_['iDisplayStart'].encode('utf-8')
            self.start = int(self.start)

        #
        # iDisplayLength (dataTables), count
        #
        if 'count' in input_:
            self.count = input_['count'].encode('utf-8')
            self.count = int(self.count)
        # overrides count if specified
        if 'iDisplayLength' in input_:
            self.count = input_['iDisplayLength'].encode('utf-8')
            self.count = int(self.count)
        # Job Id
        if 'job_id' in input_:
            self.job_id = input_['job_id'].encode('utf-8')
            self.job_id = int(self.job_id)


class SosInfo(object):
    def GET(self):
        rows = {"Container Name":request.session['containerName'],
                 "Index Name":request.session['indexName'],
                 "Record no":request.session['recordNo'],
                 "Position":request.session['pos'] }
        return [rows, len(rows)]

def SosErrorReply(err):
    return { "error" : "{0}".format(str(err))}

class SosContainer(SosRequest):
    """
    Build up a container object that includes the container's schema,
    indexes and partitions
    """
    def GET(self, request):
        try:
            query = request.GET
            self.parse_request(query)
            schema_rows = []
            for schema in self.container().schema_iter():
                row = { "Name" : schema.name(), "AttrCount" : schema.attr_count() }
                schema_rows.append(row)
            idx_rows = []
            for index in self.container().index_iter():
                stats = index.stats()
                row = { "Name" : index.name(),
                        "Entries" : stats['cardinality'],
                        "Duplicates" : stats['duplicates'],
                        "Size" : stats['size']}
                idx_rows.append(row)
            part_rows = []
            for part in self.container().part_iter():
                stat = part.stat()
                row = { "Name" : str(part.name()),
                        "State" : str(part.state()),
                        "Id" : int(part.part_id()),
                        "Size" : int(stat.size),
                        "Accessed" : str(stat.accessed),
                        #"Created" : stat['created'],
                        "Modified" : str(stat.modified)
                    }
                part_rows.append(row)
            #self.release()
            return { "container" :
                     { "schema" : schema_rows,
                       "indexes" : idx_rows,
                       "partitions" : part_rows
                     }
                 }
        except Exception as e:
            #self.release()
            exc_a, exc_b, exc_tb = sys.exc_info()
            log.write('SosContainer Err: '+repr(e)+' '+repr(exc_tb.tb_lineno))
            return SosErrorReply(e)

class SosSchema(SosRequest):
    """
    Return all of the attributes and attribute meta-data for the
    specified schema.
    """
    def GET(self, request):
        try:
            query = request.GET
            self.parse_request(query)
        except Exception as e:
	    log.write(e)
            return SosErrorReply(e)
        if not self.schema():
            return SosErrorReply("A 'schema' clause must be specified.\n")
        rows = []
        for attr in self.schema():
            row = {'name': attr.name(), 'id':attr.attr_id(),
                   'sos_type':attr.type_name(), 'indexed': repr(attr.is_indexed())}
            if str(attr.is_indexed()) == 'True':
                stat = attr.index().stats()
                row['card'] = int(stat['cardinality'])
                row['dups'] = int(stat['duplicates'])
                #row['min_key'] = int(attr.min())
                #row['max_key'] = int(attr.max())
            else:
                row['card'] = ""
                row['dups'] = ""
                row['min_key'] = ""
                row['max_key'] = ""
            rows.append(row)
        return { "schema" : { "name" : self.schema().name(), "attrs": rows } }

class SosQuery(SosRequest):
    """
    This is the base class for the SosTable class. It handles all of
    the query preparation, such as creating the filter, advancing to
    the first matching element, etc.
    """
    def __init__(self):
        super( SosQuery, self ).__init__()
        self.filt = None

    def reset(self):
        try:
            self.request.session['indexName'] = self.index_name
            self.request.session['containerName'] = self.container().name()
            self.request.session['pos']= self.start
            self.request.session['recordNo'] = self.count
        except Exception as e:
            pass

    def parse_query(self, request):
        self.parms = request.GET
        self.request = request
        try:
            self.parse_request(self.parms)
        except Exception as e:
            return (1, "Exception in parse_request: {0}".format(e), None)

        if not self.schema():
            return (1, "A 'schema' clause must be specified.\n", None)

        if not 'index' in self.parms:
            return (1, "An 'index' clause must be specified.\n", None)

        #
        # Open an iterator on the container
        #
        self.index_attr = None
        self.index_name = self.parms['index'].encode('utf-8')
        if 'indexName' not in self.request.session:
            self.reset()
        if 'containerName' not in self.request.session:
            self.reset()
        self.schema_name = self.schema().name()
        self.index_attr = self.schema().attr_by_name(self.index_name)
        self.iter_ = self.index_attr.index().stats()
        self.filt = Sos.Filter(self.index_attr)
        if 'unique' in self.parms:
            self.unique = True
            self.filt.unique()
        else:
            self.unique = False
        self.card = self.iter_['cardinality']
        if self.unique:
            self.card = self.card - self.iter_['duplicates']

        #
        # Parse the select clause. The view_cols contains the index as it's first element.
        #
        self.view_cols = []
        if 'select' in self.parms:
            self.select = self.parms['select'].encode('utf-8')
            for attr_name in self.select.split(','):
                if attr_name != self.index_name:
                    self.view_cols.append(attr_name)
        else:
            for attr in self.schema():
                if attr.name() != self.index_name:
                    self.view_cols.append(attr.name())
        #
        # Parse the where clause
        #
        #
        # A filter is an array of conditions
        #
        if 'where' in self.parms:
            where = self.parms['where']
            conds = where.split(',')
            for cond in conds:
                tokens = cond.split(':')
                if len(tokens) < 3:
                    return (1, "Invalid where clause '{0}', "
                            "valid syntax is attr:cmp_str:value".format(cond), None)
                attr_name = tokens[0]
                attr = self.schema().attr_by_name(attr_name)
                if not attr:
                    return (1, "The attribute {0} was not found "
                            "in the schema {1}".format(attr_name, self.schema().name()), None)
                sos_cmp = sos_filt_cond[tokens[1]]
                value_str = None
                tokens[2] = tokens[2].split('"')[1]
                for s in tokens[2:]:
                    if value_str:
                        value_str = value_str + ':' + s
                    else:
                        value_str = s
                self.filt.add_condition(attr, sos_cmp, int(tokens[2]))

        obj = None
        if self.start == 0:
            self.reset()
            obj = self.filt.begin()
            skip = self.start
        elif self.start + self.count >= self.card:
            self.reset()
            obj = self.filt.end()
            skip = self.card % self.count
            while obj and skip > 0:
                obj = self.filt.prev()
                skip = skip - 1
        else:
            self.filt.set_pos(str(self.request.session['pos']))
            skip = self.start - self.request.session['recordNo']

            obj = self.filt.obj()
            while obj and skip != 0:
                if skip > 0:
                    obj = next(self.filt)
                    skip = skip - 1
                else:
                    obj = self.filt.prev()
                    skip = skip + 1
        pos = self.filt.get_pos()
        self.request.session['pos'] = pos
        self.request.session['recordNo'] = self.start
        return (0, None, obj)

class SosTable(SosQuery):
    def GET(self, request):
        try:
            rc, msg, obj = self.parse_query(request)
            if rc != 0:
                return SosErrorReply(msg)

            tbl_hdr = [ 'RecNo', self.index_name ]
            for attr_name in self.view_cols:
                tbl_hdr.append(attr_name)

            rows = []
            count = 0
            while obj is not None and count < self.count:
                row = { 'DT_RowId':self.request.session['recordNo'] + count,
                        str(self.index_name):str(obj[self.index_name])}
                for attr_name in self.view_cols:
                    if attr_name == self.index_name:
                        continue
                    try:
                        value = str(obj[attr_name])
                    except:
                        value = "bad_name"
                    row[attr_name] = value
                rows.append(row)
                count = count + 1
                obj = next(self.filt)
            if obj:
                del obj
            if self.filt:
                del self.filt
            self.release()
            return {self.schema_name:rows,
                    'iTotalRecords':self.card,
                    'iTotalDisplayRecords': self.card}
        except Exception as e:
            a, b, exc_tb = sys.exc_info()
            log.write('SosTable Err: '+str(e)+' '+str(exc_tb.tb_lineno))
            self.release()
            return SosErrorReply(e)

    def INSERT(self, request):
        try:
            rc, msg, obj = self.parse_request(request)
            if rc != 0:
                return { "status" : str(msg) }
            for attr in self.schema():
                if attr.name() in self.parms:
                    obj = self.schema().alloc()
                    obj[attr.name()] = self.parms[attr.name()].encode('utf-8')
            return { "status": 0 }
        except Exception as e:
            if self.filt:
                del self.filt
            log.write(e)
            self.release()
            return SosErrorReply(e)

