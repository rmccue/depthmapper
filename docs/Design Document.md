# CSSE1001 Assignment 3 Design Document
Name: Ryan McCue  
Student Number: 42907510  
Project Title: Depth Mapper

## Description
The aim of the project is to create two separate yet linked utilities to read
depth data from a Kinect, and to display it in a browsable 3D interface.

## User Interface
The user interface consists of two separate utilities: the data collector and
the data displayer.

### Data Collector
The project contains a data collection utility. This utility is used for reading
the data from the hardware, and stores the data in a serialized format. This
enables the data to be displayed at a later date without requiring the hardware
to be connected.

The collector is designed to be hardware-agnostic, utilising an abstraction
module. This enables the Kinect hardware to be swapped out in the future for a
more accurate sensor, such as a LIDAR.

### Data Displayer
The data displayer is the main piece of UI that the user interacts with. After
data has been collected, the displayer reads this serialized data format to
create a functional 3D display of the data.

The display shows a 3D grid of points as collected by the collector. From the
default view, the points are be arranged such that the camera appears to be at
the relative position of the Kinect.

The display is navigatable using keyboard and mouse controls. Normal gaming
controls are used for navigation:

* `w`, `s`, `a` and `d` move the camera forward, backward, left and right
  respectively in 3D space
* `Page Up`/`Page Down` move the camera vertically upwards and downwards
  respectively in 3D space
* Mouse movement corresponds to rotation of the camera, with an upward movement
  causing the camera to rotate upward, etc.
* `Esc` is used to quit the application

Lighting and shadowing is used to give a sense of 3D space. The front-facing
side of the points is lit, while the sides are darker, enabling a much clearer
visual display. Coloration is also used, with the points being colored red close
to the physical camera, and white at far distances.

**Note:** Coloration may not work on all platforms, due to issues with the
PyOgre library.

## Design
### Project Overview
The code is split into module files, organised hierarchially. The top-level
directory contains only documentation files, such as `README.md` and
`LICENSE.md`. These files are written in Markdown format, to enable viewing as
plain text in addition to supporting formatting.

Underneath this top-level are three directories. `bin` contains the utilites for
running the collector and displayer as `collector.py` and `displayer.py`
respectively. These can either be run via Python (`python collector.py`, e.g.)
or directly by setting the executable bit
(`chmod +x collector.py; collector.py`). This directory also contains media and
configuration files for PyOgre, and after running, will also contain the
Ogre log (`Ogre.log`).

The `docs` directory contains documentation for the project, including the
design document, initial proposal and reflection document. These are written in
Markdown.

The `depthmapper` directory contains the library Python files used by the binary
utilities. These can also be included into other Python projects as a module.

### Code Overview
The code is split into two main modules, with common methods shared via the
`utilites` module.

The collector consists of the main "collector" module (`depthmapper.collector`)
and hardware specific modules. It uses a submodule to abstract the Kinect's data
from the Kinect SDK, enabling alternate pieces of hardware to be used
(`depthmapper.collector.kinect`). This submodule contains a method to enable the
hardware and set it into the right mode (`initialize`), a method to get point
cloud data from the Kinect (`get_point_cloud`), and a method to shutdown the
hardware once finished (`uninitialize`). The collected data contain 3D
positional data (relative to the current view) as a `PointCloud` object which
contains `Point` objects.

The displayer consists of a main interface module, called "displayer"
(`depthmapper.displayer`). This module is powered by PyOgre and is responsible
for both displaying the data and responding to input from the user. It is
separated into two parts: the `DisplayApplication` class, which is responsible
for creating all the points from the data, and setting up the Ogre scene; and
the `FrameListener` class, which is responsible for responding to user input.
Both of these classes are based on the PyOgre sample classes
(`ogre.renderer.OGRE.sf_OIS`) to reduce redundant code. Where possible, magic
numbers have been removed and abstracted as class properties to allow changing
via dynamic methods (`app.spreadFactor = 2`, e.g.) or via subclassing.

These modules interface with each other via the utilities methods.
`depthmapper.utilities` contains all methods relevant to both utilities. The
`PointCloud` class is responsible for storing data from the collector, and
contains methods for saving and loading data via pickling the point cloud
(`__getstate__` and `__setstate__` respectively). Points are represented via
a `Point` class to enable future expansion of methods, as well as a better
representation (via `repr()`). A `Timeline` class is used to store collections
of `PointCloud` objects in sequential order, enabling the collector to get the
most recent cloud object easily. Point clouds are added atomically to the
timeline, rather than being filled with partial data as it is loaded, ensuring
that a full set of data is always loaded.

For future expansion, a full timeline of point clouds could be stored by the
collector and subsequently loaded into the displayer and animated. However,
this would most likely require optimisation of the collector loop to ensure that
less frames are dropped.

## Support Modules
The project requires the following modules.

### Hardware Interfacing
[PyKinect][] is used as a method of interfacing with the Kinect hardware. The
library is based on the official Kinect for Windows drivers. This is used for
interfacing with the Kinect in the collector.

The PyKinect library was chosen over the alternative [libfreenect][] due to its
nature as an officially provided driver. One of the main disadvantages of using
the official drivers is that they are only available on Windows, while
libfreenect drivers are available on Windows, Linux and OS X. Given that the
main development environment for this project was Windows and the documentation
provided by the official SDK is of a much higher quality, it was decided that
the benefits of the offical drivers outweighed the negatives.

### Data Display
[Python-Ogre][] (aka PyOgre) is used for the interface, as it provides a fairly
useful 3D environment including a camera and a 3D environment. This avoids the
need to recreate those facilities. Internally, this uses the [Ogre3D][] library,
which uses DirectX or OpenGL to render the environment, and is configurable via
a user interface on startup. This is used for the interface in the displayer.


[PyKinect]: http://pytools.codeplex.com/wikipage?title=PyKinect
[libfreenect]: http://openkinect.org/
[Python-Ogre]: http://python-ogre.org/
[Ogre3D]: http://www.ogre3d.org/