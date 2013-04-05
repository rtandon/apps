#!/usr/local/bin/python2.7

"""
Utils module containing helper methods used across application
Tags: Utils
Api: MIP DataPipeline
"""
import re
from metadata import hive_formatter

__author__ = 'sameer.thakur@clickable.com (Sameer Thakur)'
from pytz import timezone
import datetime
import os
import errno
import csv
import tarfile
import shutil
import zipfile
import bz2
import network_api.constants as constants
import settings
import logging
from datetime import datetime
import datetime as dt
import calendar
import time
from urllib2 import URLError
import mimetools
import mimetypes
import itertools
import urllib
import urllib2
import httplib
import json
import pytz
from lxml import etree
import collections
import Queue
#Module Logger
logger = logging.getLogger(__name__)
doLogClientRequest=True

def parse_datetime_string(date_str):
    """
    input format expected - YYYYMMDDHHmmssSSS
    eg: 8/9/2012 23:24:45.346 will be 20120809232445346
    """
    #return datetime.datetime.strptime(date_str, '%Y%m%d%H%M%S%f')
    return datetime.strptime(date_str, '%Y%m%d%H%M%S%f')


def format_datetime(dt):
    """
    output format expected - YYYYMMDDHHmmssSSS
    eg: 8/9/2012 23:24:45.346 will be 20120809232445346
    mod.hbase_formatter.format_datetime({source}.entity.StartDate)
    """
    return time.strftime('%Y%m%d%H%M%S%f')[:-3]

def get_unix_time(date_str, timezone):
    date_val=None
    date_val=parse_datetime_string(date_str)
    date_val = date_val.replace(tzinfo=timezone)
    return calendar.timegm(date_val.utctimetuple())

# this class allows you to upload a file to a URL
# using pure urllib
class MultiPartForm(object):
    """Accumulate the data to be used when posting a form.
       source: http://www.doughellmann.com/PyMOTW/urllib2/#uploading-files
    """

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        try:
            body = fileHandle.read()
            if mimetype is None:
                mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            self.files.append((fieldname, filename, mimetype, body))
        finally:
            try:
                if fileHandle:
                    fileHandle.close()
            except:
                pass
        return

    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend(
            [part_boundary,
             'Content-Disposition: form-data; name="%s"' % name,
             '',
             value,
             ]
                for name, value in self.form_fields
        )

        # Add the files to upload
        parts.extend(
            [part_boundary,
             'Content-Disposition: file; name="%s"; filename="%s"' % \
             (field_name, filename),
             'Content-Type: %s' % content_type,
             '',
             body,
             ]
                for field_name, filename, content_type, body in self.files
        )

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        flattened = map(str, flattened)
        return '\r\n'.join(flattened)



def cleanList(list):
    """Remove unwanted values from list
        Args:
          list: list of string values
    """
    for idx, value in enumerate(list[:]):
        new_value=value.strip()
        if new_value == '--':
            list[idx] = ''
        elif new_value == 'None':
            list[idx] = ''
    return list

def cleanDict(map):
    """Remove unwanted values from dict
        remove Tab,New Line, Text None) ,Text (==)
        Args:
        map: dict
    """
    for k, v in map.iteritems():
        inp_val=v
        if isinstance(v, unicode):
            inp_val=v.encode('utf-8')
        else:
            inp_val=str(v)

        new_value=' '.join(inp_val.split('\t'))
        new_value=' '.join(new_value.split('\n'))
        if new_value == 'None':
            new_value=''
        elif new_value == 'null':
            new_value=''
        elif new_value == '--':
            new_value=''
        map[k]=new_value
    return map

def clean_json_dict(map):
    for k, v in map.items():
        if v == '':
            del map[k]
    return map

def export_entities(entity_list,network_type,entity_type,account_id, data_type,time):
    """ Export data in TSV format
        Args:
        entity_list: List of dict items with each item representing one row and item dict key as header and values
                     as column values
        network_type:  Network type id (Adwords ,AdCenter ,Facebook)
        entity_type:   STATS,ACCOUNT,CAMPAIGN,AD_GROUPS,ADS,KEYWORDS,AD_GROUPS_CRITERION,
                       CAMPAIGN_CRITERION,CAMPAIGN_TARGETS,AD_GROUPS_TARGETS,AD_CREATIVES,AD_IMAGES

        account_id: Account Id
    """
    # File Name and location to export data to.
    logger.debug('Exporting Account Id: {0} List Size: {1} Network Type: {2} Entity Type: {3} '.format(account_id,len(entity_list),network_type,entity_type))
    file_handle=get_export_file_handle(network_type,entity_type,account_id,data_type,time)
    # TSV data export
    tsvWriter(entity_list,file_handle)

