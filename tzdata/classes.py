from collections import namedtuple

Mon, Tue, Wed, Thu, Fri, Sat, Sun = range(7)
(Jan, Feb, Mar, Apr, May, Jun,
 Jul, Aug, Sep, Oct, Nov, Dec) = range(1, 13)


class Rules:
    pass

Rule = namedtuple('Rule', 'name begin end type in_month on at save letters')
Observance = namedtuple('Observance', 'gmtoff rules format until')


class Zone:
    pass
