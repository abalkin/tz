TZFILE
======

| `NAME <#NAME>`__
| `DESCRIPTION <#DESCRIPTION>`__
| `SEE ALSO <#SEE%20ALSO>`__

--------------

` <>`__

NAME
----

tzfile − time zone information

` <>`__

DESCRIPTION
-----------

The time zone information files used by *tzset*\ (3) begin with the
magic characters "TZif" to identify them as time zone information files,
followed by a character identifying the version of the file’s format (as
of 2013, either an ASCII NUL, or ’2’, or ’3’) followed by fifteen bytes
containing zeroes reserved for future use, followed by six four-byte
integer values written in a standard byte order (the high-order byte of
the value is written first). These values are, in order: *
tzh\_ttisgmtcnt*

The number of UT/local indicators stored in the file.

*tzh\_ttisstdcnt*

The number of standard/wall indicators stored in the file.

*tzh\_leapcnt*

The number of leap seconds for which data entries are stored in the
file.

*tzh\_timecnt*

The number of transition times for which data entries are stored in the
file.

*tzh\_typecnt*

The number of local time types for which data entries are stored in the
file (must not be zero).

*tzh\_charcnt*

The number of characters of time zone abbreviation strings stored in the
file.

The above header is followed by *tzh\_timecnt* four-byte signed integer
values sorted in ascending order. These values are written in standard
byte order. Each is used as a transition time (as returned by
*time*\ (2)) at which the rules for computing local time change. Next
come *tzh\_timecnt* one-byte unsigned integer values; each one tells
which of the different types of local time types described in the file
is associated with the time period starting with the same-indexed
transition time. These values serve as indices into an array of *ttinfo*
structures (with *tzh\_typecnt* entries) that appears next in the file;
these structures are defined as follows:

struct ttinfo {

+--------------------------+--------------------------+--------------------------+
|                          |                          |                          |
+--------------------------+--------------------------+--------------------------+
|                          | int32\_t                 | tt\_gmtoff;              |
+--------------------------+--------------------------+--------------------------+
|                          |                          |                          |
+--------------------------+--------------------------+--------------------------+
|                          | unsigned char            | tt\_isdst;               |
+--------------------------+--------------------------+--------------------------+
|                          |                          |                          |
+--------------------------+--------------------------+--------------------------+
|                          | unsigned char            | tt\_abbrind;             |
+--------------------------+--------------------------+--------------------------+

};

Each structure is written as a four-byte signed integer value for
*tt\_gmtoff*, in a standard byte order, followed by a one-byte value for
*tt\_isdst* and a one-byte value for *tt\_abbrind*. In each structure,
*tt\_gmtoff* gives the number of seconds to be added to UT, *tt\_isdst*
tells whether *tm\_isdst* should be set by *localtime (3)* and
*tt\_abbrind* serves as an index into the array of time zone
abbreviation characters that follow the *ttinfo* structure(s) in the
file.

Then there are *tzh\_leapcnt* pairs of four-byte values, written in
standard byte order; the first value of each pair gives the time (as
returned by *time(2))* at which a leap second occurs; the second gives
the *total* number of leap seconds to be applied during the time period
starting at the given time. The pairs of values are sorted in ascending
order by time.

Then there are *tzh\_ttisstdcnt* standard/wall indicators, each stored
as a one-byte value; they tell whether the transition times associated
with local time types were specified as standard time or wall clock
time, and are used when a time zone file is used in handling POSIX-style
time zone environment variables.

Finally there are *tzh\_ttisgmtcnt* UT/local indicators, each stored as
a one-byte value; they tell whether the transition times associated with
local time types were specified as UT or local time, and are used when a
time zone file is used in handling POSIX-style time zone environment
variables.

*Localtime* uses the first standard-time *ttinfo* structure in the file
(or simply the first *ttinfo* structure in the absence of a
standard-time structure) if either *tzh\_timecnt* is zero or the time
argument is less than the first transition time recorded in the file.

For version-2-format time zone files, the above header and data are
followed by a second header and data, identical in format except that
eight bytes are used for each transition time or leap second time. After
the second header and data comes a newline-enclosed,
POSIX-TZ-environment-variable-style string for use in handling instants
after the last transition time stored in the file (with nothing between
the newlines if there is no POSIX representation for such instants).

For version-3-format time zone files, the POSIX-TZ-style string may use
two minor extensions to the POSIX TZ format, as described in
*newtzset*\ (3). First, the hours part of its transition times may be
signed and range from −167 through 167 instead of the POSIX-required
unsigned values from 0 through 24. Second, DST is in effect all year if
it starts January 1 at 00:00 and ends December 31 at 24:00 plus the
difference between daylight saving and standard time.

Future changes to the format may append more data.

` <>`__

SEE ALSO
--------

newctime(3), newtzset(3), zdump(8), zic(8)

--------------