def export_deleted_list(entity_list,network_type,entity_type,account_id,time_stamp):
    """ Export list data to file in single column
        Args:
        entity_list: List of items
        network_type:  Network type id (Adwords ,AdCenter ,Facebook)
        entity_type:   STATS,ACCOUNT,CAMPAIGN,AD_GROUPS,ADS,KEYWORDS,AD_GROUPS_CRITERION,
                       CAMPAIGN_CRITERION,CAMPAIGN_TARGETS,AD_GROUPS_TARGETS,AD_CREATIVES,AD_IMAGES

        account_id: Account Id
    """
    # File Name and location to export data to.
    file_handle=get_export_file_handle(network_type,entity_type,account_id,constants.DATA_TYPE_ENTITY,time_stamp,'deleted')
    # TSV data export
    logger.info('Exporting deleted ids ')
    tsvWriter(entity_list,file_handle)

class DictUnicodeProxy(object):
    def __init__(self, d):
        self.d = d
    def __iter__(self):
        return self.d.__iter__()
    def get(self, item, default=None):
        i = self.d.get(item, default)
        if isinstance(i, unicode):
            return i.encode('utf-8')
        return i


def tsvWriter(entity_list,file_handle):
    """ Method to physically export data in TSV BZ2 format
        Args:
        entity_list: List of dict items with each item representing one row and item dict key as header and values
                     as column values.

        file_handle: Location  and file name for data export.
    """
    logger.info('Exporting data in TSV format')
    if len(entity_list) > 0 :
        write_header=settings.EXPORT_HEADER
        if os.path.isfile(file_handle):
            write_header=False
        #f = bz2.BZ2File(file_handle+'.bz2', 'wb')
        f = open(file_handle, 'a+')


        #        f = open(file_handle, 'wt')
        try:
            listHeader=entity_list[0]
            # using \x07 BEL unprintable char hack as quote char in csv writer as there is bug in quoting attribute.
            # Setting quoting attr to csv.QUOTE_NONE does not work.
            dw = csv.DictWriter(f, delimiter='\t', fieldnames=listHeader,quotechar='\x07',doublequote = False,quoting=csv.QUOTE_NONE,escapechar = '\\',extrasaction='ignore')
            if write_header:
                headerRow = {}
                for k, v in listHeader.items():
                    headerRow[k] = k
                dw.writerow(headerRow)
            for row in entity_list:
                if any(x != '' for x in row.itervalues()):
                    dw.writerow(DictUnicodeProxy(row))

        finally:
            f.close()
        logger.debug('Files exported to %s' % file_handle+'.bz2')
    #print open(file_handle, 'rt').read()
    else:
        logger.debug( "Zero list size for file %s" % file_handle)


def export_downloaded_report(file_handle,network_type,entity_type,account,time_stamp):
    try:
        if not os.path.exists(settings.TMP_ROOT_PATH):
            os.makedirs(settings.TMP_ROOT_PATH)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

    fileName, fileExtension = os.path.splitext(file_handle)
    if fileExtension != '.zip':
        tar = tarfile.open(file_handle)
        extract_file_handle=get_export_file_handle(network_type,entity_type,account.ext_ref_code,constants.DATA_TYPE_STATS,time_stamp)
        tar.extractall(path=extract_file_handle)
        tar.close()
    else:
        zip_file = zipfile.ZipFile(file_handle, 'r')
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue

            # copy file (taken from zipfile's extract)
            source = zip_file.open(member)
            fileName, fileExtension = os.path.splitext(filename)
            #            extract_file_handle=get_export_file_handle(network_type,entity_type,account_id)
            extract_file_handle=os.path.join(settings.TMP_ROOT_PATH,filename)
            target = open(extract_file_handle,'wb')
            shutil.copyfileobj(source, target)
            source.close()
            target.close()
            # Do bzip2 compression
            header_line_to_remove=11
            if settings.EXPORT_HEADER:
                header_line_to_remove=10

            source_raw_file = open(extract_file_handle, 'r')
            output_file_handle=get_export_file_handle(network_type,entity_type,account.ext_ref_code,constants.DATA_TYPE_STATS,time_stamp)
            #logger.debug('Raw file contains {0} lines'.format(len(source_raw_file)))
            #output = bz2.BZ2File(output_file_handle+'.bz2', 'wb')
            output = open(output_file_handle, 'a+')

            default_insertions = [hive_formatter.format_datetime(time_stamp), str(account.customer_id), str(account.id)]
            try:
                logger.debug( 'Writing tsv file %s' % output_file_handle)
                for line in read_lines(source_raw_file, header_line_to_remove, 2):
                    columns = line.strip('\r\n').split('\t')
                    columns[0:0] = default_insertions
                    output.writelines('\t'.join( x.strip('"') for x in columns) + '\n')
            finally:
                output.close()
                source_raw_file.close()
            logger.debug( "performing cleanup")
        #            print 'Removing %s' %source_raw_file
        #            os.remove(source_raw_file)
        #            print 'Removing %s' %file_handle
        #            os.remove(file_handle)

        zip_file.close()

    logger.debug( 'Finished extracting file {0} '.format(file_handle))

