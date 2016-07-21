"""PEP 495 compliant tzinfo implementation."""
import bisect
import itertools
import os
import struct
from array import array
from datetime import timedelta, tzinfo, date, datetime

import sys

from . import metadata

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright

ZERO = timedelta(0)
HOUR = timedelta(hours=1)
SEC = timedelta(0, 1)

def pairs(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

if hasattr(datetime, 'fold'):
    def enfold(dt, fold=1):
        return dt.replace(fold=fold)
else:
    class _DatetimeWithFold(datetime):
        @property
        def fold(self):
            return 1

    def enfold(dt, fold=1):
        if getattr(dt, 'fold', 0) == fold:
            return dt
        args = dt.timetuple()[:6]
        args += (dt.microsecond, dt.tzinfo)
        if fold:
            return _DatetimeWithFold(*args)
        else:
            return datetime(*args)

class ZoneInfo(tzinfo):
    zoneroot = '/usr/share/zoneinfo'

    def __init__(self, ut, ti, *args, **kwargs):
        """

        :param ut: array
            Array of transition point timestamps
        :param ti: list
            A list of (offset, isdst, abbr) tuples
        :return: None
        """
        super(ZoneInfo, self).__init__(*args, **kwargs)
        self.ut = ut
        self.ti = ti
        self.lt = self.invert(ut, ti)

    @staticmethod
    def invert(ut, ti):
        lt = (ut.__copy__(), ut.__copy__())
        if ut:
            offset = ti[0][0] // SEC
            lt[0][0] = max(-2 ** 31, lt[0][0] + offset)
            lt[1][0] = max(-2 ** 31, lt[1][0] + offset)
            for i in range(1, len(ut)):
                lt[0][i] += ti[i - 1][0] // SEC
                lt[1][i] += ti[i][0] // SEC
        return lt

    @classmethod
    def fromfile(cls, fileobj):
        if fileobj.read(4).decode() != "TZif":
            raise ValueError("not a zoneinfo file")
        fileobj.seek(32)
        counts = array('i')
        counts.fromfile(fileobj, 3)
        if sys.byteorder != 'big':
            counts.byteswap()

        ut = array('i')
        ut.fromfile(fileobj, counts[0])
        if sys.byteorder != 'big':
            ut.byteswap()

        type_indices = array('B')
        type_indices.fromfile(fileobj, counts[0])

        ttis = []
        for i in range(counts[1]):
            ttis.append(struct.unpack(">lbb", fileobj.read(6)))

        abbrs = fileobj.read(counts[2])

        # Convert ttis
        for i, (gmtoff, isdst, abbrind) in enumerate(ttis):
            abbr = abbrs[abbrind:abbrs.find(0, abbrind)].decode()
            ttis[i] = (timedelta(0, gmtoff), isdst, abbr)

        ti = [None] * len(ut)
        for i, idx in enumerate(type_indices):
            ti[i] = ttis[idx]

        self = cls(ut, ti)

        return self

    @classmethod
    def fromname(cls, name):
        path = os.path.join(cls.zoneroot, name)
        with open(path, 'rb') as f:
            return cls.fromfile(f)

    EPOCHORDINAL = date(1970, 1, 1).toordinal()

    def fromutc(self, dt):
        """datetime in UTC -> datetime in local time."""

        if not isinstance(dt, datetime):
            raise TypeError("fromutc() requires a datetime argument")
        if dt.tzinfo is not self:
            raise ValueError("dt.tzinfo is not self")

        timestamp = ((dt.toordinal() - self.EPOCHORDINAL) * 86400 +
                     dt.hour * 3600 + dt.minute * 60 + dt.second)

        if timestamp < self.ut[1]:
            tti = self.ti[0]
            fold = 0
        else:
            idx = bisect.bisect_right(self.ut, timestamp)
            assert self.ut[idx - 1] <= timestamp
            assert idx == len(self.ut) or timestamp < self.ut[idx]
            tti_prev, tti = self.ti[idx - 2:idx]
            # Detect fold
            shift = tti_prev[0] - tti[0]
            fold = (shift > timedelta(0, timestamp - self.ut[idx - 1]))
        dt += tti[0]
        if fold:
            return enfold(dt)
        else:
            return dt

    def _find_ti(self, dt, i):
        timestamp = ((dt.toordinal() - self.EPOCHORDINAL) * 86400 +
                     dt.hour * 3600 + dt.minute * 60 + dt.second)
        lt = self.lt[getattr(dt, 'fold', 0)]
        idx = bisect.bisect_right(lt, timestamp)

        return self.ti[max(0, idx - 1)][i]

    def utcoffset(self, dt):
        return self._find_ti(dt, 0)

    def dst(self, dt):
        isdst = self._find_ti(dt, 1)
        # XXX: We cannot accurately determine the "save" value,
        # so let's return 1h whenever DST is in effect.  Since
        # we don't use dst() in fromutc(), it is unlikely that
        # it will be needed for anything more than bool(dst()).
        return ZERO if isdst else HOUR

    def tzname(self, dt):
        return self._find_ti(dt, 2)

    @classmethod
    def zonenames(cls, zonedir=None):
        if zonedir is None:
            zonedir = cls.zoneroot
        for root, _, files in os.walk(zonedir):
            for f in files:
                p = os.path.join(root, f)
                with open(p, 'rb') as o:
                    magic = o.read(4)
                if magic == b'TZif':
                    yield p[len(zonedir) + 1:]

    @classmethod
    def stats(cls, start_year=1):
        count = gap_count = fold_count = zeros_count = 0
        min_gap = min_fold = timedelta.max
        max_gap = max_fold = ZERO
        min_gap_datetime = max_gap_datetime = datetime.min
        min_gap_zone = max_gap_zone = None
        min_fold_datetime = max_fold_datetime = datetime.min
        min_fold_zone = max_fold_zone = None
        stats_since = datetime(start_year, 1, 1)  # Starting from 1970 eliminates a lot of noise
        for zonename in cls.zonenames():
            count += 1
            tz = cls.fromname(zonename)
            for dt, shift in tz.transitions():
                if dt < stats_since:
                    continue
                if shift > ZERO:
                    gap_count += 1
                    if (shift, dt) > (max_gap, max_gap_datetime):
                        max_gap = shift
                        max_gap_zone = zonename
                        max_gap_datetime = dt
                    if (shift, datetime.max - dt) < (min_gap, datetime.max - min_gap_datetime):
                        min_gap = shift
                        min_gap_zone = zonename
                        min_gap_datetime = dt
                elif shift < ZERO:
                    fold_count += 1
                    shift = -shift
                    if (shift, dt) > (max_fold, max_fold_datetime):
                        max_fold = shift
                        max_fold_zone = zonename
                        max_fold_datetime = dt
                    if (shift, datetime.max - dt) < (min_fold, datetime.max - min_fold_datetime):
                        min_fold = shift
                        min_fold_zone = zonename
                        min_fold_datetime = dt
                else:
                    zeros_count += 1
        trans_counts = (gap_count, fold_count, zeros_count)
        print("Number of zones:       %5d" % count)
        print("Number of transitions: %5d = %d (gaps) + %d (folds) + %d (zeros)" %
              ((sum(trans_counts),) + trans_counts))
        print("Min gap:         %16s at %s in %s" % (min_gap, min_gap_datetime, min_gap_zone))
        print("Max gap:         %16s at %s in %s" % (max_gap, max_gap_datetime, max_gap_zone))
        print("Min fold:        %16s at %s in %s" % (min_fold, min_fold_datetime, min_fold_zone))
        print("Max fold:        %16s at %s in %s" % (max_fold, max_fold_datetime, max_fold_zone))

    def transitions(self):
        for (_, prev_ti), (t, ti) in pairs(zip(self.ut, self.ti)):
            shift = ti[0] - prev_ti[0]
            yield datetime.utcfromtimestamp(t), shift

    def nondst_folds(self):
        """Find all folds with the same value of isdst on both sides of the transition."""
        for (_, prev_ti), (t, ti) in pairs(zip(self.ut, self.ti)):
            shift = ti[0] - prev_ti[0]
            if shift < ZERO and ti[1] == prev_ti[1]:
                yield datetime.utcfromtimestamp(t), -shift, prev_ti[2], ti[2]

    @classmethod
    def print_all_nondst_folds(cls, same_abbr=False, start_year=1):
        count = 0
        for zonename in cls.zonenames():
            tz = cls.fromname(zonename)
            for dt, shift, prev_abbr, abbr in tz.nondst_folds():
                if dt.year < start_year or same_abbr and prev_abbr != abbr:
                    continue
                count += 1
                print("%3d) %-30s %s %10s %5s -> %s" %
                      (count, zonename, dt, shift, prev_abbr, abbr))

    def folds(self):
        for t, shift in self.transitions():
            if shift < ZERO:
                yield t, -shift

    def gaps(self):
        for t, shift in self.transitions():
            if shift > ZERO:
                yield t, shift

    def zeros(self):
        for t, shift in self.transitions():
            if not shift:
                yield t
