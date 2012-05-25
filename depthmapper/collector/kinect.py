"""
collector/kinect.py - Kinect data collection

Requires PyKinect from http://pytools.codeplex.com/wikipage?title=PyKinect
See README.md for installation requirements

Copyright (c) 2012, Ryan McCue
See LICENSE.md for copyright information
"""

import thread
import ctypes

from pykinect import nui

from .. import utilities as utils

from itertools import izip_longest
import time

DEPTH_WINSIZE = 640, 480
VIDEO_WINSIZE = 640, 480
video_display = False

timeline = utils.Timeline()


class KinectRuntime(nui.Runtime):
	"""Subclass of the normal Kinect runtime to allow proper shutdown"""
	please_stop = False

	def stop_thread(self):
		self.please_stop = True

	def _event_thread(self):
		handles = (ctypes.c_voidp * 3)()
		handles[0] = self._skeleton_event
		handles[1] = self._depth_event
		handles[2] = self._image_event
		while not self.please_stop:
			wait = nui._WaitForMultipleObjects(3, handles, False, nui._INFINITE)
			if wait == 0:
				# skeleton data
				try:
					frame = self._nui.NuiSkeletonGetNextFrame(0)
				except KinectError:
					continue

				for curSkeleton in frame.SkeletonData:
					if curSkeleton.eTrackingState !=
					SkeletonTrackingState.NOT_TRACKED:
						self.skeleton_frame_ready.fire(frame)
						break
			elif wait == 1:
				# depth event
				depth_frame = self._nui.NuiImageStreamGetNextFrame(
					self.depth_stream._stream, 0
				)
				self.depth_frame_ready.fire(depth_frame)
				self._nui.NuiImageStreamReleaseFrame(
					self.depth_stream._stream, depth_frame
				)
			elif wait == 2:
				# image event
				depth_frame = self._nui.NuiImageStreamGetNextFrame(
					self.video_stream._stream, 0
				)
				self.video_frame_ready.fire(depth_frame)
				self._nui.NuiImageStreamReleaseFrame(
					self.video_stream._stream, depth_frame
				)
				pass
			else:
				# wait failed in some form (abandoned, timeout, or failed), this
				# ends our loop when we close our events.
				break


# From the Python documentation:
# http://docs.python.org/library/itertools.html#recipes
def grouper(n, iterable, fillvalue=None):
	"grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
	args = [iter(iterable)] * n
	return izip_longest(fillvalue=fillvalue, *args)


# Based on:
# http://channel9.msdn.com/Series/KinectSDKQuickstarts/Working-with-Depth-Data
def depth_frame_ready(frame):
	"""Callback for the Kinect when the depth camera captures a new frame"""
	with screen_lock:
		cloud = utils.PointCloud()
		x = 1
		y = 1
		first = None
		for bit in frame.image.bits:
			if first is None:
				first = bit
				continue

			distance = first + (bit << 8)
			x += 1
			if x > DEPTH_WINSIZE[0]:
				x = x % DEPTH_WINSIZE[0]
				y += 1

			first = None
			point = utils.Point(x, y, distance)
			cloud.add_point(point)

		timeline.set_cloud(frame.timestamp, cloud)


def get_point_cloud():
	"""Get the latest point cloud collected from the data"""
	last = None
	while not last:
		time.sleep(3)
		with screen_lock:
			last = timeline.get_last()
	return last


def initialize():
	"""Setup the Kinect hardware and register callbacks"""
	global screen_lock, screen, kinect
	screen_lock = thread.allocate()

	kinect = KinectRuntime()

	kinect.depth_frame_ready += depth_frame_ready
	#kinect.video_frame_ready += video_frame_ready

	#kinect.video_stream.open(nui.ImageStreamType.Video, 2,
	# nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
	kinect.depth_stream.open(nui.ImageStreamType.Depth, 2,
		nui.ImageResolution.Resolution640x480, nui.ImageType.Depth)


def uninitialize():
	"""Shutdown the Kinect hardware"""
	global kinect
	with screen_lock:
		# Wait a second to ensure that everything is cleaned up
		kinect.stop_thread()
		time.sleep(1)
		kinect.close()
