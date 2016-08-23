from zic.classes import *
from datetime import *


class AW(Rules):
    name ="AW"
    rules = [
        Rule(1974, 1975, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1975, 1976, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1983, 1984, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1984, 1985, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1991, 1992, None, Nov, 17,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1992, 1993, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2006, 2007, None, Dec, 3,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(2007, 2010, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2007, 2009, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
    ]

class Vanuatu(Rules):
    name ="Vanuatu"
    rules = [
        Rule(1983, 1984, None, Sep, 25,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(1984, 1992, None, Mar, Sun>=23,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=0), letters=''),
        Rule(1984, 1985, None, Oct, 23,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(1985, 1992, None, Sep, Sun>=23,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(1992, 1994, None, Jan, Sun>=23,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=0), letters=''),
        Rule(1992, 1993, None, Oct, Sun>=23,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='S'),
    ]

class NC(Rules):
    name ="NC"
    rules = [
        Rule(1977, 1979, None, Dec, Sun>=1,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(1978, 1980, None, Feb, 27,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=0), letters=''),
        Rule(1996, 1997, None, Dec, 1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(1997, 1998, None, Mar, 2,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters=''),
    ]

class AS(Rules):
    name ="AS"
    rules = [
        Rule(1971, 1986, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1986, 1987, None, Oct, 19,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1987, 2008, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1972, 1973, None, Feb, 27,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1973, 1986, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1986, 1991, None, Mar, Sun>=15,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1991, 1992, None, Mar, 3,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1992, 1993, None, Mar, 22,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1993, 1994, None, Mar, 7,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1994, 1995, None, Mar, 20,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1995, 2006, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2006, 2007, None, Apr, 2,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2007, 2008, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2008, 10000, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2008, 10000, None, Oct, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
    ]

class Fiji(Rules):
    name ="Fiji"
    rules = [
        Rule(1998, 2000, None, Nov, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(1999, 2001, None, Feb, lastSun,
             at=(timedelta(hours=3, minutes=0), 'wall'),
             save=timedelta(hours=0), letters=''),
        Rule(2009, 2010, None, Nov, 29,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(2010, 2011, None, Mar, lastSun,
             at=(timedelta(hours=3, minutes=0), 'wall'),
             save=timedelta(hours=0), letters=''),
        Rule(2010, 2014, None, Oct, Sun>=21,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(2011, 2012, None, Mar, Sun>=1,
             at=(timedelta(hours=3, minutes=0), 'wall'),
             save=timedelta(hours=0), letters=''),
        Rule(2012, 2014, None, Jan, Sun>=18,
             at=(timedelta(hours=3, minutes=0), 'wall'),
             save=timedelta(hours=0), letters=''),
        Rule(2014, 2015, None, Jan, Sun>=18,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters=''),
        Rule(2014, 10000, None, Nov, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(2015, 10000, None, Jan, Sun>=15,
             at=(timedelta(hours=3, minutes=0), 'wall'),
             save=timedelta(hours=0), letters=''),
    ]

class Cook(Rules):
    name ="Cook"
    rules = [
        Rule(1978, 1979, None, Nov, 12,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=0, minutes=30), letters='HS'),
        Rule(1979, 1992, None, Mar, Sun>=1,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=0), letters=''),
        Rule(1979, 1991, None, Oct, lastSun,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=0, minutes=30), letters='HS'),
    ]

class Aus(Rules):
    name ="Aus"
    rules = [
        Rule(1917, 1918, None, Jan, 1,
             at=(timedelta(hours=0, minutes=1), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1917, 1918, None, Mar, 25,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(1942, 1943, None, Jan, 1,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1942, 1943, None, Mar, 29,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(1942, 1943, None, Sep, 27,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1943, 1945, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(1943, 1944, None, Oct, 3,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='D'),
    ]

class Tonga(Rules):
    name ="Tonga"
    rules = [
        Rule(1999, 2000, None, Oct, 7,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(2000, 2001, None, Mar, 19,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters=''),
        Rule(2000, 2002, None, Nov, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(2001, 2003, None, Jan, lastSun,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters=''),
    ]

class NZ(Rules):
    name ="NZ"
    rules = [
        Rule(1927, 1928, None, Nov, 6,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='S'),
        Rule(1928, 1929, None, Mar, 4,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='M'),
        Rule(1928, 1934, None, Oct, Sun>=8,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0, minutes=30), letters='S'),
        Rule(1929, 1934, None, Mar, Sun>=15,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='M'),
        Rule(1934, 1941, None, Apr, lastSun,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='M'),
        Rule(1934, 1941, None, Sep, lastSun,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0, minutes=30), letters='S'),
        Rule(1946, 1947, None, Jan, 1,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(1974, 1975, None, Nov, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1975, 1976, None, Feb, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1975, 1989, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1976, 1990, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1989, 1990, None, Oct, Sun>=8,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1990, 2007, None, Oct, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1990, 2008, None, Mar, Sun>=15,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2007, 10000, None, Sep, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(2008, 10000, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
    ]

class AQ(Rules):
    name ="AQ"
    rules = [
        Rule(1971, 1972, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1972, 1973, None, Feb, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1989, 1992, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1990, 1993, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
    ]

class WS(Rules):
    name ="WS"
    rules = [
        Rule(2010, 2011, None, Sep, lastSun,
             at=(timedelta(hours=0, minutes=0), 'wall'),
             save=timedelta(hours=1), letters='D'),
        Rule(2011, 2012, None, Apr, Sat>=1,
             at=(timedelta(hours=4, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(2011, 2012, None, Sep, lastSat,
             at=(timedelta(hours=3, minutes=0), 'wall'),
             save=timedelta(hours=1), letters='D'),
        Rule(2012, 10000, None, Apr, Sun>=1,
             at=(timedelta(hours=4, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(2012, 10000, None, Sep, lastSun,
             at=(timedelta(hours=3, minutes=0), 'wall'),
             save=timedelta(hours=1), letters='D'),
    ]

class AT(Rules):
    name ="AT"
    rules = [
        Rule(1967, 1968, None, Oct, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1968, 1969, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1968, 1986, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1969, 1972, None, Mar, Sun>=8,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1972, 1973, None, Feb, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1973, 1982, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1982, 1984, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1984, 1987, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1986, 1987, None, Oct, Sun>=15,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1987, 1991, None, Mar, Sun>=15,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1987, 1988, None, Oct, Sun>=22,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1988, 1991, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1991, 2000, None, Oct, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1991, 2006, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2000, 2001, None, Aug, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(2001, 10000, None, Oct, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(2006, 2007, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2007, 2008, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2008, 10000, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
    ]

class Holiday(Rules):
    name ="Holiday"
    rules = [
        Rule(1992, 1994, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1993, 1995, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
    ]

class AV(Rules):
    name ="AV"
    rules = [
        Rule(1971, 1986, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1972, 1973, None, Feb, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1973, 1986, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1986, 1991, None, Mar, Sun>=15,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1986, 1988, None, Oct, Sun>=15,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1988, 2000, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1991, 1995, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1995, 2006, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2000, 2001, None, Aug, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(2001, 2008, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(2006, 2007, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2007, 2008, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2008, 10000, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2008, 10000, None, Oct, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
    ]

class Chatham(Rules):
    name ="Chatham"
    rules = [
        Rule(1974, 1975, None, Nov, Sun>=1,
             at=(timedelta(hours=2, minutes=45), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1975, 1976, None, Feb, lastSun,
             at=(timedelta(hours=2, minutes=45), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1975, 1989, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=45), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1976, 1990, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=45), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1989, 1990, None, Oct, Sun>=8,
             at=(timedelta(hours=2, minutes=45), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1990, 2007, None, Oct, Sun>=1,
             at=(timedelta(hours=2, minutes=45), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1990, 2008, None, Mar, Sun>=15,
             at=(timedelta(hours=2, minutes=45), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2007, 10000, None, Sep, lastSun,
             at=(timedelta(hours=2, minutes=45), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(2008, 10000, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=45), 'std'),
             save=timedelta(hours=0), letters='S'),
    ]

class LH(Rules):
    name ="LH"
    rules = [
        Rule(1981, 1985, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1982, 1986, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(1985, 1986, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0, minutes=30), letters='D'),
        Rule(1986, 1990, None, Mar, Sun>=15,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(1986, 1987, None, Oct, 19,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0, minutes=30), letters='D'),
        Rule(1987, 2000, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0, minutes=30), letters='D'),
        Rule(1990, 1996, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(1996, 2006, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(2000, 2001, None, Aug, lastSun,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0, minutes=30), letters='D'),
        Rule(2001, 2008, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0, minutes=30), letters='D'),
        Rule(2006, 2007, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(2007, 2008, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(2008, 10000, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0), letters='S'),
        Rule(2008, 10000, None, Oct, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'wall'),
             save=timedelta(hours=0, minutes=30), letters='D'),
    ]

class AN(Rules):
    name ="AN"
    rules = [
        Rule(1971, 1986, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1972, 1973, None, Feb, 27,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1973, 1982, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1982, 1983, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1983, 1986, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1986, 1990, None, Mar, Sun>=15,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1986, 1987, None, Oct, 19,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1987, 2000, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(1990, 1996, None, Mar, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(1996, 2006, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2000, 2001, None, Aug, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(2001, 2008, None, Oct, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
        Rule(2006, 2007, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2007, 2008, None, Mar, lastSun,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2008, 10000, None, Apr, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=0), letters='S'),
        Rule(2008, 10000, None, Oct, Sun>=1,
             at=(timedelta(hours=2, minutes=0), 'std'),
             save=timedelta(hours=1, minutes=0), letters='D'),
    ]

class Antarctica:
    class Macquarie(Zone):
        name = 'Macquarie'
        observances = [
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=(1899, Nov)),
            Observance(gmtoff=10,
                       rules=None,
                       format='AEST',
                       until=(1916, Oct, 1, 2, 0, wall)),
            Observance(gmtoff=10,
                       rules='1:00',
                       format='AEDT',
                       until=(1917, Feb)),
            Observance(gmtoff=10,
                       rules=Aus,
                       format='AE%sT',
                       until=(1919, Apr, 1, 0, 0, std)),
            Observance(gmtoff=0,
                       rules=None,
                       format='-00',
                       until=(1948, Mar, 25)),
            Observance(gmtoff=10,
                       rules=Aus,
                       format='AE%sT',
                       until=1967),
            Observance(gmtoff=10,
                       rules=AT,
                       format='AE%sT',
                       until=(2010, Apr, 4, 3, 0, wall)),
            Observance(gmtoff=11,
                       rules=None,
                       format='MIST',
                       until=None),
        ]

class Australia:
    class Adelaide(Zone):
        name = 'Adelaide'
        observances = [
            Observance(gmtoff=(9, 14, 20),
                       rules=None,
                       format='LMT',
                       until=(1895, Feb)),
            Observance(gmtoff=9,
                       rules=None,
                       format='ACST',
                       until=(1899, May)),
            Observance(gmtoff=(9, 30),
                       rules=Aus,
                       format='AC%sT',
                       until=1971),
            Observance(gmtoff=(9, 30),
                       rules=AS,
                       format='AC%sT',
                       until=None),
        ]

    class Brisbane(Zone):
        name = 'Brisbane'
        observances = [
            Observance(gmtoff=(10, 12, 8),
                       rules=None,
                       format='LMT',
                       until=1895),
            Observance(gmtoff=10,
                       rules=Aus,
                       format='AE%sT',
                       until=1971),
            Observance(gmtoff=10,
                       rules=AQ,
                       format='AE%sT',
                       until=None),
        ]

    class Broken_Hill(Zone):
        name = 'Broken_Hill'
        observances = [
            Observance(gmtoff=(9, 25, 48),
                       rules=None,
                       format='LMT',
                       until=(1895, Feb)),
            Observance(gmtoff=10,
                       rules=None,
                       format='AEST',
                       until=(1896, Aug, 23)),
            Observance(gmtoff=9,
                       rules=None,
                       format='ACST',
                       until=(1899, May)),
            Observance(gmtoff=(9, 30),
                       rules=Aus,
                       format='AC%sT',
                       until=1971),
            Observance(gmtoff=(9, 30),
                       rules=AN,
                       format='AC%sT',
                       until=2000),
            Observance(gmtoff=(9, 30),
                       rules=AS,
                       format='AC%sT',
                       until=None),
        ]

    class Currie(Zone):
        name = 'Currie'
        observances = [
            Observance(gmtoff=(9, 35, 28),
                       rules=None,
                       format='LMT',
                       until=(1895, Sep)),
            Observance(gmtoff=10,
                       rules=None,
                       format='AEST',
                       until=(1916, Oct, 1, 2, 0, wall)),
            Observance(gmtoff=10,
                       rules='1:00',
                       format='AEDT',
                       until=(1917, Feb)),
            Observance(gmtoff=10,
                       rules=Aus,
                       format='AE%sT',
                       until=(1971, Jul)),
            Observance(gmtoff=10,
                       rules=AT,
                       format='AE%sT',
                       until=None),
        ]

    class Darwin(Zone):
        name = 'Darwin'
        observances = [
            Observance(gmtoff=(8, 43, 20),
                       rules=None,
                       format='LMT',
                       until=(1895, Feb)),
            Observance(gmtoff=9,
                       rules=None,
                       format='ACST',
                       until=(1899, May)),
            Observance(gmtoff=(9, 30),
                       rules=Aus,
                       format='AC%sT',
                       until=None),
        ]

    class Eucla(Zone):
        name = 'Eucla'
        observances = [
            Observance(gmtoff=(8, 35, 28),
                       rules=None,
                       format='LMT',
                       until=(1895, Dec)),
            Observance(gmtoff=(8, 45),
                       rules=Aus,
                       format='ACW%sT',
                       until=(1943, Jul)),
            Observance(gmtoff=(8, 45),
                       rules=AW,
                       format='ACW%sT',
                       until=None),
        ]

    class Hobart(Zone):
        name = 'Hobart'
        observances = [
            Observance(gmtoff=(9, 49, 16),
                       rules=None,
                       format='LMT',
                       until=(1895, Sep)),
            Observance(gmtoff=10,
                       rules=None,
                       format='AEST',
                       until=(1916, Oct, 1, 2, 0, wall)),
            Observance(gmtoff=10,
                       rules='1:00',
                       format='AEDT',
                       until=(1917, Feb)),
            Observance(gmtoff=10,
                       rules=Aus,
                       format='AE%sT',
                       until=1967),
            Observance(gmtoff=10,
                       rules=AT,
                       format='AE%sT',
                       until=None),
        ]

    class Lindeman(Zone):
        name = 'Lindeman'
        observances = [
            Observance(gmtoff=(9, 55, 56),
                       rules=None,
                       format='LMT',
                       until=1895),
            Observance(gmtoff=10,
                       rules=Aus,
                       format='AE%sT',
                       until=1971),
            Observance(gmtoff=10,
                       rules=AQ,
                       format='AE%sT',
                       until=(1992, Jul)),
            Observance(gmtoff=10,
                       rules=Holiday,
                       format='AE%sT',
                       until=None),
        ]

    class Lord_Howe(Zone):
        name = 'Lord_Howe'
        observances = [
            Observance(gmtoff=(10, 36, 20),
                       rules=None,
                       format='LMT',
                       until=(1895, Feb)),
            Observance(gmtoff=10,
                       rules=None,
                       format='AEST',
                       until=(1981, Mar)),
            Observance(gmtoff=(10, 30),
                       rules=LH,
                       format='LH%sT',
                       until=None),
        ]

    class Melbourne(Zone):
        name = 'Melbourne'
        observances = [
            Observance(gmtoff=(9, 39, 52),
                       rules=None,
                       format='LMT',
                       until=(1895, Feb)),
            Observance(gmtoff=10,
                       rules=Aus,
                       format='AE%sT',
                       until=1971),
            Observance(gmtoff=10,
                       rules=AV,
                       format='AE%sT',
                       until=None),
        ]

    class Perth(Zone):
        name = 'Perth'
        observances = [
            Observance(gmtoff=(7, 43, 24),
                       rules=None,
                       format='LMT',
                       until=(1895, Dec)),
            Observance(gmtoff=8,
                       rules=Aus,
                       format='AW%sT',
                       until=(1943, Jul)),
            Observance(gmtoff=8,
                       rules=AW,
                       format='AW%sT',
                       until=None),
        ]

    class Sydney(Zone):
        name = 'Sydney'
        observances = [
            Observance(gmtoff=(10, 4, 52),
                       rules=None,
                       format='LMT',
                       until=(1895, Feb)),
            Observance(gmtoff=10,
                       rules=Aus,
                       format='AE%sT',
                       until=1971),
            Observance(gmtoff=10,
                       rules=AN,
                       format='AE%sT',
                       until=None),
        ]

class Indian:
    class Christmas(Zone):
        name = 'Christmas'
        observances = [
            Observance(gmtoff=(7, 2, 52),
                       rules=None,
                       format='LMT',
                       until=(1895, Feb)),
            Observance(gmtoff=7,
                       rules=None,
                       format='CXT',
                       until=None),
        ]

    class Cocos(Zone):
        name = 'Cocos'
        observances = [
            Observance(gmtoff=(6, 27, 40),
                       rules=None,
                       format='LMT',
                       until=1900),
            Observance(gmtoff=(6, 30),
                       rules=None,
                       format='CCT',
                       until=None),
        ]

class Pacific:
    class Apia(Zone):
        name = 'Apia'
        observances = [
            Observance(gmtoff=(12, 33, 4),
                       rules=None,
                       format='LMT',
                       until=(1879, Jul, 5)),
            Observance(gmtoff=(-11, -26, -56),
                       rules=None,
                       format='LMT',
                       until=1911),
            Observance(gmtoff=(-11, -30),
                       rules=None,
                       format='WSST',
                       until=1950),
            Observance(gmtoff=-11,
                       rules=WS,
                       format='S%sT',
                       until=(2011, Dec, 29, 24, 0, wall)),
            Observance(gmtoff=13,
                       rules=WS,
                       format='WS%sT',
                       until=None),
        ]

    class Auckland(Zone):
        name = 'Auckland'
        observances = [
            Observance(gmtoff=(11, 39, 4),
                       rules=None,
                       format='LMT',
                       until=(1868, Nov, 2)),
            Observance(gmtoff=(11, 30),
                       rules=NZ,
                       format='NZ%sT',
                       until=(1946, Jan, 1)),
            Observance(gmtoff=12,
                       rules=NZ,
                       format='NZ%sT',
                       until=None),
        ]

    class Bougainville(Zone):
        name = 'Bougainville'
        observances = [
            Observance(gmtoff=(10, 22, 16),
                       rules=None,
                       format='LMT',
                       until=1880),
            Observance(gmtoff=(9, 48, 32),
                       rules=None,
                       format='PMMT',
                       until=1895),
            Observance(gmtoff=10,
                       rules=None,
                       format='PGT',
                       until=(1942, Jul)),
            Observance(gmtoff=9,
                       rules=None,
                       format='JST',
                       until=(1945, Aug, 21)),
            Observance(gmtoff=10,
                       rules=None,
                       format='PGT',
                       until=(2014, Dec, 28, 2, 0, wall)),
            Observance(gmtoff=11,
                       rules=None,
                       format='BST',
                       until=None),
        ]

    class Chatham(Zone):
        name = 'Chatham'
        observances = [
            Observance(gmtoff=(12, 13, 48),
                       rules=None,
                       format='LMT',
                       until=(1868, Nov, 2)),
            Observance(gmtoff=(12, 15),
                       rules=None,
                       format='CHAST',
                       until=(1946, Jan, 1)),
            Observance(gmtoff=(12, 45),
                       rules=Chatham,
                       format='CHA%sT',
                       until=None),
        ]

    class Chuuk(Zone):
        name = 'Chuuk'
        observances = [
            Observance(gmtoff=(10, 7, 8),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=10,
                       rules=None,
                       format='CHUT',
                       until=None),
        ]

    class Efate(Zone):
        name = 'Efate'
        observances = [
            Observance(gmtoff=(11, 13, 16),
                       rules=None,
                       format='LMT',
                       until=(1912, Jan, 13)),
            Observance(gmtoff=11,
                       rules=Vanuatu,
                       format='VU%sT',
                       until=None),
        ]

    class Enderbury(Zone):
        name = 'Enderbury'
        observances = [
            Observance(gmtoff=(-11, -24, -20),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=-12,
                       rules=None,
                       format='PHOT',
                       until=(1979, Oct)),
            Observance(gmtoff=-11,
                       rules=None,
                       format='PHOT',
                       until=1995),
            Observance(gmtoff=13,
                       rules=None,
                       format='PHOT',
                       until=None),
        ]

    class Fakaofo(Zone):
        name = 'Fakaofo'
        observances = [
            Observance(gmtoff=(-11, -24, -56),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=-11,
                       rules=None,
                       format='TKT',
                       until=(2011, Dec, 30)),
            Observance(gmtoff=13,
                       rules=None,
                       format='TKT',
                       until=None),
        ]

    class Fiji(Zone):
        name = 'Fiji'
        observances = [
            Observance(gmtoff=(11, 55, 44),
                       rules=None,
                       format='LMT',
                       until=(1915, Oct, 26)),
            Observance(gmtoff=12,
                       rules=Fiji,
                       format='FJ%sT',
                       until=None),
        ]

    class Funafuti(Zone):
        name = 'Funafuti'
        observances = [
            Observance(gmtoff=(11, 56, 52),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=12,
                       rules=None,
                       format='TVT',
                       until=None),
        ]

    class Gambier(Zone):
        name = 'Gambier'
        observances = [
            Observance(gmtoff=(-8, -59, -48),
                       rules=None,
                       format='LMT',
                       until=(1912, Oct)),
            Observance(gmtoff=-9,
                       rules=None,
                       format='GAMT',
                       until=None),
        ]

    class Guadalcanal(Zone):
        name = 'Guadalcanal'
        observances = [
            Observance(gmtoff=(10, 39, 48),
                       rules=None,
                       format='LMT',
                       until=(1912, Oct)),
            Observance(gmtoff=11,
                       rules=None,
                       format='SBT',
                       until=None),
        ]

    class Guam(Zone):
        name = 'Guam'
        observances = [
            Observance(gmtoff=(-14, -21),
                       rules=None,
                       format='LMT',
                       until=(1844, Dec, 31)),
            Observance(gmtoff=(9, 39),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=10,
                       rules=None,
                       format='GST',
                       until=(2000, Dec, 23)),
            Observance(gmtoff=10,
                       rules=None,
                       format='ChST',
                       until=None),
        ]

    class Kiritimati(Zone):
        name = 'Kiritimati'
        observances = [
            Observance(gmtoff=(-10, -29, -20),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=(-10, -40),
                       rules=None,
                       format='LINT',
                       until=(1979, Oct)),
            Observance(gmtoff=-10,
                       rules=None,
                       format='LINT',
                       until=1995),
            Observance(gmtoff=14,
                       rules=None,
                       format='LINT',
                       until=None),
        ]

    class Kosrae(Zone):
        name = 'Kosrae'
        observances = [
            Observance(gmtoff=(10, 51, 56),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=11,
                       rules=None,
                       format='KOST',
                       until=(1969, Oct)),
            Observance(gmtoff=12,
                       rules=None,
                       format='KOST',
                       until=1999),
            Observance(gmtoff=11,
                       rules=None,
                       format='KOST',
                       until=None),
        ]

    class Kwajalein(Zone):
        name = 'Kwajalein'
        observances = [
            Observance(gmtoff=(11, 9, 20),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=11,
                       rules=None,
                       format='MHT',
                       until=(1969, Oct)),
            Observance(gmtoff=-12,
                       rules=None,
                       format='KWAT',
                       until=(1993, Aug, 20)),
            Observance(gmtoff=12,
                       rules=None,
                       format='MHT',
                       until=None),
        ]

    class Majuro(Zone):
        name = 'Majuro'
        observances = [
            Observance(gmtoff=(11, 24, 48),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=11,
                       rules=None,
                       format='MHT',
                       until=(1969, Oct)),
            Observance(gmtoff=12,
                       rules=None,
                       format='MHT',
                       until=None),
        ]

    class Marquesas(Zone):
        name = 'Marquesas'
        observances = [
            Observance(gmtoff=(-9, -18),
                       rules=None,
                       format='LMT',
                       until=(1912, Oct)),
            Observance(gmtoff=(-9, -30),
                       rules=None,
                       format='MART',
                       until=None),
        ]

    class Nauru(Zone):
        name = 'Nauru'
        observances = [
            Observance(gmtoff=(11, 7, 40),
                       rules=None,
                       format='LMT',
                       until=(1921, Jan, 15)),
            Observance(gmtoff=(11, 30),
                       rules=None,
                       format='NRT',
                       until=(1942, Mar, 15)),
            Observance(gmtoff=9,
                       rules=None,
                       format='JST',
                       until=(1944, Aug, 15)),
            Observance(gmtoff=(11, 30),
                       rules=None,
                       format='NRT',
                       until=(1979, May)),
            Observance(gmtoff=12,
                       rules=None,
                       format='NRT',
                       until=None),
        ]

    class Niue(Zone):
        name = 'Niue'
        observances = [
            Observance(gmtoff=(-11, -19, -40),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=(-11, -20),
                       rules=None,
                       format='NUT',
                       until=1951),
            Observance(gmtoff=(-11, -30),
                       rules=None,
                       format='NUT',
                       until=(1978, Oct, 1)),
            Observance(gmtoff=-11,
                       rules=None,
                       format='NUT',
                       until=None),
        ]

    class Norfolk(Zone):
        name = 'Norfolk'
        observances = [
            Observance(gmtoff=(11, 11, 52),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=(11, 12),
                       rules=None,
                       format='NMT',
                       until=1951),
            Observance(gmtoff=(11, 30),
                       rules=None,
                       format='NFT',
                       until=(1974, Oct, 27, 2, 0, wall)),
            Observance(gmtoff=(11, 30),
                       rules='1:00',
                       format='NFST',
                       until=(1975, Mar, 2, 2, 0, wall)),
            Observance(gmtoff=(11, 30),
                       rules=None,
                       format='NFT',
                       until=(2015, Oct, 4, 2, 0, wall)),
            Observance(gmtoff=11,
                       rules=None,
                       format='NFT',
                       until=None),
        ]

    class Noumea(Zone):
        name = 'Noumea'
        observances = [
            Observance(gmtoff=(11, 5, 48),
                       rules=None,
                       format='LMT',
                       until=(1912, Jan, 13)),
            Observance(gmtoff=11,
                       rules=NC,
                       format='NC%sT',
                       until=None),
        ]

    class Pago_Pago(Zone):
        name = 'Pago_Pago'
        observances = [
            Observance(gmtoff=(12, 37, 12),
                       rules=None,
                       format='LMT',
                       until=(1879, Jul, 5)),
            Observance(gmtoff=(-11, -22, -48),
                       rules=None,
                       format='LMT',
                       until=1911),
            Observance(gmtoff=-11,
                       rules=None,
                       format='NST',
                       until=(1967, Apr)),
            Observance(gmtoff=-11,
                       rules=None,
                       format='BST',
                       until=(1983, Nov, 30)),
            Observance(gmtoff=-11,
                       rules=None,
                       format='SST',
                       until=None),
        ]

    class Palau(Zone):
        name = 'Palau'
        observances = [
            Observance(gmtoff=(8, 57, 56),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=9,
                       rules=None,
                       format='PWT',
                       until=None),
        ]

    class Pitcairn(Zone):
        name = 'Pitcairn'
        observances = [
            Observance(gmtoff=(-8, -40, -20),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=(-8, -30),
                       rules=None,
                       format='PNT',
                       until=(1998, Apr, 27, 0, 0, wall)),
            Observance(gmtoff=-8,
                       rules=None,
                       format='PST',
                       until=None),
        ]

    class Pohnpei(Zone):
        name = 'Pohnpei'
        observances = [
            Observance(gmtoff=(10, 32, 52),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=11,
                       rules=None,
                       format='PONT',
                       until=None),
        ]

    class Port_Moresby(Zone):
        name = 'Port_Moresby'
        observances = [
            Observance(gmtoff=(9, 48, 40),
                       rules=None,
                       format='LMT',
                       until=1880),
            Observance(gmtoff=(9, 48, 32),
                       rules=None,
                       format='PMMT',
                       until=1895),
            Observance(gmtoff=10,
                       rules=None,
                       format='PGT',
                       until=None),
        ]

    class Rarotonga(Zone):
        name = 'Rarotonga'
        observances = [
            Observance(gmtoff=(-10, -39, -4),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=(-10, -30),
                       rules=None,
                       format='CKT',
                       until=(1978, Nov, 12)),
            Observance(gmtoff=-10,
                       rules=Cook,
                       format='CK%sT',
                       until=None),
        ]

    class Tahiti(Zone):
        name = 'Tahiti'
        observances = [
            Observance(gmtoff=(-9, -58, -16),
                       rules=None,
                       format='LMT',
                       until=(1912, Oct)),
            Observance(gmtoff=-10,
                       rules=None,
                       format='TAHT',
                       until=None),
        ]

    class Tarawa(Zone):
        name = 'Tarawa'
        observances = [
            Observance(gmtoff=(11, 32, 4),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=12,
                       rules=None,
                       format='GILT',
                       until=None),
        ]

    class Tongatapu(Zone):
        name = 'Tongatapu'
        observances = [
            Observance(gmtoff=(12, 19, 20),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=(12, 20),
                       rules=None,
                       format='TOT',
                       until=1941),
            Observance(gmtoff=13,
                       rules=None,
                       format='TOT',
                       until=1999),
            Observance(gmtoff=13,
                       rules=Tonga,
                       format='TO%sT',
                       until=None),
        ]

    class Wake(Zone):
        name = 'Wake'
        observances = [
            Observance(gmtoff=(11, 6, 28),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=12,
                       rules=None,
                       format='WAKT',
                       until=None),
        ]

    class Wallis(Zone):
        name = 'Wallis'
        observances = [
            Observance(gmtoff=(12, 15, 20),
                       rules=None,
                       format='LMT',
                       until=1901),
            Observance(gmtoff=12,
                       rules=None,
                       format='WFT',
                       until=None),
        ]

