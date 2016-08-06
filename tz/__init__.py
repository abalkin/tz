"""PEP 495 compliant tzinfo implementation."""
from . import metadata
from .zoneinfo import ZoneInfo

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright


def get(name):
    return ZoneInfo.fromname(name)


class Area:
    def __init__(self, name):
        self.name = name
        for loc in ZoneInfo.list_area(name):
            if loc.endswith('/'):
                loc = loc[:-1]
                area = Area('/'.join([name, loc]))
                setattr(self, loc.replace('-', ''), area)
            else:
                info = ZoneInfo.fromname('/'.join([name, loc]))
                setattr(self, loc.replace('-', ''), info)

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
