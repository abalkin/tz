..
  PEP: TBD
  Title: Timezone database for Python
  Version: $Revision$
  Last-Modified: $Date$
  Author: Alexander Belopolsky <alexander.belopolsky@gmail.com>
  Status: Draft
  Type: Standards Track
  Content-Type: text/x-rst
  Created: TBD
  Post-History:


Abstract
========

This PEP proposes adding access to a timezone database from the
standard library.


Rationale
=========

As most modern computing is performed on mobile devices connected
to distributed networks, the notion of a fixed timezone associated
with a given computer is becoming obsolete.  Python 3.6 has a decent
support for obtaining information about the "system" timezone (as
specified by the TZ environment variable or configured in the OS.)
However, if your computer is configured in London, answering a simple
question such as "What time is it in Sydney, Australia when markets open
at 9:30 am in New York?" is very difficult using Python even on the
operating systems that ship wit a high quality timezone database.

Introduction
============

New packages
============

The tz package
--------------

The :mod:`tz` package serves as a top namespace for the :class:`tzinfo`
objects.  After importing :mod:`tz`, the users can access timezones using
their dotted names::

   >>> import tz
   >>> tz.America.New_York
   tz.America.New_York

A dotted name of a timezone is obtained from its id by replacing '/' characters
with dots ('.'), '-' characters with '_', and removing the dot characters (if
any).



The tzdata package
------------------

.. function:: zones(area=None)

   Returns an iterable over the list of zones in the given area.  If the area
   is not provided, all zones are generated.

.. function:: areas(area=None)

   Returns an iterable over the list of sub-areas in the given area.  If the
   area is not provided, iterable over the list of top areas is returned.

.. function:: aliases(area=None)

   Returns a iterable over the list of aliases in the given area.  The
   aliases are returned as (name, target) pairs.

.. function:: get(tzid)

   Returns the data necessary to instantiate ``tzinfo(tzid)``.  The returned
   object should have the following attributes:

   .. attribute:: types

   A list of local time types.  Each item is a tuple
   ``(utcoffset, dstoffset, abbr)``, where *utcoffset* and *dstoffset* are
   :class:`timedelta` instances representing the UTC offset and DST
   correction (included in the UTC offset) and *abbr* is a string containing
   the timezone abbreviation.

   .. attribute:: times

   A list (or an iterable) of ``(transition_time, type_index)`` tuples, where
   the *transition_time* is a :class:`datetime` instance representing the wall
   time at which the transition to the new local time type takes place and
   *type_index* is an index into the :attr:`types` array.

   .. attribute:: rules



Changes to the datetime module
==============================

The tzinfo factory
------------------

The ``datetime.tzinfo`` constructor will become a factory method that
takes a text string in formats acceptable for the TZ environment variable.
For example::

   >>> import datetime
   >>> datetime.tzinfo('America/New_York')
   tz.America.New_York
   >>> datetime.tzinfo('AEST-10AEDT,M10.1.0,M4.1.0/3')
   tz.PosixRules('AEST-10AEDT,M10.1.0,M4.1.0/3')


References
==========

.. [1] PEP 431 - Time zone support improvements
   (https://www.python.org/dev/peps/pep-0431/)
.. [2] Sources for time zone and daylight saving time data
   (https://www.iana.org/time-zones/repository/tz-link.html)
.. [3] RFC 7808 - Time Zone Data Distribution Service
   (https://tools.ietf.org/html/rfc7808)


Copyright
=========

This document has been placed in the public domain.



..
   Local Variables:
   mode: indented-text
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   coding: utf-8
   End:
