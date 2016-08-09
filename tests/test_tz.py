from datetime import datetime, timedelta, tzinfo

import pytest

import tz
from tz.zoneinfo import ZoneInfo


def test_basic_usage():
    z = tz.America.New_York
    t = datetime.fromtimestamp(0, z)
    assert t.tzname() == 'EST'
    t += timedelta(180)
    assert t.tzname() == 'EDT'


def test_complete():
    locations = []
    with open(ZoneInfo.zonetab_path()) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            name = line.split()[2]
            locations.append(name)
    for loc in locations:
        info = eval('tz.' + loc.replace('/', '.').replace('-', ''))
        assert isinstance(info, tzinfo)


@pytest.mark.parametrize('z', [
    'tz.America.Argentina.Buenos_Aires',
    "tz.Area('America/Argentina')",
])
def test_tz_repr(z):
    assert repr(eval(z)) == z
