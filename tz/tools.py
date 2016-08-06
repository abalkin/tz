import itertools
from datetime import datetime


def pairs(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


if hasattr(datetime, 'fold'):
    def enfold(dt, fold=1):
        return dt.replace(fold=fold)
else:
    class _DatetimeWithFold(datetime):
        __slots__ = ()

        @property
        def fold(self):
            return 1

    def enfold(dt, fold=1):
        if getattr(dt, 'fold', 0) == fold:
            return dt
        args = dt.timetuple()[:6]
        args += (dt.microsecond, dt.tzinfo)
        if fold:
            return _DatetimeWithFold(*args)
        else:
            return datetime(*args)
