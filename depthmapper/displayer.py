"""
displayer.py - Depthmapper 3D display utility

Requires PyOgre from http://python-ogre.org/
See README.md for installation requirements

Copyright (c) 2012, Ryan McCue
See LICENSE.md for copyright information
"""

import ogre.renderer.OGRE as ogre
import SampleFramework as sf
from depthmapper.utilities import load_timeline as load


class DisplayApplication(sf.Application):
	"""
	The 3D display application class

	Uses the SampleFramework class from the PyOgre project
	"""

	# What resolution is the depth camera?
	resolution = 640, 420

	# How far should the xy coordinates be spread out?
	spreadFactor = 30

	# How far should the z coordinates be spread out?
	depthFactor = 1.0 / 1.0

	# How much should the cube be scaled by?
	scaleFactor = 0.0000000001

	# What portion of point should be displayed?
	# For example, `30` means 1/30th of the points will be displayed
	displayModulo = 30

	# Ignore points with z values below this
	lowerThreshold = 10

	# What is the maximum distance we can have?
	# This is used for coloration of cubes
	maxDistance = 25000

	# What color should the ambient light be?
	ambientLight = 0.6, 0.6, 0.6

	# What color should the spotlight be?
	spotlightDiffuse = .7, 1, 1
	spotlightSpecular = .7, 1, 1

	# How far back should be start the camera?
	cameraStartZ = 10000

	# Vertical field of view for the camera (radians)
	cameraFOV = 1.22

	# How close do we have to be before the camera clips an object?
	cameraClip = 5

	def _createScene(self):
		"""Setup the scene and lighting"""
		sceneManager = self.sceneManager
		sceneManager.ambientLight = self.ambientLight
		sceneManager.shadowTechnique = ogre.SHADOWTYPE_STENCIL_ADDITIVE
		root = sceneManager.getRootSceneNode()
		self.display_cloud(root)

		light = sceneManager.createLight('PointLight')
		light.type = ogre.Light.LT_POINT
		center = {
			'x': (self.resolution[0] / 2) * self.spreadFactor,
			'y': (self.resolution[1] / 2) * self.spreadFactor
		}
		light.position = (center['x'], center['y'], -0.8 * self.cameraStartZ)
		light.diffuseColour = self.spotlightDiffuse
		light.specularColour = self.spotlightSpecular

	def display_cloud(self, root_node):
		"""Create nodes for the point cloud"""
		i = 0
		for key, point in self.cloud.iteritems():
			x, y, z = point.get_coords()
			x *= self.spreadFactor
			y *= self.spreadFactor
			z *= self.depthFactor
			if z < self.lowerThreshold:
				continue

			i += 1
			if i % self.displayModulo:
				continue

			entity = self.sceneManager.createEntity("Point{0}".format(i),
				"cube.mesh")

			# This may not work, depending on the system setup
			# It appears to be related to the graphics card used
			color = z / float(self.maxDistance)
			entity.getSubEntity(0).material.getTechnique(0).getPass(0)\
				.setDiffuse(color * 0.8, 1.0, 1.0, 1.0)
			entity.getSubEntity(0).material.getTechnique(0).getPass(0)\
				.setSpecular(color, 1.0, 1.0, 1.0)

			node = root_node.createChildSceneNode("Point{0}Node".format(i))
			node.scale = (self.scaleFactor, self.scaleFactor, self.scaleFactor)
			node.position = x, -y, z
			node.attachObject(entity)

	def _createCamera(self):
		"""Create the camera entity"""
		self.camera = self.sceneManager.createCamera('PlayerCam')
		center = {
			'x': (self.resolution[0] / 2) * self.spreadFactor,
			'y': (self.resolution[1] / 2) * self.spreadFactor
		}
		self.camera.position = (center['x'], -center['y'], -self.cameraStartZ)
		self.camera.lookAt((center['x'], -center['y'], 0))
		self.camera.nearClipDistance = self.cameraClip
		self.camera.FOVy = self.cameraFOV

	def _createViewports(self):
		"""Create the viewports to show on the screen"""
		viewport = self.renderWindow.addViewport(self.camera)
		viewport.backGroundColor = (1.0, 1.0, 1.0)
		self.camera.aspectRatio = float(viewport.actualWidth) /
			float(viewport.actualHeight)

	def _createFrameListener(self):
		"""Create the FrameListener"""
		self.frameListener = FrameListener(self.renderWindow, self.camera)
		self.frameListener.unittest = self.unittest
		self.frameListener.showDebugOverlay(True)
		self.root.addFrameListener(self.frameListener)


class FrameListener(sf.FrameListener):
	"""Listener for events in the viewport"""
	def __init__(self, renderWindow, camera, bufferedKeys=False,
		bufferedMouse=False, bufferedJoy=False):
		sf.FrameListener.__init__(self, renderWindow, camera, bufferedKeys,
			bufferedMouse, bufferedJoy)
		self.moveSpeed = 300
