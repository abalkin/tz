import unittest
import sys

from datetime import timedelta, timezone

from tz import ZoneInfo, enfold

class ZoneInfoTest(unittest.TestCase):
    zonename = 'America/New_York'

    def setUp(self):
        if sys.platform == "win32":
            self.skipTest("Skipping zoneinfo tests on Windows")
        self.tz = ZoneInfo.fromname(self.zonename)

    def assertEquivDatetimes(self, a, b):
        self.assertEqual((a.replace(tzinfo=None), getattr(a, 'fold', 0), id(a.tzinfo)),
                         (b.replace(tzinfo=None), getattr(b, 'fold', 0), id(b.tzinfo)))

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
                self.assertEqual(ldt.replace(tzinfo=None), udt.replace(tzinfo=None) + utcoffset)
                # Create a local time inside the gap
                ldt = tz.fromutc(dt.replace(tzinfo=tz)) - shift + x
                self.assertLess(enfold(ldt, 1).utcoffset(),
                                enfold(ldt, 0).utcoffset(),
                                "At %s." % ldt)

            for x in [-timedelta.resolution, shift]:
                udt = dt + x
                ldt = tz.fromutc(udt.replace(tzinfo=tz))
                self.assertEqual(getattr(ldt, 'fold', 0), 0)
