import os

from tz import tzfile
from datetime import datetime, timedelta

from tz.tools import pairs

EPOCH = datetime(1970, 1, 1)
SEC = timedelta(0, 1)
# The most negative value of a UTC timestamp:
# use January 2, 0001 to allow for up to 24 hours
# UTC offset.
U1 = (datetime(1, 1, 2) - EPOCH) // SEC


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


def format_offset(offset):
    if offset >= 0:
        sign = 1
    else:
        sign = -1
        offset = -offset
    hours, res = divmod(offset, 3600)
    if res == 0:
        offset = sign * hours
    else:
        offset = sign * hours,
        minutes, seconds = divmod(res, 60)
        offset += sign * minutes,
        if seconds:
            offset += sign * seconds,
    return offset


def format_type_info(offset, save, abbr):
    assert save > 1 or save == 0
    return "(%r, %r, %r)" % (
        format_offset(offset),
        format_offset(save), abbr)


def format_zone_data(zone, data):
    type_infos = guess_saves(zone, data)
    types = ',\n    '.join(format_type_info(*x) for x in type_infos)
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
            f.write(format_zone_data(zone, data))
        zones.append(zone + '\n')
    zones_path = os.path.join(tzdata_dir, 'zones')
    with open(zones_path, 'w') as f:
        f.writelines(zones)
    print("Wrote %d zones in %s." % (len(zones), tzdata_dir))


def T(x):
    return datetime.fromtimestamp(max(U1, x))


def guess_saves(zone, data):
    """Return type_infos with guessed DST saves"""
    saves = {}
    details = {}
    for (time0, type0), (time1, type1) in pairs(
            zip(data.times, data.type_indices)):
        i0 = data.type_infos[type0]
        i1 = data.type_infos[type1]
        is_dst0 = i0[1]
        is_dst1 = i1[1]
        if (is_dst0, is_dst1) == (False, True):
            shift = i1[0] - i0[0]
            if shift > 0:
                saves.setdefault(type1, set()).add(shift)
                details[type1, shift] = (T(time1),
                                         '%s->[%s]' % (i0[2], i1[2]))
        elif (is_dst0, is_dst1) == (True, False):
            shift = i0[0] - i1[0]
            if shift > 0:
                saves.setdefault(type0, set()).add(shift)
                details[type0, shift] = (T(time0),
                                         '[%s]->%s' % (i0[2], i1[2]))

    type_infos = data.type_infos[:]
    unused = set(range(len(type_infos))) - set(data.type_indices)
    for i, (offset, save, abbr) in enumerate(data.type_infos):
        if save and i not in unused:
            guesses = saves.get(i, set())
            if not guesses:
                print("No save value guesses for type %d (%r) in zone %s." %
                      (i, type_infos[i][-1], zone))
                guess = 3600
            elif len(guesses) == 1:
                guess = guesses.pop()
            else:
                print("Multiple save value guesses for type %d (%r)"
                      " in zone %s." % (i, type_infos[i][-1], zone))
                for g in guesses:
                    d = details[i, g]
                    print("   ", g, *d)
                guess = min(g for g in guesses if g)
        else:
            guess = save * 3600
        type_infos[i] = (offset, guess, abbr)
    return type_infos


if __name__ == '__main__':
    zoneinfo_dir = 'tzdata-pkg/raw/etc/zoneinfo'
    tzdata_dir = 'tzdata-pkg/tzdata'
    make_tree(zoneinfo_dir, tzdata_dir)
