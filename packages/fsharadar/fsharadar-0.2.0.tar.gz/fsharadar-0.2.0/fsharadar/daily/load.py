# load() and associated methods implemented from
# the corresponding originals within zipline/data/bundles/core.py
# for connecting BundleData with sharadar-specific bundle and reader.

import os
import errno
from toolz import complement
from contextlib2 import ExitStack
import pandas as pd

from trading_calendars import get_calendar

import zipline.utils.paths as pth
from zipline.assets import AssetFinder
from zipline.data.bundles import bundles
from zipline.data.bundles import UnknownBundle
from zipline.data.bundles import from_bundle_ingest_dirname
from zipline.data.bundles.core import BundleData
from zipline.data.bundles.core import asset_db_path, daily_equity_path

from fsharadar.load import most_recent_data
from fsharadar.bcolz_reader_float64 import SharadarDailyBcolzReader

from fsharadar.daily.meta import bundle_name, bundle_tags

def load():

    # original arguments
    name = bundle_name
    environ=os.environ
    timestamp=None

    if timestamp is None:
        timestamp = pd.Timestamp.utcnow()
    timestr = most_recent_data(name, timestamp, environ=environ)
    
    return BundleData(
        asset_finder=AssetFinder(
            asset_db_path(name, timestr, environ=environ),
        ),
        equity_minute_bar_reader=None,
        equity_daily_bar_reader=SharadarDailyBcolzReader(
            daily_equity_path(name, timestr, environ=environ),
            bundle_tags=bundle_tags,
        ),
        adjustment_reader=None,
    )

