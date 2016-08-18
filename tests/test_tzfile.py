import pytest

from tz import tzfile


def test_invalid_zoneinfo(tmpdir):
    empty = tmpdir.ensure('empty')
    with pytest.raises(ValueError):
        with empty.open() as f:
            tzfile.read(f)


def test_tzfile_read_ny2(ny_tzfile):
    ny = tzfile.read(ny_tzfile)
    assert ny.version == 2
    assert ny.times[0] == -2**59
    assert ny.posix_string == 'EST5EDT,M3.2.0,M11.1.0'


def test_tzfile_read_ny0(ny_tzfile):
    ny = tzfile.read(ny_tzfile, version=0)
    assert ny.version == 0
    assert ny.times[0] == -2**31
    assert ny.posix_string is None
