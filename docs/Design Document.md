# CSSE1001 Assignment 3 Design Document
Name: Ryan McCue  
Student Number: 42907510  
Project Title: Depth Mapper

## Description
The aim of the project is to create two separate yet linked utilities to read
depth data from a Kinect, and to display it in a browsable 3D interface.

## User Interface
The user interface will consist of two separate utilities: the data collector,
and the data displayer.

### Data Collector
It is expected that the project will collect data in order to display and/or
replay it at a later date. This means that a data collection facility will be
required.

The collector will be focussed on reading the data from the hardware, but will
also contain data for storing the data in a serializable format, such as pickled
data. This will enable the data to be displayed at a later date without
requiring the hardware to be connected.

### Data Displayer
The data displayer will be the main piece of UI that the user interacts with.
After data has been collected, the displayer will create a functional 3D display
of the data.

The display will show a 3D grid of points as collected by the collector. From
the default view, the points will be arranged such that the camera is at the
origin position (that is, the position of the Kinect).

The display will be navigatable using keyboard and mouse controls. Normal gaming
controls will be used for navigation:

* `w`, `s`, `a` and `d` will move the camera forward, backward, left and right
  respectively in 3D space
* Mouse movement will correspond to rotation of the camera, with an upward
  movement causing the camera to rotate upward, etc.
* `Esc` will be used to show a pause menu and/or quit

If possible within time constraints, the images captured by the Kinect's camera
will be mapped to the view, enabling a visual 3D display with real images.
However, as this may require a longer timeframe for development, this may not be
possible. If this is the case, it will display the 3D data as a depth map, with
colouration showing the distance from the Kinect. Without this colouration, the
viewer may require shadowing/lighting to differentiate distance, and this is
expected to be hard to achieve in the specified timeline.

## Design
### Project Overview
The code will be split into module files, organised hierarchially. The
top-level directory will contain only documentation files, such as README and
INSTALL, and a `requirements.txt`. These files will be written in Markdown
format, to enable viewing as plain text in addition to supporting formatting.
The `requirements.txt` will enable easy installation using the [`pip`][pip]
utility.

Three directories will exist under the top directory. `bin` will contain the
executable scripts to run the collector and the displayer as `collector.py` and
`displayer.py`. `docs` will contain documentation on how to use the software,
written in reStructuredText and suitable for later publishing using [Sphinx][]
and [Read The Docs][]. `depthmapper` will contain all the non-executable Python
module files.

### Code Overview
The code will be split into two main modules, with submodules and utilities
shared between them in other modules.

The collector will consist of the main "collector" module
(`depthmapper.collector`). It will use a submodule to abstract the Kinect's
data from the Kinect SDK, enabling alternate pieces of hardware to be used
(`depthmapper.collector.kinect`). This submodule will contain a method to
enable the hardware and set it into the right mode (`initialize`), and a method
to get point cloud data from the Kinect (`get_point_cloud`). This data will
contain 3D positional data (relative to the current view). If time permits,
a `get_color_cloud` [sic] will be added to enable colouration of the points.

The displayer will consist of a main interface module, called "displayer"
(`depthmapper.displayer`). This module will be separated into submodules for
creating the display from the points (`depthmapper.displayer.objectcreator`) and
for controlling any additional interaction from the user
(`depthmapper.displayer.interact`). For a live view of the data, the displayer
will interface directly with the collector.

For stored data, these modules will interface with each other via utilities
methods. `depthmapper.utilities` will contain all relevant methods. The
`depthmapper.utilities.PointCloud` class will be responsible for storing data
from the collector, and will contain methods for saving and loading data via
pickling the point cloud (`__getstate__` and `__setstate` respectively).

## Support Modules
The project will require the following modules.

### Hardware Interfacing
[PyKinect][] will be used as a method of interfacing with the Kinect hardware.
The library is based on the official Kinect for Windows drivers. This will be
used for interfacing with the Kinect in the collector.

### Data Display
[Python-Ogre][] will be used for the interface, as it provides a fairly useful
3D environment including a camera and a 3D environment. This avoids the need to
recreate those facilities. Internally, this uses the [Ogre3D][] library, which
uses DirectX or OpenGL to render the environment. This will be used for the
interface in the displayer.


[pip]: http://www.pip-installer.org/
[Sphinx]: http://sphinx.pocoo.org/
[Read The Docs]: http://readthedocs.org/
[PyKinect]: http://pytools.codeplex.com/wikipage?title=PyKinect
[Python-Ogre]: http://python-ogre.org/
[Ogre3D]: http://www.ogre3d.org/