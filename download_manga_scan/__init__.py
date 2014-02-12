"""
This file is part of Download Manga Scan.

Foobar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>
"""

VERSION = (0, 0, 1, "f") # following PEP 386
DEV_N = None

__author__ = "Laurent Vergerolle"
__copyright__ = "Copyright (c) 2014 Laurent Vergerolle"
__license__ = "GPL-V3"

def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = "%s.%s" % (version, VERSION[2])
    if VERSION[3] != "f":
        version = "%s%s" % (version, VERSION[3])
        if DEV_N:
            version = "%s.dev%s" % (version, DEV_N)
    return version

__version__ = get_version()

from download_scan import DownloadScan
