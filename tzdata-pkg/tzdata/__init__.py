import os
from datetime import datetime, timedelta
DATA_DIR = os.path.dirname(__file__)
_zones = None


class ZoneData:
    source = 'iana'
    types = []
    times = []
    rules = None


def zones(area=None):
    global _zones
    if _zones is None:
        zones_path = os.path.join(DATA_DIR, 'zones')
        _zones = []
        with open(zones_path) as f:
            for line in f:
                _zones.append(line.strip())
    for z in _zones:
        if area is None or z.startswith(area + '/'):
            yield z


def aliases(area=None):
    return []


def delta(x):
    try:
        return timedelta(hours=x)
    except TypeError:
        kwds = {name: value for name, value in zip(['hours', 'minutes',
                                                    'seconds'], x)}
        return timedelta(**kwds)


def get(tzid):
    """Return timezone data"""
    ns = {}
    path = os.path.join(DATA_DIR, tzid)
    with open(path) as f:
        raw_data = f.read()
    exec(raw_data, ns, ns)
    z = ZoneData()
    z.types = [(delta(offset), delta(save), abbr)
               for offset, save, abbr in ns['types']]
    z.times = [(datetime(*time), i)
               for time, i in ns['times']]
    z.rules = ns['posix']
    return z