def read_lines(filehandle, top_lines_to_skip, bottom_lines_to_skip):
    q = Queue.Queue()
    for i, line in enumerate(filehandle):
        if i < top_lines_to_skip + bottom_lines_to_skip:
            if i > (top_lines_to_skip-1):
                q.put(line)
        else:
            q.put(line)
            yield q.get_nowait()

def get_export_folder_location(network_type,account_id,data_type,time_stamp):
    year=time_stamp.strftime("%Y")
    month=time_stamp.strftime("%m")
    day=time_stamp.strftime("%d")
    wholeSecondsString = time_stamp.strftime("%H%M%S")
    network_folder=get_network_folder_name(network_type)
    return os.path.join(constants.EXPORT_FOLDER_LOCATION,year,month,day,network_folder,str(account_id),data_type,wholeSecondsString)

def get_export_file_handle(network_type,entity_type,account_id,data_type,time_stamp,file_name_tag=None):
    folder_location = get_export_folder_location(network_type,account_id,data_type,time_stamp)
    entity_file=get_entity_file_name(entity_type)
    try:
        if not os.path.exists(folder_location):
            os.makedirs(folder_location)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
    if file_name_tag:
        fileName=entity_file+'_'+file_name_tag+constants.EXPORT_FILE_EXTENTION
    else:
        fileName=entity_file+constants.EXPORT_FILE_EXTENTION
    file_handle=os.path.join(folder_location,fileName)
    return file_handle



def get_network_folder_name(network_type):
    return {
        constants.NETWORK_TYPE_AD_CENTER:constants.NETWORK_TYPE_AD_CENTER,
        constants.NETWORK_TYPE_AD_WORDS:constants.NETWORK_TYPE_AD_WORDS,
        constants.NETWORK_TYPE_CCT:constants.NETWORK_TYPE_CCT,
        constants.NETWORK_TYPE_FACEBOOK:constants.NETWORK_TYPE_FACEBOOK,
        constants.NETWORK_TYPE_PRO:constants.NETWORK_TYPE_PRO,
        constants.NETWORK_TYPE_DISTIMO: constants.NETWORK_TYPE_DISTIMO,
        constants.NETWORK_TYPE_CLICKY: constants.NETWORK_TYPE_CLICKY,
        constants.NETWORK_TYPE_GOOGLE_ANALYTICS: constants.NETWORK_TYPE_GOOGLE_ANALYTICS
    }[network_type]


def get_entity_file_name(entity_type):
    return {
        constants.ENTITY_TYPE_STATS   :   constants.ENTITY_TYPE_STATS,
        constants.ENTITY_TYPE_ACCOUNT   :   constants.ENTITY_TYPE_ACCOUNT,
        constants.ENTITY_TYPE_CAMPAIGN   :   constants.ENTITY_TYPE_CAMPAIGN,
        constants.ENTITY_TYPE_AD_GROUPS   :   constants.ENTITY_TYPE_AD_GROUPS,
        constants.ENTITY_TYPE_ADS   :   constants.ENTITY_TYPE_ADS,
        constants.ENTITY_TYPE_KEYWORDS   :   constants.ENTITY_TYPE_KEYWORDS,
        constants.ENTITY_TYPE_CAMPAIGN_TARGETS   :   constants.ENTITY_TYPE_CAMPAIGN_TARGETS,
        constants.ENTITY_TYPE_AD_GROUPS_TARGETS   :   constants.ENTITY_TYPE_AD_GROUPS_TARGETS,
        constants.ENTITY_TYPE_CAMPAIGN_CRITERION:constants.ENTITY_TYPE_CAMPAIGN_CRITERION,
        constants.ENTITY_TYPE_AD_GROUPS_CRITERION:constants.ENTITY_TYPE_AD_GROUPS_CRITERION,
        constants.ENTITY_TYPE_AD_CREATIVES:constants.ENTITY_TYPE_AD_CREATIVES,
        constants.ENTITY_TYPE_AD_IMAGES:constants.ENTITY_TYPE_AD_IMAGES,
        constants.SYNC_TYPE_STATS:constants.SYNC_TYPE_STATS,
        constants.SYNC_TYPE_ENTITIES:constants.SYNC_TYPE_ENTITIES
    }.get(entity_type, entity_type)

