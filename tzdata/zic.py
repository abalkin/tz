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

RULE_TEMPLATE = 'Rule({}, {}, {}, {}, {}, {!r}, {!r}, {!r})'


def format_rule(begin, end, type, in_month, on, at, save, letters):
    begin = int(begin)
    if end == 'only':
        end = begin + 1
    elif end == 'max':
        end == 1000
    else:
        end = int(end) + 1
    if type == '-':
        type = None
    if letters == '-':
        letters = ''

    return RULE_TEMPLATE.format(begin, end, type, in_month,
                                on, at, save, letters)


def print_rules(rules, file):
    prefix = ' ' * 8
    for name, lines in rules.items():
        file.write('class %s(Rules):\n'
                   '    name ="%s"\n'
                   '    rules = [\n' % (rules_name(name), name))
        for args in lines:
            file.write(prefix + format_rule(*args) + ',\n')
        file.write('    ]\n\n')

TIME_UNITS = 'hours', 'minutes', 'seconds'


def format_until(until):
    n = len(until)
    if n == 0:
        return None
    if n == 1:
        return int(until[0])
    return '(%s)' % ', '.join(repr(u) for u in until)


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
            file.write(prefix + '%s]\n' % (4 * ' '))


def rules_name(name):
    return name.replace('-', '_')

zone_name = rules_name

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: zic infile [outfile]")
        sys.exit(1)
    compile(*sys.argv[1:])
