#!/usr/bin/env python
"""
bin/collector.py - Collector utility

Usage: python collector.py [<filename>]
<filename> defaults to snap.data
See README.md for more information.

Requires PyKinect from http://pytools.codeplex.com/wikipage?title=PyKinect
See README.md for installation requirements

Copyright (c) 2012, Ryan McCue
See LICENSE.md for copyright information
"""

# Path hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import depthmapper.collector as collector

filename = "snap.data"
if len(sys.argv) > 1:
	filename = sys.argv[1]

collector.setup()
snapshot = collector.snapshot()
collector.teardown()
collector.save(snapshot, filename)
