# -*- coding: utf-8 -*-

"""
jishaku.meta
~~~~~~~~~~~~

Meta information about jishaku.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

from collections import namedtuple

__all__ = (
    '__author__',
    '__copyright__',
    '__docformat__',
    '__license__',
    '__title__',
    '__version__',
    'version_info'
)

# pylint: disable=invalid-name
VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=420, minor=69, micro=0, releaselevel='final', serial=0) # real version is major=1 and minor=20

__author__ = 'Gorialis'
__copyright__ = 'Copyright 2020 Devon (Gorialis) R'
__docformat__ = 'restructuredtext en'
__license__ = 'MIT'
__title__ = '🅱️ishaku' # real name is Jishaku
__version__ = '.'.join(map(str, (version_info.major, version_info.minor, version_info.micro)))
