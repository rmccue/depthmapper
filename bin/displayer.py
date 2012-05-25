#!/usr/bin/env python
"""
bin/displayer.py - 3D data display utility

Usage: python displayer.py [<filename>]
<filename> defaults to snap.data
See README.md for more information.

Requires PyOgre from http://python-ogre.org/
See README.md for installation requirements

Copyright (c) 2012, Ryan McCue
See LICENSE.md for copyright information
"""

# Path hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import depthmapper.displayer as displayer

filename = "snap.data"
if len(sys.argv) > 1:
	filename = sys.argv[1]

app = displayer.DisplayApplication()
app.cloud = displayer.load(filename)
app.go()
