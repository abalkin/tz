from calendar import isleap
from datetime import tzinfo as _tzinfo, timedelta, date, datetime
from .tools import pairs, enfold
import bisect
import os
import struct
import sys
from array import array

__all__ = ['ZoneInfo']

ZERO = timedelta(0)
HOUR = timedelta(hours=1)
SEC = timedelta(0, 1)


class tzinfo(_tzinfo):
    def __new__(cls, tz=None, *args):
        if not isinstance(tz, str):
            return _tzinfo.__new__(cls)
        try:
            return ZoneInfo.fromname(tz)
        except OSError:
            return PosixRules(tz)


class ZoneInfo(tzinfo):
    zoneroot = '/usr/share/zoneinfo'

    version = 0
    posix_rules = None
    area_lookup = None
    country_lookup = None

    def __init__(self, ut=array('q'), ti=()):
        """

        :param ut: array
            Array of transition point timestamps
        :param ti: list
            A list of (offset, isdst, abbr) tuples
        :return: None
        """
        super(ZoneInfo, self).__init__()
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
    def _read_counts(cls, fileobj):
        counts = array('i')
        counts.fromfile(fileobj, 6)
        if sys.byteorder != 'big':
            counts.byteswap()
        return counts

    @classmethod
    def fromfile(cls, fileobj, version=None):
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
         timecnt, typecnt, charcnt) = cls._read_counts(fileobj)
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
             timecnt, typecnt, charcnt) = cls._read_counts(fileobj)
            ttfmt = 'q'
        else:
            ttfmt = 'i'

        ut = array(ttfmt)
        ut.fromfile(fileobj, timecnt)
        if sys.byteorder != 'big':
            ut.byteswap()

        type_indices = array('B')
        type_indices.fromfile(fileobj, timecnt)

        # Read local time types.
        ttis = []
        for i in range(typecnt):
            ttis.append(struct.unpack(">iBB", fileobj.read(6)))

        abbrs = fileobj.read(charcnt)

        if version > 0:
            # Skip to POSIX TZ string
            fileobj.seek(12 * leapcnt + ttisstdcnt + ttisgmtcnt, os.SEEK_CUR)
            posix_rules = fileobj.read().strip()
        else:
            posix_rules = b''

        # Convert ttis
        for i, (gmtoff, isdst, abbrind) in enumerate(ttis):
            abbr = abbrs[abbrind:abbrs.find(0, abbrind)].decode()
            ttis[i] = (timedelta(0, gmtoff), isdst, abbr)

        ti = [None] * len(ut)
        for i, idx in enumerate(type_indices):
            ti[i] = ttis[idx]

        self = cls(ut, ti)
        self.version = version
        if posix_rules:
            self.posix_rules = PosixRules(posix_rules.decode('ascii'))

        return self

    @classmethod
    def fromname(cls, name, version=None):
        path = os.path.join(cls.zoneroot, name)
        with open(path, 'rb') as f:
            return cls.fromfile(f, version)

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
    def read_zone_file(cls):
        path = os.path.join(cls.zoneroot, 'zone.tab')
        try:
            f = open(path)
        except OSError:
            return
        cls.country_lookup = {}
        cls.area_lookup = {}
        with f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                country_code, coordinates, tz = line.split('\t', 4)[:3]
                cls.country_lookup.setdefault(country_code, []
                                              ).append((coordinates, tz))
                area, location = tz.rsplit('/', 1)
                cls.area_lookup.setdefault(area, set()).add(location)
                while '/' in area:
                    area, subarea = area.rsplit('/', 1)
                    cls.area_lookup.setdefault(area, set()).add(subarea + '/')

    @classmethod
    def list_area(cls, area):
        cls.read_zone_file()
        if cls.area_lookup is not None:
            for name in cls.area_lookup[area]:
                    yield name
            return
        # If 'zone.tab' file is not present - walk the tzinfo tree.
        path = os.path.join(cls.zoneroot, area)
        for name in os.listdir(path):
            p = os.path.join(path, name)
            if os.path.isdir(p):
                yield name + '/'
            elif is_tzfile(p):
                yield name

    @classmethod
    def zonenames(cls, zonedir=None):
        if zonedir is None:
            zonedir = cls.zoneroot
        elif not zonedir.startswith('/'):
            zonedir = os.path.join(cls.zoneroot, zonedir)
        for root, _, files in os.walk(zonedir):
            for f in files:
                p = os.path.join(root, f)
                if is_tzfile(p):
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
        # Starting from 1970 eliminates a lot of noise
        stats_since = datetime(start_year, 1, 1)
        errors = []
        for zonename in cls.zonenames():
            try:
                tz = cls.fromname(zonename)
            except ValueError as e:
                errors.append((zonename, e))
                continue
            count += 1
            for dt, shift in tz.transitions():
                if dt < stats_since:
                    continue
                if shift > ZERO:
                    gap_count += 1
                    if (shift, dt) > (max_gap, max_gap_datetime):
                        max_gap = shift
                        max_gap_zone = zonename
                        max_gap_datetime = dt
                    if (shift, datetime.max - dt) < (min_gap, datetime.max -
                                                     min_gap_datetime):
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
                    if (shift, datetime.max - dt) < (min_fold, datetime.max -
                                                     min_fold_datetime):
                        min_fold = shift
                        min_fold_zone = zonename
                        min_fold_datetime = dt
                else:
                    zeros_count += 1
        trans_counts = (gap_count, fold_count, zeros_count)
        print("Number of zones:       %5d" % count)
        print("Number of transitions: %5d ="
              " %d (gaps) + %d (folds) + %d (zeros)" %
              ((sum(trans_counts),) + trans_counts))
        print("Min gap:         %16s at %s in %s" %
              (min_gap, min_gap_datetime, min_gap_zone))
        print("Max gap:         %16s at %s in %s" %
              (max_gap, max_gap_datetime, max_gap_zone))
        print("Min fold:        %16s at %s in %s" %
              (min_fold, min_fold_datetime, min_fold_zone))
        print("Max fold:        %16s at %s in %s" %
              (max_fold, max_fold_datetime, max_fold_zone))
        for name, e in errors:
            print("ERROR in %s: %s" % (name, e))
        if errors:
            raise errors[0][1]

    def transitions(self):
        for (_, prev_ti), (t, ti) in pairs(zip(self.ut, self.ti)):
            shift = ti[0] - prev_ti[0]
            yield datetime.utcfromtimestamp(max(t, -62135596800)), shift

    def nondst_folds(self):
        """Find all folds with the same value of isdst
           on both sides of the transition."""
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

    @classmethod
    def zonetab_path(cls):
        path = os.path.join(cls.zoneroot, 'zone1970.tab')
        if os.path.exists(path):
            return path
        path = os.path.join(cls.zoneroot, 'zone.tab')
        if os.path.exists(path):
            return path
        raise SystemError('Missing zone.tab')


