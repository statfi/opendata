# -*- coding: utf-8 -*-

# Copyright (c) 2012,2013 Statistics Finland
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains a Px class which parses the PX file structure including meta

In addition there is a conversion functionality to create a Pandas DataFrame object with MultiIndex
(multidimensional table) from PX data

Note: Python 2.7 support required
"""

import resource, logging, re, codecs
from collections import OrderedDict as OD
from collections import defaultdict
from itertools import izip_longest, cycle, repeat
from operator import mul
import pandas as pd

def get_logger(level=logging.DEBUG, handler=logging.StreamHandler):
    """
    Adapted from logging module's documentation.
    """
    log = logging.getLogger('px_log')
    log.setLevel(level)
    ch = handler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    ch.set_name('px_handler')
    existing_handlers = [h for h in log.handlers if h.name == ch.name]
    if not existing_handlers:
        log.addHandler(ch)
    return log

class Px(object):
    """
    PC Axis document structure as a object interface

    Creates dynamically fields containing everything from PC Axis file's metadata part
    (excluding multilingual fields for the moment #FIXME multilingual fields)
    """
    
    _timeformat = '%Y-%m-%d %H:%M'
    _subfield_re = re.compile(r'^(.*?)\("(.*?)"\)=')
    _items_re = re.compile(r'"(.*?)"')

    log = get_logger()

    def _get_subfield_name(self, field):
        m = self._subfield_re.search(field)
        if m:
            return m.groups()

    def _clean_value(self, value):
        items = self._items_re.findall(value)
        if len(items) == 1:
            return items.pop()
        else:
            return items

    def _get_subfield(self, m, line):
        field, subkey = m.groups()
        value = line[m.end():]
        return field.lower(), subkey, self._clean_value(value)

    def _split_px(self, px_doc):
        """
        Parses metadata keywords from px_doc and inserts those into self object
        Returns the data part
        """
        meta, data = open(px_doc, 'U').read().split("DATA=")
        meta = unicode(meta, 'iso-8859-1')
        data = unicode(data, 'iso-8859-1')
        nmeta = {}
        for line in meta.strip().split(';\n'):
            if line:
                m = self._subfield_re.match(line)
                if m:
                    field, subkey, value = self._get_subfield(m, line)
                    if hasattr(self, field):
                        getattr(self, field)[subkey] = value
                    else:
                        setattr(self, field, OD(
                            [(subkey, value)]
                            ))
                else: 
                    field, value = line.split('=', 1)
                    if not field.startswith('NOTE'):
                        setattr(self, field.strip().lower(), self._clean_value(value))
                        #TODO: NOTE keywords can be standalone or have subfields...
        return data.strip()[:-1]
   
    def __init__(self, px_doc):
        data = self._split_px(px_doc)
        self._data = data.replace('"', '')

        if type(self.stub) != type(list()):
            self.stub = [self.stub]

        if type(self.heading) != type(list()):
            self.heading = [self.heading]

        for key, val in self.values.items():
            if type(val) != type(list()):
                self.values[key] = [val]

        #
        # Number of rows and cols is multiplication of number of variables for both directions
        #
        self.cols = reduce(mul, [len(self.values.get(i)) for i in self.heading], 1)
        self.rows = reduce(mul, [len(self.values.get(i)) for i in self.stub], 1)
    
   # def __unicode__(self):
  #      return u'PX file %s: %s' % (self.name, self.title)
   
    #def __repr__(self):
    #    return unicode(self)
   
    @property
    def created_dt(self):
        return datetime.datetime.strptime(self.created, self._timeformat)
   
    @property
    def updated_dt(self):
        return datetime.datetime.strptime(self.updated, self._timeformat)

    @property
    def data(self):
        return list(grouper(self.cols, self._data.split()))

    def pd_dataframe(self):
        """
        Shortcut function to return Pandas DataFrame build from PX file's structure
        """
        return build_dataframe(self)

def grouper(n, iterable, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks
    Lifted from itertools module's examples
    """
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def index(px):
    """
    Pandas has a concept of MultiIndex for hierarchical or multidimensional tables
    PC Axis files have list of column and row variables (can be thought of as column
    and row headings for the purposes of this documentation)

    Lowest level (last in the list) variable is repeated for exactly one
    column or row each till all columns/rows have a variable

    Going up the convention states that upper level variable groups lower level variable.

    Since Pandas MultiIndex excepts certain format for its variable structure:

    first level : [val1, val1, val1, val1, val2, val2, val2, val2]
    second level: [valx, valx, valz, valz, valx, valx, valz, valz]
    third level : [vala, valb, vala, valb, vala, valb, vala, valb] the lowest level

    This is one algorithm for generating repeating variable values from PX table structure
    First level/dimension:
        repeat = cols or rows / number of level's values
    Second level:
        repeat = first iterations repeat/ number of second level's values
    And so on

    Example:
    cols = 12
    first level values = 2
    second level values = 3
    third level values = 3
    12/2 = 6
    6 / 2 = 3
    3 / 3 = 1
    """
    col_index = []
    rep_index = px.cols
    for n, field in enumerate(px.heading):
        field_values = px.values.get(field)
        repeats = rep_index / len(field_values)
        rep_index = repeats
        print field, repeats

        col_index.append(list())
        index = 0
        values = cycle(field_values)
        value = values.next()
        for i, rep in enumerate(range(px.cols)):
            if index == repeats:
                index = 0
                value = values.next()
            index += 1
            col_index[n].append(value)
    row_index = []
    rep_index = px.rows
    for n, field in enumerate(px.stub):
        field_values = px.values.get(field)
        repeats = rep_index / len(field_values)
        rep_index = repeats
        print field, repeats

        row_index.append(list())
        index = 0
        values = cycle(field_values)
        value = values.next()
        for i, rep in enumerate(range(px.rows)):
            if index == repeats:
                index = 0
                value = values.next()
            index += 1
            row_index[n].append(value)
    return col_index, row_index

def build_dataframe(px):
    """
    Build a Pandas DataFrame from Px rows and columns
    """
    cols, rows = index(px)
    col_index = pd.MultiIndex.from_arrays(cols)
    row_index = pd.MultiIndex.from_arrays(rows)
    return pd.DataFrame(px.data, index=row_index, columns=col_index)
