import sys
from array import array
from datetime import timedelta
from tz.zoneinfo import ZoneModule
sys.modules[__name__].__class__ = ZoneModule
ut, ti = array('q', []), [(timedelta(0), 0, 'UTC')] * 0
posix_rules = None
