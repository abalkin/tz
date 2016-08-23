from zic.classes import *
from datetime import *


class Troll(Rules):
    name ="Troll"
    rules = [
        Rule(2005, 10000, None, Mar, lastSun,
             at=(timedelta(hours=1, minutes=0), 'utc'),
             save=timedelta(hours=2, minutes=0), letters='CEST'),
        Rule(2004, 10000, None, Oct, lastSun,
             at=(timedelta(hours=1, minutes=0), 'utc'),
             save=timedelta(hours=0, minutes=0), letters='UTC'),
    ]

class Antarctica:
    class Casey(Zone):
        name = 'Casey'
        observances = [
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=1969),
            Observance(gmtoff=8,
                       rules=None,
                       format='AWST',
                       until=(2009, Oct, 18, 2, 0, wall)),
            Observance(gmtoff=11,
                       rules=None,
                       format='CAST',
                       until=(2010, Mar, 5, 2, 0, wall)),
            Observance(gmtoff=8,
                       rules=None,
                       format='AWST',
                       until=(2011, Oct, 28, 2, 0, wall)),
            Observance(gmtoff=11,
                       rules=None,
                       format='CAST',
                       until=(2012, Feb, 21, 17, 0, utc)),
            Observance(gmtoff=8,
                       rules=None,
                       format='AWST',
                       until=None),
        ]

    class Davis(Zone):
        name = 'Davis'
        observances = [
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=(1957, Jan, 13)),
            Observance(gmtoff=7,
                       rules=None,
                       format='DAVT',
                       until=(1964, Nov)),
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=(1969, Feb)),
            Observance(gmtoff=7,
                       rules=None,
                       format='DAVT',
                       until=(2009, Oct, 18, 2, 0, wall)),
            Observance(gmtoff=5,
                       rules=None,
                       format='DAVT',
                       until=(2010, Mar, 10, 20, 0, utc)),
            Observance(gmtoff=7,
                       rules=None,
                       format='DAVT',
                       until=(2011, Oct, 28, 2, 0, wall)),
            Observance(gmtoff=5,
                       rules=None,
                       format='DAVT',
                       until=(2012, Feb, 21, 20, 0, utc)),
            Observance(gmtoff=7,
                       rules=None,
                       format='DAVT',
                       until=None),
        ]

    class DumontDUrville(Zone):
        name = 'DumontDUrville'
        observances = [
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=1947),
            Observance(gmtoff=10,
                       rules=None,
                       format='PMT',
                       until=(1952, Jan, 14)),
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=(1956, Nov)),
            Observance(gmtoff=10,
                       rules=None,
                       format='DDUT',
                       until=None),
        ]

    class Mawson(Zone):
        name = 'Mawson'
        observances = [
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=(1954, Feb, 13)),
            Observance(gmtoff=6,
                       rules=None,
                       format='MAWT',
                       until=(2009, Oct, 18, 2, 0, wall)),
            Observance(gmtoff=5,
                       rules=None,
                       format='MAWT',
                       until=None),
        ]

    class Rothera(Zone):
        name = 'Rothera'
        observances = [
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=(1976, Dec, 1)),
            Observance(gmtoff=-3,
                       rules=None,
                       format='ROTT',
                       until=None),
        ]

    class Syowa(Zone):
        name = 'Syowa'
        observances = [
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=(1957, Jan, 29)),
            Observance(gmtoff=3,
                       rules=None,
                       format='SYOT',
                       until=None),
        ]

    class Troll(Zone):
        name = 'Troll'
        observances = [
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=(2005, Feb, 12)),
            Observance(gmtoff=0,
                       rules=Troll,
                       format='%s',
                       until=None),
        ]

    class Vostok(Zone):
        name = 'Vostok'
        observances = [
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=(1957, Dec, 16)),
            Observance(gmtoff=6,
                       rules=None,
                       format='VOST',
                       until=None),
        ]

class Indian:
    class Kerguelen(Zone):
        name = 'Kerguelen'
        observances = [
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=1950),
            Observance(gmtoff=5,
                       rules=None,
                       format='TFT',
                       until=None),
        ]

