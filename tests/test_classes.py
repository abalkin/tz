import pytest
from tzdata.classes import (
    Mon,
    Jul,
    last, next_month,
    Rule, Mar, Sun, Nov, FixedOffset)
from datetime import date, timedelta, datetime


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


def test_us_dst_rule():
    rule = Rule(2007, 10000, None, Mar, Sun >= 8,
                at=(timedelta(hours=2, minutes=0), 'wall'),
                save=timedelta(hours=1, minutes=0), letters='D')
    assert rule.abbr('E%sT') == 'EDT'
    assert rule.abbr('EST/EDT') == 'EDT'
    assert rule.abbr('PDT') == 'PDT'
    assert rule.in_effect(2007)
    assert not rule.in_effect(2006)

    prev_tz = FixedOffset(utcoffset=-timedelta(hours=5),
                          dstoffset=timedelta(0), abbr='EST')
    trans = rule.transitions(prev_tz, "E%sT", 2016, 2017)
    assert list(trans) == [
        (datetime(2016, 3, 13, 2, 0, tzinfo=prev_tz),
         -timedelta(hours=4), timedelta(hours=1), 'EDT'),
    ]


def test_us_std_rule():
    rule = Rule(2007, 10000, None, Nov, Sun >= 1,
                (timedelta(hours=2, minutes=0), 'wall'), '0', 'S')
    assert rule
