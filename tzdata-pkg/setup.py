#!/usr/bin/python
from os.path import isfile
import os
import re

from setuptools import setup


if isfile("MANIFEST"):
    os.unlink("MANIFEST")


TOPDIR = os.path.dirname(__file__) or "."
TZVERSION = '0a'
try:
    version_file = open(TOPDIR + '/raw/version')
except OSError:
    with open(TOPDIR + '/raw/Makefile') as f:
        for line in f:
            m = re.search('VERSION=\s*([^\s]+)', line)
            if m:
                TZVERSION = m.group(1)
                break
else:
    with version_file:
        TZVERSION = version_file.read().strip()
VERSION = "1.%s.%d" % (TZVERSION[:-1], ord(TZVERSION[-1]) - ord('a'))
with open(TOPDIR + '/tzdata/zones') as f:
    ZONES = [line.strip() for line in f]

setup(name="tzdata",
      version=VERSION,
      description="Extensions to the standard Python datetime module",
      author="Alexander Belopolsky",
      author_email="alexander.belopolsky@gmail.com",
      url="https://abalkin.github.io/tz",
      license="Simplified BSD",
      long_description="""\
The tzdata package provides the timezone data for use with the tz package.
""",
      packages=["tzdata"],
      package_data={"tzdata": ["zones"] + ZONES},
      zip_safe=True,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
      ],
      )
