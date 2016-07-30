import pytest
from tzdata.classes import (
    Mon,
    Jul,
    last, next_month,
)
from datetime import date


@pytest.mark.parametrize('f,year,month,day', [
    ('Mon>=1', 2016, 7, 4),
])
def test_dow(f, year, month, day):
    d = date(year, month, day)
    f = eval(f)
    assert d.weekday() == Mon
    assert f(year, month) == d


@pytest.mark.parametrize('x,y', [
    ((2000, 10), (2000, 11)),
    ((2000, 12), (2001, 1)),
])
def test_next_month(x, y):
    year, month = x
    assert next_month(year, month) == y


@pytest.mark.parametrize('dow,year,month,day', [
    (Mon, 2016, Jul, 25),
])
def test_last(dow, year, month, day):
    f = last(dow)
    d = date(year, month, day)
    assert d == f(year, month)
