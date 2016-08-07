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


Changes to the datetime module
==============================


References
==========

.. [1] PEP 431 - Time zone support improvements
   (https://www.python.org/dev/peps/pep-0431/)


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
