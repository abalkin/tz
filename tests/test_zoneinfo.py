import unittest
import sys

from datetime import timedelta, timezone, datetime
import pickle
import pytest

import tz
from tz.tools import pairs
from tz.zoneinfo import ZoneInfo, enfold, parse_std_dst, parse_mnd_time, \
    dth_day_of_week_n, PosixRules, HOUR, ZERO, parse_time, julian_day


def tz_shifts(z):
    for (_, prev_info), (time, info) in pairs(zip(z.ut, z.ti)):
        shift = info[0] - prev_info[0]
        yield time, shift


def tz_folds(z):
    for time, shift in tz_shifts(z):
        if shift < ZERO:
            yield time, -shift


def tz_gaps(z):
    for time, shift in tz_shifts(z):
        if shift > ZERO:
            yield time, shift


def tz_zeros(z):
    for time, shift in tz_shifts(z):
        if not shift:
            yield time


class ZoneInfoTest(unittest.TestCase):
    zonename = 'America/New_York'
    version = None

    def setUp(self):
        if sys.platform == "win32":
            self.skipTest("Skipping zoneinfo tests on Windows")
        data = tz.tzdata.get(self.zonename)
        self.tz = ZoneInfo.fromdata(data.types, data.times, data.rules)

    def assertEquivDatetimes(self, a, b):
        self.assertEqual((a.replace(tzinfo=None), getattr(a, 'fold', 0),
                          id(a.tzinfo)),
                         (b.replace(tzinfo=None), getattr(b, 'fold', 0),
                          id(b.tzinfo)))

    def test_folds(self):
        tz = self.tz
        for dt, shift in tz_folds(tz):
            for x in [0 * shift, 0.5 * shift, shift - timedelta.resolution]:
                udt = dt + x
                ldt = tz.fromutc(udt.replace(tzinfo=tz))
                self.assertEqual(getattr(ldt, 'fold', 0), 1)
                adt = udt.replace(tzinfo=timezone.utc).astimezone(tz)
                self.assertEquivDatetimes(adt, ldt)
                utcoffset = ldt.utcoffset()
                self.assertEqual(ldt.replace(tzinfo=None), udt + utcoffset)
                # Round trip
                self.assertEquivDatetimes(ldt.astimezone(timezone.utc),
                                          udt.replace(tzinfo=timezone.utc))

            for x in [-timedelta.resolution, shift]:
                udt = dt + x
                udt = udt.replace(tzinfo=tz)
                ldt = tz.fromutc(udt)
                self.assertEqual(getattr(ldt, 'fold', 0), 0)

    def test_gaps(self):
        tz = self.tz
        for dt, shift in tz_gaps(tz):
            for x in [0 * shift, 0.5 * shift, shift - timedelta.resolution]:
                udt = dt + x
                udt = udt.replace(tzinfo=tz)
                ldt = tz.fromutc(udt)
                self.assertEqual(getattr(ldt, 'fold', 0), 0)
                adt = udt.replace(tzinfo=timezone.utc).astimezone(tz)
                self.assertEquivDatetimes(adt, ldt)
                utcoffset = ldt.utcoffset()
                self.assertEqual(ldt.replace(tzinfo=None),
                                 udt.replace(tzinfo=None) + utcoffset)
                # Create a local time inside the gap
                ldt = tz.fromutc(dt.replace(tzinfo=tz)) - shift + x
                self.assertLess(enfold(ldt, 1).utcoffset(),
                                enfold(ldt, 0).utcoffset(),
                                "At %s." % ldt)

            for x in [-timedelta.resolution, shift]:
                udt = dt + x
                ldt = tz.fromutc(udt.replace(tzinfo=tz))
                self.assertEqual(getattr(ldt, 'fold', 0), 0)

    def test_zeros(self):
        tz = self.tz
        shifts = list(tz_shifts(tz))
        folds = list(tz_folds(tz))
        gaps = list(tz_gaps(tz))
        zeros = list(tz_zeros(tz))
        self.assertEqual(len(shifts), len(folds) + len(gaps) + len(zeros))

    def test_fromutc_errors(self):
        tz = self.tz
        with self.assertRaises(TypeError):
            tz.fromutc(None)
        with self.assertRaises(ValueError):
            dt = datetime(1, 1, 1)
            tz.fromutc(dt)


def test_pickle():
    ut = [datetime.min]
    ti = [(timedelta(0), timedelta(0), 'UTC'), ]
    z = ZoneInfo(ut, ti)
    s = pickle.dumps(z)
    r = pickle.loads(s)
    assert z.ut == r.ut


def test_posix_rules_pickle():
    z = PosixRules('EST+05EDT')
    s = pickle.dumps(z)
    r = pickle.loads(s)
    assert r.tzstr == z.tzstr


