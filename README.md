# opendata

Statistics Finland's tools and examples for use with our open data API.

Information about our Open Data API can be found here: http://www.stat.fi/org/lainsaadanto/avoin_data_en.html

## statfi_px_api.py

This script loads the database contents CSV given one of the URLs above and creates a list of objects containing the CSV information in an easy to use form.

Use functions fetch_px and fetch_px_zipped to download statistical data files from a database.

WARNING: Statfin database contains over 2500 PX files with many gigabytes of data. 

## px_reader.py

### Status

This module is in beta at the moment. I have run it against 2500+ PX documents inside our Statfin database and encountered only a handful of problems. With few files which contain police domains (http://www.stat.fi/til/pkei/) reader will use all available memory and CPU, so be warned. Additionally files with KEYES data format (which is used with large amounts of zeroes) or files missing heading or row variables are not supported. In all less than 10 files are unreadable.

### Features

Notable feature is conversion to a [Pandas][pandas] DataFrame using MultiIndex, which supports multidimensional table object. Pandas calls this [hierarchical indexing][pandas indexing]. Pandas has an [extensive feature list][pandas features]. Thus you can use PC Axis files for data analysis, visualization and export to other data formats.

Installing scientific Python toolset can be a daunting task. One option is the [Anaconda distribution][anaconda]. Otherwise Pandas installation may work with just `pip install pandas`. This code is unsupported, but please create an issue if you run into problems.

[anaconda]: http://continuum.io/downloads.html
[pandas]: http://pandas.pydata.org/
[pandas features]: http://pandas.pydata.org/#library-highlights
[pandas indexing]: http://pandas.pydata.org/pandas-docs/stable/indexing.html#hierarchical-indexing-multiindex

License
-------

All code here is under the BSD license unless otherwise stated. Otherwise Mozilla public license (MPL) is used since it supports both open and proprietary development alike.
