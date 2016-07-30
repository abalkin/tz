import textwrap

import sys

HEADER = """\
from tzdata.classes import *
from datetime import *


"""


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
            until = format_until(fields[3:])
            if until is None:
                state = None

            observances.append(
                format_observance(gmtoff, zone_rules, format, until))
    print_rules(rules, file=output)
    print_zones(zones, file=output)


def print_rules(rules, file):
    for name, rules in rules.items():
        file.write('class %s(Rules):\n    pass\n' % name)


TIME_UNITS = 'hours', 'minutes', 'seconds'


def format_until(until):
    until = [(u.lstrip('0') or '0') for u in until]
    n = len(until)
    if n == 0:
        return None
    if n == 1:
        return int(until[0])
    if n == 2:
        return '(%s, %s)' % tuple(until)
    if n == 3:
        return 'date(%s)' % ', '.join(until)
    if n == 4:
        return 'datetime(%s, %s)' % (
            ', '.join(until[:3]),
            ', '.join((u.lstrip('0') or '0') for u in until[3].split(':')))
    raise ValueError('Unexpected until=%s' % until)


def format_delta(delta):
    sign = ''
    if delta.startswith('-'):
        sign = '-'
        delta = delta[1:]
    args = ['%s=%s' % (unit, int(value))
            for unit, value in zip(TIME_UNITS, delta.split(':'))]
    return '%stimedelta(%s)' % (sign, ', '.join(args))


def format_observance(gmtoff, rules, format, until):
    if rules == '-':
        rules = None
    elif ':' in rules:
        rules = "'%s'" % rules
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
            file.write(prefix + 'class %s(Zone):\n' % name)
            file.write(prefix + '    observances = [\n')
            for observance in observances:
                file.write(textwrap.indent(observance, prefix + 8 * ' '))
            file.write(prefix + '%s]\n' % (4 * ' '))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: zic infile [outfile]")
        sys.exit(1)
    compile(*sys.argv[1:])
