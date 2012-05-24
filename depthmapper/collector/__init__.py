import depthmapper.collector.kinect
from depthmapper.utilities import save_timeline as save


def snapshot():
	pointcloud = depthmapper.collector.kinect.get_point_cloud()
	return pointcloud


def setup():
	depthmapper.collector.kinect.initialize()


def teardown():
	depthmapper.collector.kinect.uninitialize()
	pass


def main():
	pass


if __name__ == "__main__":
	pass
