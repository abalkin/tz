import bisect
from array import array
from calendar import isleap
from datetime import tzinfo as _tzinfo, timedelta, date, datetime

from .tools import enfold

__all__ = ['ZoneInfo']

ZERO = timedelta(0)
HOUR = timedelta(hours=1)
SEC = timedelta(0, 1)
EPOCH = datetime(1970, 1, 1)


class tzinfo(_tzinfo):
    cache = {}

    def __new__(cls, tz=None, *args):
        if not isinstance(tz, str):
            return _tzinfo.__new__(cls)
        try:
            return cls.cache[tz]
        except KeyError:
            pass
        try:
            return PosixRules(tz)
        except ValueError:
            return cls.m_get(tz)

    @classmethod
    def m_get(cls, tz):
        raise NotImplemented


class ZoneInfo(tzinfo):
    posix_rules = None
    posix_after = datetime.max
    tzid = None     # The canonical zone name, e.g. 'America/New_York'
    tzrepr = None   # If set, returned by __repr__.

    def __init__(self, ut=array('q'), ti=()):
        """

        :param ut: array
            Array of transition point timestamps
        :param ti: list
            A list of (offset, isdst, abbr) tuples
        :return: None
        """
        if self.tzid is not None:
            # XXX: self is already initialized by the superclass
            # __new__.  Revisit this logic considering only using
            # __new__ in all classes.
            return
        super(ZoneInfo, self).__init__()
        self.ut = ut
        self.ti = ti
        if ut:
            self.lt = self.invert(ut, ti)
        else:
            self.posix_after = datetime.min

    @classmethod
    def make_reduce(cls, get):
        def __reduce__(self):
            tzrepr = self.tzrepr
            if tzrepr is None:
                return tzinfo.__reduce__(self)
            return get, (tzrepr, )
        return __reduce__

    def __repr__(self):
        tzrepr = self.tzrepr
        if tzrepr is not None:
            return 'tz.' + tzrepr
        tzid = self.tzid
        cls = type(self)
        if tzid is not None:
            return "%s.%s(%r)" % (cls.__module__, cls.__name__, tzid)
        return "<%s.%s object at 0x%x: %d times>" % (
            cls.__module__, cls.__name__, id(self), len(self.ut))

    @staticmethod
    def invert(ut, ti):
        lt = (ut[:], ut[:])
        if ut:
            offset = ti[0][0]
            lt[0][0] = max(datetime.min, lt[0][0] + offset)
            lt[1][0] = max(datetime.min, lt[1][0] + offset)
            for i in range(1, len(ut)):
                lt[0][i] += ti[i - 1][0]
                lt[1][i] += ti[i][0]
        return lt

    @classmethod
    def fromdata(cls, types, times, rules=None):
        ti = []
        ut = []
        for t, i in times:
            ut.append(t)
            ti.append(types[i])
        self = cls(ut, ti)
        if rules is not None:
            self.posix_rules = PosixRules(rules)
            self.posix_after = ut[-1]
        return self

    EPOCHORDINAL = date(1970, 1, 1).toordinal()

    def fromutc(self, dt):
        """datetime in UTC -> datetime in local time."""

        if not isinstance(dt, datetime):
            raise TypeError("fromutc() requires a datetime argument")
        if dt.tzinfo is not self:
            raise ValueError("dt.tzinfo is not self")
        dt = dt.replace(tzinfo=None)
        if dt > self.posix_after:
            return self.posix_rules.fromutc(dt)
        if dt < self.ut[1]:
            tti = self.ti[0]
            fold = 0
        else:
            idx = bisect.bisect_right(self.ut, dt)
            assert self.ut[idx - 1] <= dt
            assert idx == len(self.ut) or dt < self.ut[idx]
            tti_prev, tti = self.ti[idx - 2:idx]
            # Detect fold
            shift = tti_prev[0] - tti[0]
            fold = (shift > dt - self.ut[idx - 1])
        dt += tti[0]
        dt = dt.replace(tzinfo=self)
        if fold:
            return enfold(dt)
        else:
            return dt

    def _find_ti(self, dt, i):
        lt = self.lt[getattr(dt, 'fold', 0)]
        idx = bisect.bisect_right(lt, dt.replace(tzinfo=None))

        return self.ti[max(0, idx - 1)][i]

    def utcoffset(self, dt):
        if dt.replace(tzinfo=None) > self.posix_after:
            return self.posix_rules.utcoffset(dt)
        return self._find_ti(dt, 0)

    def dst(self, dt):
        if dt.replace(tzinfo=None) > self.posix_after:
            return self.posix_rules.dst(dt)
        return self._find_ti(dt, 1)

    def tzname(self, dt):
        return self._find_ti(dt, 2)


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
        raise ValueError("Expected a string starting with 'M' or 'J'",
                         mnd_time)
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

    def __reduce__(self):
        return PosixRules, (self.tzstr, )

    def __repr__(self):
        return 'tz.zoneinfo.PosixRules(%r)' % self.tzstr

    def __new__(cls, posix_rules):
        self = _tzinfo.__new__(cls)
        self.tzstr = posix_rules
        r = posix_rules.strip().split(',')
        self.offset, self.abbrs = parse_std_dst(r[0])
        if len(r) > 2:
            self.dst_start = parse_mnd_time(r[1])
            self.dst_end = parse_mnd_time(r[2])
        return self

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
