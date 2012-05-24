import ogre.renderer.OGRE as ogre
import SampleFramework as sf
from depthmapper.utilities import load_timeline as load


class DisplayApplication(sf.Application):
	spreadFactor = 30
	depthFactor = 1.0 / 1.0  # must be float
	scaleFactor = 0.0000000001
	displayModulo = 30
	lowerThreshold = 10

	def _createScene(self):
		sceneManager = self.sceneManager
		sceneManager.ambientLight = 0.6, 0.6, 0.6
		sceneManager.shadowTechnique = ogre.SHADOWTYPE_STENCIL_ADDITIVE
		root = sceneManager.getRootSceneNode()
		self.display_cloud(root)

		light = sceneManager.createLight('PointLight')
		light.type = ogre.Light.LT_POINT
		center = {'x': 320 * self.spreadFactor, 'y': 240 * self.spreadFactor}
		light.position = (center['x'], center['y'], -8000)
		light.diffuseColour = (.7, 1, 1)
		light.specularColour = (.5, .9, .9)

	def display_cloud(self, root_node):
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

			entity = self.sceneManager.createEntity("Point{0}".format(i), "cube.mesh")
			color = z / 25000.0
			entity.getSubEntity(0).material.getTechnique(0).getPass(0).setDiffuse(color * 0.8, 1.0, 1.0, 1.0)
			entity.getSubEntity(0).material.getTechnique(0).getPass(0).setSpecular(color, 1.0, 1.0, 1.0)
			node = root_node.createChildSceneNode("Point{0}Node".format(i))
			node.scale = (self.scaleFactor, self.scaleFactor, self.scaleFactor)
			node.position = x, -y, z
			node.attachObject(entity)

	def _createCamera(self):
		self.camera = self.sceneManager.createCamera('PlayerCam')
		center = {'x': 320 * self.spreadFactor, 'y': 240 * self.spreadFactor}
		self.camera.position = (center['x'], -center['y'], -10000)
		self.camera.lookAt((center['x'], -center['y'], 0))
		self.camera.nearClipDistance = 5
		self.camera.FOVy = 1.22

	def _createViewports(self):
		viewport = self.renderWindow.addViewport(self.camera)
		viewport.backGroundColor = (1.0, 1.0, 1.0)
		self.camera.aspectRatio = float(viewport.actualWidth) / float(viewport.actualHeight)

	def _createFrameListener(self):
		"""Creates the FrameListener."""
		self.frameListener = FrameListener(self.renderWindow, self.camera)
		self.frameListener.unittest = self.unittest
		self.frameListener.showDebugOverlay(True)
		self.root.addFrameListener(self.frameListener)


class FrameListener(sf.FrameListener):
	def __init__(self, renderWindow, camera, bufferedKeys=False, bufferedMouse=False, bufferedJoy=False):
		sf.FrameListener.__init__(self, renderWindow, camera, bufferedKeys, bufferedMouse, bufferedJoy)
		self.moveSpeed = 300
