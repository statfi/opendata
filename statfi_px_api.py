# -*- coding: UTF-8 -*-

"""
This module contains tools to load information about PC Axis files in
Statistics Finland's databases and download the files from the databases
using the open data API:
http://www.stat.fi/org/lainsaadanto/avoin_data_en.html
"""


import csv, datetime, urllib
import csv_tools

class PxInfo(object):
    """
    A simple object representation of PX information in 
    Statistics Finland's open data API:
    """

    _timeformat = '%Y-%m-%d %H:%M' #Just a cache place for dateformat

    def __init__(self, path, size, created, updated, variables,
tablesize, type, language, title, *args):
        self.path = path.strip()
        self.size = size.strip()
        self.created = created.strip()
        self.updated = updated.strip()
        self.variables = variables.strip()
        self.tablesize = tablesize.strip()
        self.type = type.strip()
        self.language = language.strip()
        self.title = title.strip()

    def __unicode__(self):
        return u'PX file %s: %s' % (self.path, self.title)

    def __repr__(self):
        return unicode(self).encode('utf-8')

    @property
    def created_dt(self):
        return datetime.datetime.strptime(self.created, self._timeformat)

    @property
    def updated_dt(self):
        return datetime.datetime.strptime(self.updated, self._timeformat)

def create_px(url="http://pxweb2.stat.fi/database/StatFin/StatFin_rap.csv"):
    """
    Creates a list of Px-objects from a given url. Url should point to a CSV file.
    Url's default value points to Statfin databases contents CSV.
    """
    iterable = urllib.urlopen(url)
    iterable.next() #First line is for metadata
    return [PxInfo(*i) for i in csv_tools.UnicodeReader(iterable, delimiter=";", encoding="iso-8859-1")]

def fetch_px_zipped(px_objs, target_dir="."):
    """
    Fetch PC Axis files for given list of Px objects with gzip compression on the transfer
    Modified from http://www.diveintopython.net/http_web_services/gzip_compression.html
    Save the files to target directory

    WARNING: Statfin database contains over 2500 PX files with many gigabytes of data.
    """
    import urllib2, httplib, StringIO, gzip, os.path, time
    opener = urllib2.build_opener()
    for px_obj in px_objs:
        base, pxfile_path = os.path.split(px_obj.path)
        pxfile = open(os.path.join(target_dir, pxfile_path), 'w+')
        request = urllib2.Request(px_obj.path)
        request.add_header('Accept-encoding', 'gzip')
        f = opener.open(request)
        compressedstream = StringIO.StringIO(f.read())
        try:
            for data in gzip.GzipFile(fileobj=compressedstream):
                pxfile.write(data)
            print f.headers
        except IOError, e:
            print e, px_obj, f.headers
            break
        pxfile.close()
        time.sleep(1)

def fetch_px(px_objs, target_dir="."):
    """
    Fetch PC Axis files for given list of Px objects
    Save the files to target directory

    WARNING: Statfin database contains over 2500 PX files with many gigabytes of data.
    """
    import urllib2, httplib, StringIO, gzip, os.path
    opener = urllib2.build_opener()
    for px_obj in px_objs:
        base, pxfile_path = os.path.split(px_obj.path)
        pxfile = open(os.path.join(target_dir, pxfile_path), 'w+')
        request = urllib2.Request(px_obj.path)
        f = opener.open(request)
        try:
            for data in f.read():
                pxfile.write(data)
        except IOError, e:
            print e, px_obj, f.headers
            break
        pxfile.close()
