import os
from datetime import timedelta, datetime

from . import tzfile
from .tzfile import is_tzfile

__all__ = ['zones', 'aliases', 'get']

zoneinfo_dir = '/usr/share/zoneinfo'

_zones = []
_aliases = {}


class ZoneData:
    source = 'system'
    observances = []
    transitions = []
    posix_string = None


def zones(area=None):
    if not _zones:
        zone_tab = os.path.join(zoneinfo_dir, 'zone.tab')
        with open(zone_tab) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    zone = line.split()[2]
                    _zones.append(zone)
    if area is None:
        return _zones

    return [z for z in _zones if z.startswith(area + '/')]


def aliases(area=None):
    if not _aliases:
        zone_set = set(zones())
        inos = {}
        targets = {}
        n = len(zoneinfo_dir) + 1
        for root, _, files in os.walk(zoneinfo_dir):
            for f in files:
                p = os.path.join(root, f)
                stats = os.stat(p)
                if stats.st_nlink > 1 and is_tzfile(p):
                    zone = p[n:]
                    inos[zone] = i = stats.st_ino
                    if zone in zone_set:
                        targets[i] = zone
        for zone, i in inos.items():
            t = targets.get(i)
            if t is not None and t != zone:
                _aliases[zone] = t
    if area is None:
        return _aliases

    return {a: t for a, t in _aliases.items() if a.startswith(area + '/')}


SECOND = timedelta(0, 1)
UNIX_EPOCH = datetime(1970, 1, 1)
CREATION = (datetime(1, 1, 1) - UNIX_EPOCH) // SECOND


def get(zone):
    path = os.path.join(zoneinfo_dir, zone)
    with open(path, 'br') as f:
        raw_data = tzfile.read(f)
    data = ZoneData()
    data.observances = [
        (timedelta(seconds=gmtoff),
         timedelta(hours=is_std),
         abbr) for gmtoff, is_std, abbr in raw_data.type_infos]
    data.transitions = [
        (UNIX_EPOCH + timedelta(seconds=max(CREATION, t)), i)
        for t, i in zip(raw_data.times, raw_data.type_indices)]
    data.posix_string = raw_data.posix_string
    return data
