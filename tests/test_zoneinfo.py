import unittest
import sys

from datetime import timedelta, timezone, datetime, time
from array import array
import pickle
import pytest

from tz.zoneinfo import ZoneInfo, enfold, parse_std_dst, parse_mnd_time


def test_enfold():
    d0 = datetime(1, 1, 1)
    d1 = enfold(d0, fold=1)
    assert d1.fold == 1
    d2 = enfold(d1, fold=0)
    assert getattr(d2, 'fold', 0) == 0


class ZoneInfoTest(unittest.TestCase):
    zonename = 'America/New_York'
    version = None

    def setUp(self):
        if sys.platform == "win32":
            self.skipTest("Skipping zoneinfo tests on Windows")
        self.tz = ZoneInfo.fromname(self.zonename, self.version)

    def assertEquivDatetimes(self, a, b):
        self.assertEqual((a.replace(tzinfo=None), getattr(a, 'fold', 0),
                          id(a.tzinfo)),
                         (b.replace(tzinfo=None), getattr(b, 'fold', 0),
                          id(b.tzinfo)))

    def test_folds(self):
        tz = self.tz
        for dt, shift in tz.folds():
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
        for dt, shift in tz.gaps():
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
        transitions = list(tz.transitions())
        folds = list(tz.folds())
        gaps = list(tz.gaps())
        zeros = list(self.tz.zeros())
        self.assertEqual(len(transitions), len(folds) + len(gaps) + len(zeros))

    def test_zonenames(self):
        names = list(self.tz.zonenames())
        self.assertGreater(len(names), 0)

    def test_fromutc_errors(self):
        tz = self.tz
        with self.assertRaises(TypeError):
            tz.fromutc(None)
        with self.assertRaises(ValueError):
            dt = datetime(1, 1, 1)
            tz.fromutc(dt)


class ZoneInfoV0Test(ZoneInfoTest):
    version = 0


def test_invalid_zoneinfo(tmpdir):
    empty = tmpdir.ensure('empty')
    with pytest.raises(ValueError):
        with empty.open() as f:
            ZoneInfo.fromfile(f)


def test_zoneinfo_stats(capsys):
    ZoneInfo.stats()
    out, err = capsys.readouterr()
    assert out
    assert not err


def test_zoneinfo_nondst_folds(capsys):
    ZoneInfo.print_all_nondst_folds()
    out, err = capsys.readouterr()
    assert out
    assert not err


def test_pickle():
    ut = array('q', [1 - 2**63])
    ti = [(timedelta(0), False, 'UTC'), ]
    z = ZoneInfo(ut, ti)
    s = pickle.dumps(z)
    r = pickle.loads(s)
    assert z.ut == r.ut


@pytest.mark.parametrize('std_dst, parsed', [
    ('EST5EDT', (5, ('EST', 'EDT'))),
    ('CET-1CEST', (-1, ('CET', 'CEST'))),
    ('MSK-3', (-3, ('MSK', ''))),
])
def test_parse_std_dst(std_dst, parsed):
    assert parsed == parse_std_dst(std_dst)


@pytest.mark.parametrize('mnd_time, parsed', [
    ('M10.5.0', ((10, 5, 0), time(2))),
    ('M10.5.0/3', ((10, 5, 0), time(3))),
])
def test_parse_mnd_time(mnd_time, parsed):
    assert parsed == parse_mnd_time(mnd_time)
