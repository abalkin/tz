import os
import textwrap

import sys

from datetime import datetime, timezone

HEADER = """\
from zic.classes import *
from datetime import *


"""
PKG_DIR = os.path.dirname(__file__)
RAW_FILES = [
    'africa', 'antarctica', 'asia', 'australasia',
    'europe', 'northamerica', 'southamerica'
]


def lines(input):
    """Remove comments and empty lines"""
    for raw_line in input:
        line = raw_line.strip()
        if line and not line.startswith('#'):
            yield strip_comments(line)


def strip_comments(line):
    quoted = False
    for i, c in enumerate(line):
        if c == '"':
            quoted = not quoted
        elif c == "#" and not quoted:
            return line[:i].strip()
    return line


OBSERVANCE_TEMPLATE = """\
Observance(gmtoff={},
           rules={},
           format='{}',
           until={}),
"""


def compile(infile, outfile=None):
    with open(infile) as input:
        if outfile is None:
            compile_stream(input, sys.stdout)
        else:
            with open(outfile, 'w') as output:
                compile_stream(input, output)


def compile_stream(input, output, header=HEADER):
    output.write(header)
    observances = state = None
    zones = {}
    rules = {}
    for line in lines(input):
        fields = line.split()
        if fields[0] == 'Zone':
            names = fields[1].split('/')
            z = zones
            for name in names:
                z = z.setdefault(name, {})
            observances = z.setdefault('observances', [])
            state = 'Zone'
            del fields[:2]
        elif fields[0] == 'Rule':
            rules.setdefault(fields[1], []).append(fields[2:])
        if state == 'Zone':
            gmtoff, zone_rules, format = fields[:3]
            until = format_until(*fields[3:])
            if until is None:
                state = None

            observances.append(
                format_observance(gmtoff, zone_rules, format, until))
    print_rules(rules, file=output)
    print_zones(zones, file=output)

RULE_TEMPLATE = ('Rule({}, {}, {}, {}, {},\n'
                 '     at={},\n'
                 '     save={}, letters={!r})')


def format_rule(begin, end, type, in_month, on, at, save, letters):
    begin = int(begin)
    if end == 'only':
        end = begin + 1
    elif end == 'max':
        end = 10000
    else:
        end = int(end) + 1
    if type == '-':
        type = None
    if letters == '-':
        letters = ''
    at = format_at(at)
    save = format_time(save)
    return RULE_TEMPLATE.format(begin, end, type, in_month,
                                on, at, save, letters)

TIME_FORMATS = ['%H', '%H:%M', "%H:%M:%S"]
TIME_TYPES = {
    'w': 'wall',
    'u': 'utc',
    'g': 'utc',
    'z': 'utc',
    's': 'std',
}

def format_time(t):
    if t == '-':
        return 'timedelta(0)'
    if t.startswith('24'):
        return 'timedelta(1)'
    n = t.count(':')
    fmt = TIME_FORMATS[n]
    t = datetime.strptime(t, fmt).time()
    args = ['hours={0.hour}', 'minutes={0.minute}', 'seconds={0.second)']
    template = 'timedelta(%s)' % ', '.join(args[:n+1])
    return template.format(t)


def format_at(at):
    try:
        time_type = TIME_TYPES[at[-1]]
    except KeyError:
        time_type = 'wall'
    else:
        at = at[:-1]
    return '(%s, %r)' % (format_time(at), time_type)


def print_rules(rules, file):
    prefix = ' ' * 8
    for name, lines in rules.items():
        file.write('class %s(Rules):\n'
                   '    name ="%s"\n'
                   '    rules = [\n' % (rules_name(name), name))
        for args in lines:
            rule = format_rule(*args)
            file.write(textwrap.indent(rule, prefix) + ',\n')
        file.write('    ]\n\n')

TIME_UNITS = 'hours', 'minutes', 'seconds'


def time_parts(time):
    parts = time.split(':')
    ch = parts[-1][-1]
    if ch in TIME_TYPES:
        parts[-1] = parts[-1][:-1]
    parts = [p.lstrip('0') or '0' for p in parts]
    parts.append(TIME_TYPES.get(ch, 'wall'))
    return parts


def format_until(year=None, month=None, day=None, time=None):
    if year is None:
        return None
    if month is None:
        return year
    until = [year, month.lstrip('0')]
    if day:
        until.append(day.lstrip('0'))
    if time:
        until.extend(time_parts(time))
    return '(%s)' % ', '.join(until)


def format_delta(delta):
    sign = 1
    if delta.startswith('-'):
        sign = -1
        delta = delta[1:]
    parts = [sign*int(p) for p in delta.split(':')]
    while len(parts) > 1 and parts[-1] == 0:
        del parts[-1]
    if len(parts) == 1:
        return repr(parts[0])
    return repr(tuple(parts))


def format_observance(gmtoff, rules, format, until):
    if rules == '-':
        rules = None
    elif ':' in rules:
        rules = "'%s'" % rules
    else:
        rules = rules_name(rules)
    return OBSERVANCE_TEMPLATE.format(format_delta(gmtoff),
                                      rules, format, until)


def print_zones(zones, file, indent=0):
    for name, info in sorted(zones.items()):
        try:
            observances = info['observances']
        except KeyError:
            file.write(indent * ' ' + 'class %s:\n' % name)
            print_zones(info, file, indent + 4)
        else:
            prefix = indent * ' '
            file.write(prefix + 'class %s(Zone):\n' % zone_name(name))
            file.write(prefix + '    name = %r\n' % name)
            file.write(prefix + '    observances = [\n')
            for observance in observances:
                file.write(textwrap.indent(observance, prefix + 8 * ' '))
            file.write(prefix + '%s]\n\n' % (4 * ' '))


def rules_name(name):
    return name.replace('-', '_')

zone_name = rules_name

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: zic [--all | infile [outfile]]")
        sys.exit(1)
    if sys.argv[1] == '--all':
        for f in RAW_FILES:
            raw_file = os.path.join('raw', f)
            out_file = os.path.join(PKG_DIR, f + '.py')
            compile(raw_file, out_file)
    else:
        compile(*sys.argv[1:])
