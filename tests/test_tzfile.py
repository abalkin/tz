import pytest

from tz import tzfile


def test_invalid_zoneinfo(tmpdir):
    empty = tmpdir.ensure('empty')
    with pytest.raises(ValueError):
        with empty.open() as f:
            tzfile.read(f)