def parse_std_dst(std_dst):
    digit = False
    i = 0
    for j, ch in enumerate(std_dst):
        if digit:
            if not ch.isdigit():
                break
        else:
            if ch.isdigit():
                i = j
                digit = True
    else:
        j = len(std_dst)
    # At this point i points at the first digit and
    # j points at the first char of dst
    if std_dst[i - 1] in '+-':
        i -= 1
    std = std_dst[:i]
    offset = parse_time(std_dst[i:j])
    dst = std_dst[j:]
    return -offset, (std, dst)

TIME_COMPONENTS = ['hours', 'minutes', 'seconds']


def parse_time(time_str):
    neg = False
    if time_str.startswith(('+', '-')):
        neg = '-' == time_str[0]
        time_str = time_str[1:]
    parts = [int(p.lstrip('0') or '0') for p in time_str.split(':')]
    kwds = dict(zip(TIME_COMPONENTS, parts))
    if neg:
        return -timedelta(**kwds)
    else:
        return timedelta(**kwds)


def parse_mnd_time(mnd_time):
    if not mnd_time.startswith(('M', 'J')):
        raise ValueError("Expected a string starting with 'M' or 'J'", mnd_time)
    if '/' in mnd_time:
        mnd, t = mnd_time.split('/')
        t = parse_time(t)
    else:
        mnd = mnd_time
        t = timedelta(hours=2)
    args = tuple(int(part) for part in mnd[1:].split('.'))
    if mnd[0] == 'M':
        return lambda year: dth_day_of_week_n(year, *args) + t
    else:
        assert mnd[0] == 'J'
        return lambda year: julian_day(year, *args) + t


