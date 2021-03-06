# -*- coding: utf-8 -*-

# =============================================================================
#
#    Copyright (C) 2016  Fenris_Wolf, YSPStudios
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =============================================================================

"""
    freelancer.core.hashes - FL hash generation and lookup functions.
"""
import csv
from collections import namedtuple
from freelancer.core import tools, settings, log
_CACHE = {}
_REVERSE = {}

HashResult = namedtuple('HashResult', ('unsigned', 'signed', 'hex', 'text'))

def get_hash(text):
    """get_hash(text)
    Returns the hash for the specified text, or None if it unknown
    """
    return _CACHE.get(text.lower(), None)

def get_string(hash_id):
    """get_string(hash_id)
    Returns the text string matching the specified hash, or None if it unknown
    """
    return _REVERSE.get(int(hash_id), None)

def generate_cache(createid=True):
    """generate_cache(createid=True)
    Generates the hash cache. if createid is True, the hashes are generated by
    running createid.exe. If False, a file (specified in the PyFL config) is
    read instead.
    """
    if createid:
        output = tools.extract_hashes()
    else:
        with open(settings.general['hash_file']) as fih:
            output = fih.read().splitlines()

    csvr = csv.reader(output, delimiter=',', quotechar='"')
    for row in csvr:
        unsign, hexh, sign, text = row[0:4]
        result = HashResult(int(unsign), int(sign), hexh, text)
        low_t = text.lower()
        old = _CACHE.get(low_t)
        if old:
            log.error("Hash Cache: overwritting cache for %s with %s" % (old, result))
        _CACHE[low_t] = result
        _REVERSE[sign] = result

