"""
collector/__init__.py - Collector abstraction class

This class is used for future abstraction of Depthmapper from the
Kinect hardware.

Copyright (c) 2012, Ryan McCue
See LICENSE.md for copyright information
"""

import depthmapper.collector.kinect
from depthmapper.utilities import save_timeline as save


def snapshot():
	"""Get the latest snapshot of the depth data"""
	pointcloud = depthmapper.collector.kinect.get_point_cloud()
	return pointcloud


def setup():
	"""Setup and initialize the hardware"""
	depthmapper.collector.kinect.initialize()


def teardown():
	"""Stop and uninitialize the hardware"""
	depthmapper.collector.kinect.uninitialize()