def julian_day(year, n):
    """Return the Julian day n(1 <= n <= 365).

    Leap days are not counted; that is, in all years -- including leap years --
    February 28 is day 59 and March 1 is day 60. It is impossible to explicitly
    refer to the occasional February 29.
    """
    if n > 59 and isleap(year):
        n += 1
    return datetime(year, 1, 1) + timedelta(n - 1)


class PosixRules(tzinfo):
    dst_start = None
    dst_end = None

    def __new__(cls, tz=None, *args):
        return tzinfo.__new__(cls, *args)

    def __init__(self, posix_rules=None):
        if posix_rules is None:
            return
        r = posix_rules.strip().split(',')
        self.offset, self.abbrs = parse_std_dst(r[0])
        if len(r) > 2:
            self.dst_start = parse_mnd_time(r[1])
            self.dst_end = parse_mnd_time(r[2])

    def tzname(self, dt):
        is_dst = bool(self.dst(dt))
        return self.abbrs[is_dst]

    def utcoffset(self, dt):
        return self.offset + self.dst(dt)

    def dst(self, dt):
        if self.dst_start is None:
            return ZERO
        start, end = self.transitions(dt.year)
        # Can't compare naive to aware objects, so strip the timezone from
        # dt first.
        dt = dt.replace(tzinfo=None)
        if start < end:  # Northern hemisphere
            if start + HOUR <= dt < end:
                # DST is in effect.
                return HOUR
            if end <= dt < end + HOUR:
                # Fold (an ambiguous hour): use dt.fold to disambiguate.
                return ZERO if getattr(dt, 'fold', 0) else HOUR
            if start <= dt < start + HOUR:
                # Gap (a non-existent hour): reverse the fold rule.
                return HOUR if getattr(dt, 'fold', 0) else ZERO
        else:  # Southern hemisphere (DST straddles the New Year)
            if start + HOUR <= dt or dt < end:
                # DST is in effect.
                return HOUR
            if end <= dt < end + HOUR:
                # Fold (an ambiguous hour): use dt.fold to disambiguate.
                return ZERO if getattr(dt, 'fold', 0) else HOUR
            if start <= dt < start + HOUR:
                # Gap (a non-existent hour): reverse the fold rule.
                return HOUR if getattr(dt, 'fold', 0) else ZERO
        # DST is off.
        return ZERO

    def transitions(self, year):
        start = self.dst_start(year)
        end = self.dst_end(year)
        return start, end


def next_month(year, month):
    month += 1
    return year + month // 12, month % 12


def dth_day_of_week_n(y, m, n, d):
    """Return he d'th day (0 <= d <= 6) of week n of month m of the  year.

    (1 <= n <= 5, 1 <= m <= 12,  where  week 5 means "the last d day in
    month m" which may  occur in  either  the  fourth  or  the  fifth week).
    Week 1 is  the  first  week  in which the d'th day occurs.  Day zero is
    Sunday.

    :param year:
    :param m: month
    :param n: week number
    :param d: day (0 <= d <= 6) of week
    :return: datetime
    """
    if n == 5:
        # Compute the last dow of the month.
        y, m = next_month(y, m)
        dt = datetime(y, m, 1) - timedelta(1)
        # Move back to the given dow.
        dt -= timedelta((dt.weekday() - d + 1) % 7)
    else:
        dt = datetime(y, m, 1)
        dt += timedelta((d - dt.weekday() - 1) % 7 + 7 * (n - 1))
    return dt


def is_tzfile(p):
    with open(p, 'rb') as o:
        magic = o.read(4)
    return magic == b'TZif'
