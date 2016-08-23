from datetime import date, timedelta, timezone, datetime, tzinfo, time

UTC = timezone.utc


class DayOfWeek(int):
    def __new__(cls, num):
        return super().__new__(cls, num)

    def __ge__(self, other):
        def ge(year, month):
            d = date(year, month, other)
            days_to_go = (self - d.weekday()) % 7
            return d + timedelta(days_to_go)
        return ge


def next_month(year, month):
    month += 1
    return year + month // 12, month % 12


def last(dow):
    def f(year, month):
        y, m = next_month(year, month)
        last_day = date(y, m, 1) - timedelta(1)
        days_to_go = (last_day.weekday() - dow) % 7
        return last_day - timedelta(days_to_go)
    return f


Mon, Tue, Wed, Thu, Fri, Sat, Sun = [DayOfWeek(i) for i in range(7)]

lastMon = last(Mon)
lastTue = last(Tue)
lastWed = last(Wed)
lastThu = last(Thu)
lastFri = last(Fri)
lastSat = last(Sat)
lastSun = last(Sun)


(Jan, Feb, Mar, Apr, May, Jun,
 Jul, Aug, Sep, Oct, Nov, Dec) = range(1, 13)


class Rules:
    rules = []

    def in_effect(self, year):
        return [r for r in self.rules if r.in_effect(year)]


class FixedOffset(tzinfo):

    def __init__(self, utcoffset, dstoffset, abbr):
        self.__utcoffset = utcoffset
        self.__dstoffset = dstoffset
        self.__abbr = abbr
        self.__stdoffset = utcoffset - dstoffset

    def utcoffset(self, dt):
        return self.__utcoffset

    def tzname(self, dt):
        return self.__abbr

    def dst(self, dt):
        return self.__dstoffset

    def stdinfo(self):
        if not self.__dstoffset:
            return self
        return FixedOffset(self.__utcoffset,
                           timedelta(0),
                           self.__abbr)

    def stdoffset(self):
        return self.__stdoffset


class Rule:
    def __init__(self, begin, end, type, in_month,
                 on, at, save, letters):
        self.begin = begin
        self.end = end
        self.type = type
        self.in_month = in_month
        self.on = (lambda y, m: on) if isinstance(on, int) else on
        self.at = at
        self.save = save
        self.letters = letters

    def in_effect(self, year):
        return self.begin <= year < self.end

    def abbr(self, fmt):
        if '%' in fmt:
            return fmt % self.letters
        elif '/' in fmt:
            abbrs = fmt.split('/', 2)
            if self.save:
                return abbrs[1]
            else:
                return abbrs[0]
        else:
            return fmt

    def transitions(self, prev_tz, fmt, begin_year=None, end_year=None):
        begin_year = (self.begin if begin_year is None
                      else max(begin_year, self.begin))
        end_year = (self.end - 1 if end_year is None
                    else min(end_year, self.end - 1))

        for year in range(begin_year, end_year):
            month = self.in_month
            d = self.on(year, month)
            dt = datetime.combine(d, time())
            delta, time_type = self.at
            dt += delta
            if time_type == 'wall':
                info = prev_tz
            elif time_type == 'std':
                info = prev_tz.stdinfo()
            dstoff = self.save
            utcoff = prev_tz.stdoffset() + dstoff
            abbr = self.abbr(fmt)
            trans = (dt.replace(tzinfo=info), utcoff, dstoff, abbr)
            yield trans
            prev_tz = FixedOffset(*trans[1:])

TIME_ARGS = 'hours', 'minutes', 'seconds'


def wall(dt):
    return dt.astimezone(timezone.utc)

def utc(dt):
    return dt.replace(tzinfo=timezone.utc)

def std(dt):
    return dt.astimezone(timezone.utc) - dt.dst()

class Observance:
    def __init__(self, gmtoff, rules, format, until):
        if isinstance(gmtoff, int):
            gmtoff = [gmtoff]
        kwds = dict(zip(TIME_ARGS, gmtoff))
        self.gmtoff = timedelta(**kwds)
        self.rules = rules
        self.format = format
        self.until = until

class Zone:
    pass
