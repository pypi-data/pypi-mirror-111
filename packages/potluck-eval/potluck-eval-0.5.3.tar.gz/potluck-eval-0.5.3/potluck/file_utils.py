"""
file_utils.py

File-management utilities.
"""

import os
import time
import datetime
import inspect


TIMESTAMP_FORMAT = "%Y%m%d@%H:%M:%S"
"""
Format for timestamps (see `time.strftime`).
"""


def timestamp(when=None):
    """
    Returns a timestamp string based on the current time, or based on a
    given datetime.datetime object or time value in seconds-since-epoch
    format.

    TODO: Time zone issues with showing these to users?
    """
    if when is None:
        when = time.gmtime()

    if isinstance(when, datetime.datetime):
        return when.strftime(TIMESTAMP_FORMAT)
    else:
        return time.strftime(TIMESTAMP_FORMAT, when)


def time_from_timestamp(timestamp):
    """
    Converts a timestamp back into a datetime.datetime.
    """
    return datetime.datetime.strptime(timestamp, TIMESTAMP_FORMAT)


def potluck_src_dir():
    """
    Returns the absolute path to the directory where this file is
    located.
    """
    return os.path.abspath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    # TODO: Use pkg_resources instead!


def get_spec_module_name():
    """
    Uses the inspect module to get the name of the specifications module,
    assuming that we're in a function which was ultimately called from
    that module, and that module is the only one in our current call
    stack that ends with '.spec'. Returns 'unknown' if it can't find an
    appropriate call frame in the current stack.
    """
    cf = inspect.currentframe()
    while (
        hasattr(cf, "f_back")
    and not cf.f_globals.get("__name__").endswith('.spec')
    ):
        cf = cf.f_back

    if cf:
        result = cf.f_globals.get("__name__", "unknown")
    else:
        result = "unknown"

    del cf

    return result


def get_spec_file_name():
    """
    Uses the inspect module to get the path of the specifications file,
    assuming that we're in a function which was ultimately called from
    that module, and that module is the only one in our current call
    stack whose filename ends with '[/]spec.py'. Returns 'unknown' if it
    can't find an appropriate call frame in the current stack.
    """
    cf = inspect.currentframe()
    while (
        hasattr(cf, "f_back")
    and not cf.f_globals.get("__file__").endswith(os.path.sep + 'spec.py')
    ):
        cf = cf.f_back

    if cf:
        result = cf.f_globals.get("__file__", "unknown")
    else:
        result = "unknown"

    del cf

    return result


def unused_filename(orig_name):
    """
    Given a desired filename, adds a numerical suffix to the filename
    which makes it unique. If the file doesn't already exist, it returns
    the given name without any suffix. If the given filename already has
    a numerical suffix, it will be incremented until no file by that name
    exists.
    """
    # If the file doesn't exist, it's already unused
    if not os.path.exists(orig_name):
        return orig_name

    # Split the filename part
    dirs, name = os.path.split(orig_name)

    # Split the base + extension
    base, ext = os.path.splitext(name)

    # Get bits of base
    bits = base.split('-')
    last_part = bits[-1]
    first_stuff = '-'.join(bits[:-1])

    # If last part is a numeric suffix already...
    if last_part.isdigit():
        next_digit = int(last_part) + 1
        new_name = first_stuff + '-' + str(next_digit) + ext
        return unused_filename(os.path.join(dirs, new_name))
    else:
        return unused_filename(os.path.join(dirs, base + "-1" + ext))
