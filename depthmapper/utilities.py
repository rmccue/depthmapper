"""
utilities.py - Depthmapper utility/abstraction classes

Copyright (c) 2012, Ryan McCue
See LICENSE.md for copyright information
"""

import cPickle as pickle


class Point(object):
	"""A representation of a 0D object in 3D space."""
	x = 0
	y = 0
	z = 0

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def get_coords(self):
		"""Get the x, y, z coordinates for the point"""
		return self.x, self.y, self.z

	def __repr__(self):
		return "<Point({0},{1},{2})>".format(*self.get_coords())


class PointCloud(object):
	"""A container object for a number of points in 3D space"""
	cloud = {}

	def add_point(self, point):
		"""Add the point to the point cloud

		Note: only one Point can exist at a given coordinate (blame the Pauli
		exclusion principle), so any point at the given coordinate will be
		removed."""
		self.cloud[point.get_coords()] = point

	def __iter__(self):
		return iter(self.cloud)

	def iteritems(self):
		return self.cloud.iteritems()

	def __getstate__(self):
		return self.cloud

	def __setstate__(self, state):
		self.cloud = state


class Timeline(object):
	"""A timeline that we can move forward and backward through"""
	timeline = {}
	times = []

	def set_cloud(self, time, cloud):
		"""Set the cloud for the given time"""
		self.timeline[time] = cloud
		self.times.append(time)
		self.times.sort()

	def get_last(self):
		if len(self.times) == 0:
			return None

		last = self.times[-1]
		print "getting last:"
		print last
		print self.timeline[last]
		return self.timeline[last]

	def __iter__(self):
		return TimelineIterator(self)


class TimelineIterator(object):
	"""An iterator for the timeline"""
	timeline = None
	time = None

	def __init__(self, timeline):
		self.timeline = timeline

	def __iter__(self):
		return self

	def next(self):
		if not self.time:
			self.time = 0
		else:
			self.time += 1

		if self.time >= len(self.timeline.times):
			raise StopIteration()

		time = self.timeline.times[self.time]
		return self.timeline.timeline[time]


def load_timeline(filename):
	"""Load a Timeline from a file"""
	handle = open(filename, 'rb')
	result = pickle.load(handle)
	handle.close()
	return result


def save_timeline(timeline, filename):
	"""Serialize and save a Timeline to a file"""
	handle = open(filename, 'wb')
	pickle.dump(timeline, handle, pickle.HIGHEST_PROTOCOL)
	handle.close()