def logClientResult(client):
    if doLogClientRequest is True :
        sent = client.last_sent()
        received = client.last_received()
        logger.debug( '\n sent(\n%s\n)\n' % sent)
        logger.debug( '\n reply(\n%s\n)\n' % received)

def touch_file(network_type,account_id,data_type,time_stamp,sync_type,status):
    file_handle=get_export_file_handle(network_type,sync_type,account_id,data_type,time_stamp)
    fileName, fileExtension = os.path.splitext(file_handle)
    touch_file_name=fileName+'.'+status
    open(touch_file_name, 'w').close()
    logger.debug('created touch file {0}'.format(touch_file_name))

def month_date_range_list(date1,date2):
    #Monthly breakup for the input dates

    dt1, dt2 = date1,date2
    start_month=dt1.month
    end_months=(dt2.year-dt1.year)*12 + dt2.month+1
    dates=[datetime(year=yr, month=mn, day=1, tzinfo=date1.tzinfo) for (yr, mn) in (
        ((m - 1) / 12 + dt1.year, (m - 1) % 12 + 1) for m in range(start_month, end_months)
    )]
    #Update start and end dates in the list from default 1
    dates[0]=dates[0].replace(day=date1.day)
    dates[-1]=dates[-1].replace(day=date2.day)
    #print  dates
    stats_dates=[]
    if len(dates) > 1:
        for monthly in range(0,len(dates)):
            start_date=None
            end_date=None
            if monthly != (len(dates)-1):
                start_date=dates[monthly]
                first_day,last_day=calendar.monthrange(dates[monthly].year,dates[monthly].month)
                end_date=dates[monthly].replace(day=last_day)
            else:
                start_date=dates[monthly].replace(day=1)
                end_date=dates[monthly]
            stat_range=(start_date,end_date)
            stats_dates.append(stat_range)
    else:
        stats_dates.append((date1,date2))
    return  stats_dates


def handleException(network_exception,retry_counter):
    retry=False
    if 'Connection reset by peer' in network_exception or isinstance(network_exception,URLError):
        logger.exception("Error while connecting to webservice..retrying {0}".format(retry_counter))
        retry=True
        time.sleep(settings.NETWORK_RETRY_SLEEP_TIME)
        retry_counter-=1
        if retry_counter == 0:
            retry=False
            logger.exception("Retry limit reached exiting")
            logger.exception("Exception  :Reason network error")
    else:
        logger.exception('Exception ')
    return retry,retry_counter

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
           reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
                  [(t*1000,),1000,60,60])

def _decode_list(data):
    """ Helper class to convert unicode string from facebook to it's ASCII representation
        Args:
            data: list ,dict string value
    """
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    """ Helper class to convert unicode string from facebook to it's ASCII representation
        Args:
        data: dict
    """

    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def dict_url_params(params):
    url=''
    for k,v in params.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf-8')
        url=url+'&'+k+'='+str(v)
    return url


def web_request(url, prefix_to_be_trimmed=None,retry_counter=settings.FACEBOOK_RETRY_COUNTER, log_errors=True, params=None):
    """ Method to sent the web request
        Args:
            url: http/https url where the POST/GET request will be sent
    """
    response = None
    try:
        response = sendAndReceive(url, log_errors=log_errors, parameters=params)
        json_str=''
        json_response=None
        if response is not None:
            if isinstance(response, Exception):
                raise response
            json_str=response.read()
        if prefix_to_be_trimmed and json_str.startswith(prefix_to_be_trimmed):
            json_str = json_str[len(prefix_to_be_trimmed):]
        try:
            json_response = json.loads(json_str,object_hook=_decode_dict)
        except ValueError,e:
            logger.warning('Unable to decode json string input value url : {0} Exception Message : {1} '.format(url , e.message))
            raise
    finally:
        try:
            if response:
                response.close()
        except:
            pass
    return json_response


