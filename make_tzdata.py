import os

from tz import tzfile
from datetime import datetime, timedelta

EPOCH = datetime(1970, 1, 1)
SEC = timedelta(0, 1)
U1 = (datetime(1, 1, 1) - EPOCH) // SEC


def list_zones(zoneinfo_dir):
    path = os.path.join(zoneinfo_dir, 'zone.tab')
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                yield line.split('\t')[2]


def get_zone_data(zoneinfo_dir, tzid):
    path = os.path.join(zoneinfo_dir, tzid)
    with open(path, 'rb') as f:
        return tzfile.read(f)

TEMPLATE = """\
types = [
    {}
]
times = [
    {}
]
posix = {!r}
"""


def format_timestamp(x):
    t = EPOCH + max(U1, x) * SEC
    return repr(t).replace('datetime.datetime', '')


def format_zone_data(data):
    types = ',\n    '.join(repr(x).replace('datetime.timedelta', '')
                           for x in data.type_infos)
    times = ',\n    '.join("(%s, %d)" % (format_timestamp(x), i)
                           for x, i in zip(data.times, data.type_indices))
    return TEMPLATE.format(types, times, data.posix_string)


def make_tree(zoneinfo_dir, tzdata_dir):
    zones = []
    for zone in list_zones(zoneinfo_dir):
        target_path = os.path.join(tzdata_dir, zone)
        source_path = os.path.join(zoneinfo_dir, zone)
        target_dir = os.path.dirname(target_path)
        os.makedirs(target_dir, 0o777, True)
        with open(source_path, 'rb') as f:
            data = tzfile.read(f)
        with open(target_path, 'w') as f:
            f.write(format_zone_data(data))
        zones.append(zone + '\n')
    zones_path = os.path.join(tzdata_dir, 'zones')
    with open(zones_path, 'w') as f:
        f.writelines(zones)
    print("Wrote %d zones in %s." % (len(zones), tzdata_dir))


if __name__ == '__main__':
    zoneinfo_dir = 'tzdata-pkg/raw/etc/zoneinfo'
    tzdata_dir = 'tzdata-pkg/tzdata'
    make_tree(zoneinfo_dir, tzdata_dir)
