from collections import namedtuple
from datetime import date, timedelta, timezone

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
    pass

Rule = namedtuple('Rule', 'begin end type in_month on at save letters')
Observance = namedtuple('Observance', 'gmtoff rules format until')


class Zone:
    pass
