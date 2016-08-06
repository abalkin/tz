"""PEP 495 compliant tzinfo implementation."""
import os
import pickle
from . import metadata
from .zoneinfo import ZoneInfo

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright

PKG_DIR = os.path.dirname(__file__)


def get(name):
    return ZoneInfo.fromname(name)


class Area:
    def __new__(cls, name=None):
        if name is None:
            return object.__new__(cls)
        if '/' not in name:
            try:
                return cls.load(name)
            except (FileNotFoundError, EOFError):
                pass
        self = object.__new__(cls)
        self.name = name
        for loc in ZoneInfo.list_area(name):
            if loc.endswith('/'):
                loc = loc[:-1]
                area = Area('/'.join([name, loc]))
                setattr(self, loc.replace('-', ''), area)
            else:
                info = ZoneInfo.fromname('/'.join([name, loc]))
                setattr(self, loc.replace('-', ''), info)
        if '/' not in name:
            self.save()
        return self

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