class HttpRequestType:
    GET = 'GET'
    POST = 'POST'
    MULTIPART='multipart'
    PUT = 'PUT'
    DELETE = 'DELETE'


def sendAndReceive(url, parameters = None, httpRequestType = HttpRequestType.GET, data = None, headers = {},
                   retry_counter=settings.FACEBOOK_RETRY_COUNTER, network_type=constants.NETWORK_TYPE_FACEBOOK,
                   log_errors=True ,http_time_out_in_seconds=None):
    """
        Form Data={
            upload_attribute=''
            file_path:url of the remote or local file
        }
    """
    logger.debug('Inside sendAndReceive (retry counter:{0})'.format(retry_counter))
    response = None
    retry = False
    orig_ex = None
    try:
        logger.debug('Request Type: {0} URL: {1} parameters: {2} data: {3}'.format(httpRequestType,url,parameters,data))
        if httpRequestType == HttpRequestType.GET:
            full_url = url
            if parameters is not None:
                url_values = urllib.urlencode(parameters)
                #                url_values = dict_url_params(parameters)
                full_url = url + '?' + url_values

            response = (urllib2.urlopen(full_url) if http_time_out_in_seconds is None else urllib2.urlopen(full_url,timeout=http_time_out_in_seconds) )

        elif httpRequestType in HttpRequestType.POST:
            if headers is None:
                headers = {}
            logger.debug(dict_url_params(parameters))
            request = urllib2.Request(url, urllib.urlencode(parameters))
            response=urllib2.urlopen(request)
        elif httpRequestType in HttpRequestType.DELETE:
            if headers is None:
                headers = {}
            logger.debug(dict_url_params(parameters))
            request = urllib2.Request(url, urllib.urlencode(parameters))
            request.get_method = lambda: HttpRequestType.DELETE
            response=urllib2.urlopen(request)
        elif httpRequestType in HttpRequestType.PUT:
            if headers is None:
                headers = {}
            logger.debug(parameters)
            request = urllib2.Request(url, parameters)
            request.add_header('Content-Type', 'application/json')
            request.get_method = lambda: HttpRequestType.PUT
            response=urllib2.urlopen(request)


        elif  httpRequestType == HttpRequestType.MULTIPART:
            form = MultiPartForm()

            for key in parameters.keys():
                form.add_field(key,parameters[key])

            file_path=data['file_path']
            file_name = os.path.basename(file_path)
            if re.search('http://', file_path, re.IGNORECASE):
                file = sendAndReceive(file_path,http_time_out_in_seconds=http_time_out_in_seconds)
            else:
                file = open(file_path)

            form.add_file(data['upload_attribute'], file_name, file)
            request = urllib2.Request(url)
            body = str(form)
            request.add_header('Content-type', form.get_content_type())
            request.add_header('Content-length', len(body))
            request.add_data(body)
            response = urllib2.urlopen(request)
    except IOError as e:
        orig_ex = e
        retry = True
        if hasattr(e, 'code'):
            if network_type == constants.NETWORK_TYPE_FACEBOOK :
                if e.code in [400,500] :
                    retry = False
                    response=e
                    if log_errors:
                        logger.debug('Logical {0} error at facebook '.format(e.code))
                        if hasattr(e, 'reason'):
                            logger.error('Reason: {0}'.format(e.reason))
                        logger.error(response)
            else:
                logger.error("The server couldn't fulfill the request.")
                logger.error('Error code: {0}'.format(e.code))
        elif hasattr(e, 'reason'):
            logger.error('Failed to reach a server.')
            logger.error('Reason: {0}'.format(e.reason))
        else:
            logger.error('Unable to parse exception {0}'.format(e))
    except Exception, ex:
        orig_ex = ex
        retry = True
        logger.info('SendAndReceive catchAll Exception')
        logger.error('sendAndReceive :: exception sending the web request - Request Type: {0} URL: {1} parameters: {2} data: {3}. Error: {4}'.format(httpRequestType,url,parameters,data,repr(ex)))
    if retry:
        if retry_counter > 0:
            logger.debug('Retrying web request {0} sleeping for {1} seconds'.format(retry_counter, settings.NETWORK_RETRY_SLEEP_TIME))
            retry_counter -= 1
            time.sleep(settings.NETWORK_RETRY_SLEEP_TIME)
            response = sendAndReceive(url, parameters, httpRequestType, data, headers, retry_counter , network_type,log_errors,http_time_out_in_seconds)
        else:
            error_msg = 'Web request retry limit reached for url:{0} exiting sendAndReceive. Error: {1}'.format(url, orig_ex.message)
            raise Exception(error_msg)
    return response

