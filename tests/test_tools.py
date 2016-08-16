import pytest
from tz.tools import pairs


@pytest.mark.parametrize('seq, out', [
    ([], []),
    ([1], []),
    ([1, 2], [(1, 2)]),
    (range(5), [(0, 1), (1, 2), (2, 3), (3, 4)]),
])
def test_pairs(seq, out):
    p = pairs(seq)
    assert out == list(p)
