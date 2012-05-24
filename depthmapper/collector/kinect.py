 # ############################################################################
 #
 # Copyright (c) Microsoft Corporation.
 #
 # Available under the Microsoft PyKinect 1.0 Alpha license.  See LICENSE.txt
 # for more information.
 #
 # ###########################################################################/

import thread
import ctypes

from pykinect import nui

import pygame
from pygame.color import THECOLORS
from pygame.locals import *

from .. import utilities as utils

from itertools import izip_longest
import time

KINECTEVENT = pygame.USEREVENT
DEPTH_WINSIZE = 640, 480
VIDEO_WINSIZE = 640, 480
video_display = False
pygame.init()

timeline = utils.Timeline()


# recipe to get address of surface:
# http://archives.seul.org/pygame/users/Apr-2008/msg00218.html
if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
	Py_ssize_t = ctypes.c_int
elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
	Py_ssize_t = ctypes.c_int64
else:
	raise TypeError("Cannot determine type of Py_ssize_t")

_PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
_PyObject_AsWriteBuffer.restype = ctypes.c_int
_PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
								ctypes.POINTER(ctypes.c_void_p),
								ctypes.POINTER(Py_ssize_t)]


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
					if curSkeleton.eTrackingState != SkeletonTrackingState.NOT_TRACKED:
						self.skeleton_frame_ready.fire(frame)
						break
			elif wait == 1:
				# depth event
				depth_frame = self._nui.NuiImageStreamGetNextFrame(self.depth_stream._stream, 0)
				self.depth_frame_ready.fire(depth_frame)
				self._nui.NuiImageStreamReleaseFrame(self.depth_stream._stream, depth_frame)
			elif wait == 2:
				# image event
				depth_frame = self._nui.NuiImageStreamGetNextFrame(self.video_stream._stream, 0)
				self.video_frame_ready.fire(depth_frame)
				self._nui.NuiImageStreamReleaseFrame(self.video_stream._stream, depth_frame)
				pass
			else:
				# wait failed in some form (abandoned, timeout, or failed), this ends our loop
				# when we close our events.
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


def surface_to_array(surface):
	buffer_interface = surface.get_buffer()
	address = ctypes.c_void_p()
	size = Py_ssize_t()
	_PyObject_AsWriteBuffer(buffer_interface,
							ctypes.byref(address), ctypes.byref(size))
	bytes = (ctypes.c_byte * size.value).from_address(address.value)
	bytes.object = buffer_interface
	return bytes


def gui_depth_ready(frame):
	with screen_lock:
		address = surface_to_array(screen)
		#print dir(frame.image.bits)
		frame.image.copy_bits(address)
		#ctypes.memmove(address, frame.image.bits, len(address))
		del address
		pygame.display.update()


def get_point_cloud():
	last = None
	while not last:
		time.sleep(3)
		with screen_lock:
			last = timeline.get_last()
	return last


def initialize():
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
	global kinect
	with screen_lock:
		# Wait a second to ensure that everything is cleaned up
		kinect.stop_thread()
		time.sleep(1)
		kinect.close()


def setup_gui():
	global screen
	screen = pygame.display.set_mode(DEPTH_WINSIZE, 0, 16)
	pygame.display.set_caption('Python Kinect Demo')
	screen.fill(THECOLORS["black"])

	kinect.depth_frame_ready += gui_depth_ready


def gui_loop():
	global screen

	print('Controls: ')
	print(' u - Increase elevation angle')
	print(' j - Decrease elevation angle')
	print(' x - Reset elevation angle')

	# main game loop
	done = False

	while not done:
		e = pygame.event.wait()
		if e.type == pygame.QUIT:
			done = True
			break
		elif e.type == KEYDOWN:
			if e.key == K_ESCAPE:
				done = True
				break
			elif e.key == K_u:
				kinect.camera.elevation_angle = kinect.camera.elevation_angle + 2
			elif e.key == K_j:
				kinect.camera.elevation_angle = kinect.camera.elevation_angle - 2
			elif e.key == K_x:
				kinect.camera.elevation_angle = 2

if __name__ == "__main__":
	initialize()
	setup_gui()
	gui_loop()
