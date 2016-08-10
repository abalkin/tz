import os
import struct
import sys
from array import array
from collections import namedtuple


def is_tzfile(p):
    with open(p, 'rb') as o:
        magic = o.read(4)
    return magic == b'TZif'


def _read_counts(fileobj):
    counts = array('i')
    counts.fromfile(fileobj, 6)
    if sys.byteorder != 'big':
        counts.byteswap()
    return counts


TZFileData = namedtuple('TZFileData', [
    'version',
    'type_infos',
    'times',
    'type_indices',
    'posix_string',
])


def read(fileobj, version=None):
    """Read tz data from a binary file.

    @param fileobj:
    @param version:
    @return: TZFileData
    """
    magic = fileobj.read(5)
    if magic[:4] != b"TZif":
        raise ValueError("not a zoneinfo file")
    if version is None:
        version = int(magic[4:]) if magic[4] else 0
    fileobj.seek(20)
    # Read the counts:
    # [0] - The number of UT/local indicators stored in the file.
    # [1] - The number of standard/wall indicators stored in the file.
    # [2] - The number of leap seconds for which data entries are stored
    #       in the file.
    # [3] - The number of transition times for which data entries are
    #       stored in the file.
    # [4] - The number of local time types for which data entries are
    #       stored in the file (must not be zero).
    # [5] - The number of characters of time zone abbreviation strings
    #  stored in the file.

    (ttisgmtcnt, ttisstdcnt, leapcnt,
     timecnt, typecnt, charcnt) = _read_counts(fileobj)
    if version >= 2:
        # Skip to the counts in the second header.
        data_size = (5 * timecnt +
                     6 * typecnt +
                     charcnt +
                     8 * leapcnt +
                     ttisstdcnt +
                     ttisgmtcnt)
        fileobj.seek(data_size + 20, os.SEEK_CUR)
        # Re-read the counts.
        (ttisgmtcnt, ttisstdcnt, leapcnt,
         timecnt, typecnt, charcnt) = _read_counts(fileobj)
        ttfmt = 'q'
    else:
        ttfmt = 'i'

    times = array(ttfmt)
    times.fromfile(fileobj, timecnt)
    if sys.byteorder != 'big':
        times.byteswap()

    type_indices = array('B')
    type_indices.fromfile(fileobj, timecnt)

    # Read local time types.
    type_infos = []
    for i in range(typecnt):
        type_infos.append(struct.unpack(">iBB", fileobj.read(6)))

    abbrs = fileobj.read(charcnt)

    if version > 0:
        # Skip to POSIX TZ string
        fileobj.seek(12 * leapcnt + ttisstdcnt + ttisgmtcnt, os.SEEK_CUR)
        posix_string = fileobj.read().strip().decode('ascii')
    else:
        posix_string = None

    # Convert type_infos
    for i, (gmtoff, isdst, abbrind) in enumerate(type_infos):
        abbr = abbrs[abbrind:abbrs.find(0, abbrind)].decode()
        type_infos[i] = (gmtoff, isdst, abbr)

    return TZFileData(version, type_infos, times, type_indices, posix_string)
