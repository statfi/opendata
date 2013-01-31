opendata
========

Statistics Finland's tools and examples for use with our open data API.

Information about our Open Data API can be found here: http://www.stat.fi/org/lainsaadanto/avoin_data_en.html

statfi_px_api.py
----------------

This script loads the database contents CSV and creates a list of objects containing the CSV information in an easy to use form.

Additionally fetch_px and fetch_px_zipped can be used to download statistical data as PX files from the database.

WARNING: Statfin database contains over 2500 PX files with many gigabytes of data. 

px_reader.py
------------

This is alpha level module, very much a work in progress. However it works with a dozen PC Axis files from Statfin database. I'll test it againts the whole database when I manage to create a script to run this across 2000+ documents therein.

Notable feature is conversion to a [Pandas][pandas] DataFrame using MultiIndex, which is a multidimensional table object. Pandas has an [extensive feature list][pandas features]. Thus you can use PC Axis files for data analysis, visualization and export to other data formats.

Installing scientific Python toolset can be a daunting task. One option is the [Anaconda distribution][anaconda]. Otherwise Pandas installation may be just `pip install pandas` away. This code is unsupported, but please create an issue if you run into problems.

[anaconda]: http://continuum.io/downloads.html
[pandas]: http://pandas.pydata.org/
[pandas features]: http://pandas.pydata.org/#library-highlights

License
-------

All code here is under the BSD license unless otherwise stated. Otherwise Mozilla public license (MPL) is used since it supports both open and proprietary development alike.