#!/usr/bin/python
from os.path import isfile
import os
import re

from setuptools import setup

PRE_RELEASE = 'a1'

if isfile("MANIFEST"):
    os.unlink("MANIFEST")


TOPDIR = os.path.dirname(__file__) or "."
TZVERSION = '0a'
with open(TOPDIR + '/raw/Makefile') as f:
    for line in f:
        m = re.search('VERSION=\s*([^\s]+)', line)
        if m:
            TZVERSION = m.group(1)
            break
VERSION = "1.%s.%d" % (TZVERSION[:-1], ord(TZVERSION[-1]) - ord('a'))
VERSION += PRE_RELEASE
with open(TOPDIR + '/tzdata/zones') as f:
    ZONES = [line.strip() for line in f]

setup(name="tzdata",
      version=VERSION,
      description="Timezone data",
      author="Alexander Belopolsky",
      author_email="alexander.belopolsky@gmail.com",
      url="https://abalkin.github.io/tz",
      license="Simplified BSD",
      long_description="""\
The tzdata package provides the timezone data for use with the tz package.
""",
      packages=["tzdata"],
      package_data={"tzdata": ["zones"] + ZONES},
      zip_safe=False,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
      ],
      )