@pytest.mark.parametrize('std_dst, parsed', [
    ('EST5EDT', (timedelta(hours=-5), ('EST', 'EDT'))),
    ('CET-1CEST', (timedelta(hours=1), ('CET', 'CEST'))),
    ('MSK-3', (timedelta(hours=3), ('MSK', ''))),
])
def test_parse_std_dst(std_dst, parsed):
    assert parsed == parse_std_dst(std_dst)


@pytest.mark.parametrize('time_str, delta', [
    ('3', timedelta(hours=3)),
    ('3:45', timedelta(hours=3, minutes=45)),
    ('123:12:10', timedelta(hours=123, minutes=12, seconds=10)),
    ('-12:45', -timedelta(hours=12, minutes=45)),
])
def test_parse_time(time_str, delta):
    assert delta == parse_time(time_str)


@pytest.mark.parametrize('mnd_time, dt', [
    ('M10.5.0', (2016, 10, 30, 2)),
    ('M10.5.0/3', (2016, 10, 30, 3)),
    ('J59/0', (2016, 2, 28, 0)),
])
def test_parse_mnd_time(mnd_time, dt):
    dt = datetime(*dt)
    f = parse_mnd_time(mnd_time)
    assert dt == f(dt.year)


@pytest.mark.parametrize('y, m, n, d, day', [
    (2016, 8, 1, 0, 7),
    (2016, 8, 5, 0, 28),
])
def test_dth_day_of_week_n(y, m, n, d, day):
    dt = dth_day_of_week_n(y, m, n, d)
    assert dt.weekday() == (d - 1) % 7
    assert dt.timetuple()[:3] == (y, m, day)


@pytest.mark.parametrize('year, n, month, day', [
    (2015, 59, 2, 28),
    (2015, 60, 3, 1),
    (2016, 59, 2, 28),
    (2016, 60, 3, 1),
])
def test_julian_day(year, n, month, day):
    assert datetime(year, month, day) == julian_day(year, n)


@pytest.mark.parametrize('tz, year, dst_start, dst_end', [
    # New York
    ('EST5EDT,M3.2.0,M11.1.0', 2016,
     datetime(2016, 3, 13, 2), datetime(2016, 11, 6, 2)),
    # Sydney, Australia
    ('AEST-10AEDT,M10.1.0,M4.1.0/3', 2016,
     datetime(2016, 10, 2, 2), datetime(2016, 4, 3, 3)),
    # Exotic: Chatham, Pacific
    ('CHAST-12:45CHADT,M9.5.0/2:45,M4.1.0/3:45', 2016,
     datetime(2016, 9, 25, 2, 45), datetime(2016, 4, 3, 3, 45)),
    # Exotic: Tehran, Iran
    ('IRST-3:30IRDT,J80/0,J264/0', 2016,
     datetime(2016, 3, 21, 0), datetime(2016, 9, 21))
])
def test_posix_rules_transitions(tz, year, dst_start, dst_end):
    info = PosixRules(tz)
    assert (dst_start, dst_end) == info.transitions(year)
    dst_time = (dst_start + timedelta(1)).replace(tzinfo=info)
    assert dst_time.dst() == HOUR
    std_time = (dst_end + timedelta(1)).replace(tzinfo=info)
    assert std_time.dst() == ZERO
    # Ambiguous hour: the next hour after DST end.
    fold_time_0 = (dst_end + HOUR / 2).replace(tzinfo=info)
    fold_time_1 = enfold(fold_time_0, 1)
    assert fold_time_0.dst() == HOUR
    assert fold_time_1.dst() == ZERO
    # Skipped hour: the next hour after DST start
    gap_time_0 = (dst_start + HOUR / 2).replace(tzinfo=info)
    gap_time_1 = enfold(gap_time_0, 1)
    assert gap_time_0.dst() == ZERO
    assert gap_time_1.dst() == HOUR
    # Check that DST is an hour ahead of STD
    delta = dst_time.utcoffset() - std_time.utcoffset()
    assert delta == HOUR
    # Check that STD/DST abbreviations are correctly encoded in the TZ string
    std_dst = tz.split(',', 2)[0]
    std = std_time.tzname()
    dst = dst_time.tzname()
    assert std_dst.startswith(std)
    assert std_dst.endswith(dst)


def test_repr():
    z = ZoneInfo.fromdata([], [])
    z.tzid = 'America/New_York'
    assert repr(z) == "tz.zoneinfo.ZoneInfo('America/New_York')"


def test_far_future():
    z = ZoneInfo.fromdata([], [], 'EST5EDT,M3.2.0,M11.1.0')
    far_summer = datetime(9999, 6, 1, tzinfo=z)
    far_winter = datetime(9999, 12, 1, tzinfo=z)
    assert far_summer.dst()
    assert not far_winter.dst()
