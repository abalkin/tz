"""PEP 495 compliant tzinfo implementation."""
import os
import pickle
from . import metadata
from .zoneinfo import tzinfo, ZoneInfo

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
    def __new__(cls, name=None):
        if name is None:
            return object.__new__(cls)
        if '/' not in name:
            try:
                self = cls.load(name)
                tzinfo.cache.update(self.all)
                return self
            except (FileNotFoundError, EOFError):
                pass
        self = object.__new__(cls)
        self.name = name
        self.all = {}
        for loc in ZoneInfo.list_area(name):
            if loc.endswith('/'):
                loc = loc[:-1]
                area = Area('/'.join([name, loc]))
                setattr(self, loc.replace('-', ''), area)
            else:
                tzid = '/'.join([name, loc])
                info = ZoneInfo.fromname(tzid)
                info.tzrepr = clean_name(tzid)
                setattr(self, loc.replace('-', ''), info)
                self.all[tzid] = tzinfo.cache[tzid] = info
        if '/' not in name:
            self.save()
        return self

    def __repr__(self):
        cls = type(self)
        return "%s.%s(%r)" % (cls.__module__, cls.__name__, self.name)

    @classmethod
    def load(cls, name):
        path = os.path.join(PKG_DIR, name + '.pkl')
        with open(path, 'br') as f:
            return pickle.load(f)

    def save(self):
        path = os.path.join(PKG_DIR, self.name + '.pkl')
        with open(path, 'bw') as f:
            return pickle.dump(self, f, 4)

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