def get_svn_revision():
    try:
        from subprocess import Popen, PIPE
        _p = Popen(["svnversion", "."], stdout=PIPE)
        REVISION= _p.communicate()[0]
        _p = None # otherwise we get a wild exception when Django auto-reloads
    except Exception, e:
        print "Could not get revision number: ", e
        REVISION="Unknown"
    return REVISION

def getBatches(user_timezone, dataStartDt, dataEndDt=None):
    batches = []
    utc_tz=pytz.utc
    min_hour_time=dt.time(0,0,0)
    #convert start time to 00:00:00 start of day time
    start_time=user_timezone.localize(dt.datetime.combine(dataStartDt.date(), min_hour_time))
    end_time=dataEndDt
    now=dt.datetime.now(tz=user_timezone)
    one_day = dt.timedelta(days=1)
    one_second = dt.timedelta(seconds=1)

    delta = (end_time.date()-start_time.date() ).days
    if delta == 0 :
        end_time=start_time+one_day

    start_day=start_time
    end_day=end_time

    for index in range(delta+1):
        if start_day.date() <= end_day.date():
            next_day=start_day+one_day
            last_update_timestamp = now if (start_day.date() == now.date()) else (next_day - one_second)
            batches.append((start_day.astimezone(utc_tz),next_day.astimezone(utc_tz), start_day, last_update_timestamp))
            #print (start_day,next_day,last_update_timestamp)
            start_day += one_day

    return batches


class dict2obj(dict):
    def __init__(self, dict_):
        super(dict2obj, self).__init__(dict_)
        for key in self:
            item = self[key]
            if isinstance(item, list):
                for idx, it in enumerate(item):
                    if isinstance(it, dict):
                        item[idx] = dict2obj(it)
            elif isinstance(item, dict):
                self[key] = dict2obj(item)

    def __getattr__(self, key):
        if key.startswith('__'):
            raise AttributeError
        return self.get(key)

def obj2dict(obj, classkey=None):
    if isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = obj2dict(obj[k], classkey)
        return obj
    elif hasattr(obj, "__iter__"):
        return [obj2dict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, obj2dict(value, classkey))
        for key, value in obj.__dict__.iteritems()
        if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj

def add_dictionary_item(key, value, dictionary={}):
    if key in dictionary:
        dictValue = dictionary[key]
        dictValue.append(value)
    else:
        dictValue = list()
        dictValue.append(value)
        dictionary[key] = dictValue
    return dictionary

def pretty_print(xml_string):
    root = etree.fromstring(xml_string)
    return etree.tostring(root, pretty_print=True)

def sort_dict(d):
    if isinstance(d, dict):
        d = collections.OrderedDict(sorted(d.items()))
        for k,v in d.iteritems():
            #print k,v
            if isinstance(v, dict):
                #print 'Dict Instance {0}'.format(k)
                d[k]=sort_dict(v)
            if isinstance(v, list):
                for item in v:
                    sort_dict(item)
    return d


#Region for ABI_KPI_DASHBOARD project specific methods
def get_abi_kpi_report_file_path(network_type, report_date, time_stamp):
    year=time_stamp.strftime("%Y")
    month=time_stamp.strftime("%m")
    day=time_stamp.strftime("%d")
    wholeSecondsString = time_stamp.strftime("%H%M%S")
    network_folder=get_network_folder_name(network_type)
    folder_location = os.path.join(constants.CSV_EXPORT_FOLDER_LOCATION,year,month,day,network_folder,wholeSecondsString)
    try:
        if not os.path.exists(folder_location):
            os.makedirs(folder_location)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
    file_name = constants.GET_ABI_KPI_FILE_NAME_TEMPLATE.format(network_type,report_date.strftime('%d_%m_%Y'))
    complete_file_path = os.path.join(folder_location, file_name)
    return complete_file_path, file_name
