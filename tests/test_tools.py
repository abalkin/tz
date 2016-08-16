import pytest
from datetime import datetime
from tz.tools import pairs, enfold


@pytest.mark.parametrize('seq, out', [
    ([], []),
    ([1], []),
    ([1, 2], [(1, 2)]),
    (range(5), [(0, 1), (1, 2), (2, 3), (3, 4)]),
])
def test_pairs(seq, out):
    p = pairs(seq)
    assert out == list(p)


def test_enfold():
    d0 = datetime(1, 1, 1)
    d1 = enfold(d0, fold=1)
    assert d1.fold == 1
    d2 = enfold(d1, fold=0)
    assert getattr(d2, 'fold', 0) == 0
