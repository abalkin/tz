import io
from tzdata.zic import strip_comments, lines, compile_stream, compile, \
    format_time
from tzdata import raw_file
import pytest
import os


@pytest.mark.parametrize('line,stripped', [
    ('no comments',
     'no comments',),
    ('some # comments',
     'some'),
])
def test_strip_comments(line, stripped):
    assert stripped == strip_comments(line)


ny_raw = """\
# Zone  NAME            GMTOFF  RULES   FORMAT  [UNTIL]
Zone America/New_York   -4:56:02 -      LMT     1883 Nov 18 12:03:58
                        -5:00   US      E%sT    1920
                        -5:00   NYC     E%sT    1942
                        -5:00   US      E%sT    1946
                        -5:00   NYC     E%sT    1967
                        -5:00   US      E%sT
"""

ny_python = """\
class America:
    class New_York(Zone):
        name = 'New_York'
        observances = [
            Observance(gmtoff=-timedelta(hours=4, minutes=56, seconds=2),
                       rules=None,
                       format='LMT',
                       until=('1883', 'Nov', '18', '12:03:58')),
            Observance(gmtoff=-timedelta(hours=5, minutes=0),
                       rules=US,
                       format='E%sT',
                       until=1920),
            Observance(gmtoff=-timedelta(hours=5, minutes=0),
                       rules=NYC,
                       format='E%sT',
                       until=1942),
            Observance(gmtoff=-timedelta(hours=5, minutes=0),
                       rules=US,
                       format='E%sT',
                       until=1946),
            Observance(gmtoff=-timedelta(hours=5, minutes=0),
                       rules=NYC,
                       format='E%sT',
                       until=1967),
            Observance(gmtoff=-timedelta(hours=5, minutes=0),
                       rules=US,
                       format='E%sT',
                       until=None),
        ]
"""


def test_lines():
    input = io.StringIO(ny_raw)
    line_list = list(lines(input))
    assert line_list[-1] == '-5:00   US      E%sT'


def test_zic():
    input = io.StringIO(ny_raw)
    output = io.StringIO()
    compile_stream(input, output, header='')
    assert ny_python == output.getvalue()


def test_print_zones():
    pass


@pytest.mark.parametrize('file', [
    "africa", "antarctica", "asia", "australasia",
    "europe", "northamerica", "southamerica",
])
def test_generated(monkeypatch, tmpdir, file):
    monkeypatch.chdir(tmpdir)
    compile(raw_file(file), file + '.py')
    assert os.path.exists(file + '.py')
    namespace = {}
    with open(file + '.py') as f:
        exec(f.read(), namespace)
    assert 'Zone' in namespace


@pytest.mark.parametrize('at,result', [
    ('-', 'timedelta(0)'),
    ('2', 'timedelta(hours=2)'),
    ('2:00', 'timedelta(hours=2, minutes=0)'),
    ('15:00', 'timedelta(hours=15, minutes=0)'),
    ('00:00', 'timedelta(hours=0, minutes=0)'),
])
def test_format_time(at, result):
    assert result == format_time(at)
