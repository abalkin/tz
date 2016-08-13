"""PEP 495 compliant tzinfo implementation."""
import os
import pickle
from . import metadata
from .zoneinfo import tzinfo, ZoneInfo

try:
    import tzdata
except ImportError:
    from . import system_tzdata as tzdata

__all__ = ['America', 'Europe', 'Australia', 'Antarctica',  'Asia', 'Africa',
           'Arctic', 'Pacific', 'Atlantic', 'Indian', 'tzinfo']

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright

PKG_DIR = os.path.dirname(__file__)
CHAR_MAP = {
    ord('/'): '.',
    ord('-'): '_',
    ord('.'): None,
}


def get(name):
    return eval(name)


def clean_name(area_id):
    return area_id.translate(CHAR_MAP)


class Area:
    def __init__(self, name):
        self.name = name
        self.subareas = None
        self.zones = None

    def __dir__(self):
        zones, subareas = self.get_dir()

        return sorted(zones) + sorted(subareas)

    def __getattr__(self, item):
        zones, subareas = self.get_dir()
        name = self.name + '/' + item
        if item in subareas:
            attr = Area(name)
        elif item in zones:
            data = tzdata.get(name)
            attr = ZoneInfo.fromdata(data.types, data.transitions)
        else:
            raise AttributeError(item)
        setattr(self, item, attr)
        return attr

    def get_dir(self):
        subareas = set()
        zones = set()
        if self.zones is None:
            n = len(self.name) + 1
            for name in tzdata.zones(self.name):
                assert name[:n-1] == self.name
                i = name.find('/', n + 1)
                if i == -1:
                    zones.add(name[n:])
                else:
                    subareas.add(name[n:i])
            self.subareas = subareas
            self.zones = zones
        else:
            zones = self.zones
            subareas = self.subareas
        return zones, subareas

# Continents
America = Area('America')
Europe = Area('Europe')
Australia = Area('Australia')
Antarctica = Area('Antarctica')
Asia = Area('Asia')
Africa = Area('Africa')

# Oceans
Arctic = Area('Arctic')
Pacific = Area('Pacific')
Atlantic = Area('Atlantic')
Indian = Area('Indian')

# Let's not mess with ZoneInfo pickling until tz namespace is ready
ZoneInfo.__reduce__ = ZoneInfo.make_reduce(get)
