from datetime import timedelta, datetime

import pytest
from tz import system_tzdata


@pytest.fixture
def fake_system(zoneinfo, monkeypatch):
    monkeypatch.setattr(system_tzdata, 'zoneinfo_dir', zoneinfo.strpath)
    monkeypatch.setattr(system_tzdata, '_zones', [])
    monkeypatch.setattr(system_tzdata, '_aliases', {})
    return True


def test_system_tzdata_zones(fake_system):
    assert fake_system
    assert 'America/New_York' in list(system_tzdata.zones())


def test_system_tzdata_get(fake_system):
    assert fake_system
    z = system_tzdata.get('America/New_York')
    assert z.types == [
        (-timedelta(0, 17762), timedelta(0), 'LMT'),
        (-timedelta(0, 14400), timedelta(0, 3600), 'EDT'),
        (-timedelta(0, 18000), timedelta(0), 'EST'),
        (-timedelta(0, 14400), timedelta(0, 3600), 'EWT'),
        (-timedelta(0, 14400), timedelta(0, 3600), 'EPT'),
    ]
    assert z.times[:3] == [
        (datetime(1, 1, 1, 0, 0), 0),
        (datetime(1883, 11, 18, 17, 0), 2),
        (datetime(1918, 3, 31, 7, 0), 1),
    ]
    assert z.times[-3:] == [
        (datetime(2036, 11, 2, 6, 0), 2),
        (datetime(2037, 3, 8, 7, 0), 1),
        (datetime(2037, 11, 1, 6, 0), 2),
    ]
    assert z.rules == 'EST5EDT,M3.2.0,M11.1.0'

    z = system_tzdata.get('Australia/Lord_Howe')
    assert z.types == [
        (timedelta(0, 38180), timedelta(0), 'LMT'),
        (timedelta(0, 36000), timedelta(0), 'AEST'),
        (timedelta(0, 41400), timedelta(0, 3600), 'LHDT'),
        (timedelta(0, 37800), timedelta(0), 'LHST'),
        (timedelta(0, 39600), timedelta(0, 1800), 'LHDT'),
    ]
    assert z.times[:3] == [
        (datetime(1, 1, 1, 0, 0), 0),
        (datetime(1895, 1, 31, 13, 23, 40), 1),
        (datetime(1981, 2, 28, 14, 0), 3),
    ]
    assert z.times[-3:] == [
        (datetime(2036, 10, 4, 15, 30), 4),
        (datetime(2037, 4, 4, 15, 0), 3),
        (datetime(2037, 10, 3, 15, 30), 4),
    ]
    assert z.rules == 'LHST-10:30LHDT-11,M10.1.0,M4.1.0'
