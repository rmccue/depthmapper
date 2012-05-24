# Depthmapper

## Requirements
* [Python](http://python.org/)
* [PyOgre](http://python-ogre.org/) (required for displayer)
* [Kinect for Windows SDK](http://www.microsoft.com/en-us/kinectforwindows/develop/)
  (required for collector)
* [PyKinect](http://pytools.codeplex.com/wikipage?title=PyKinect) (required for
  collector)

  **Note:** PyKinect and the Kinect for Windows SDK are only available on
  Windows.

## Setup
1. Install PyOgre and PyKinect
2. Edit `bin/plugins.cfg` and change the paths to suit your machine
3. Run `collector.py` to collect data from the Kinect
4. Run `displayer.py` to display the data in a 3D interface

## Collector
The collector is responsible for collecting the data from the Kinect and saving
it into a format recognisable by the displayer.

### Usage
`python collector.py [<filename>]`

* `<filename>`: an optional filename to save the data to. Defaults to `snap.data`

## Displayer
The displayer is responsible for displaying collected data in a 3D interface.

### Usage
`python displayer.py [<filename>]`

* `<filename>`: an optional filename to save the data to. Defaults to `snap.data`

### Controls
While using the displayer, navigation is controlled through the keyboard and
mouse.

* `w`: move forward
* `a`: move left
* `s`: move backward
* `d`: move right
* `Page Up`: move vertically upwards
* `Page Down`: move vertically downwards
* `Print Screen`: save a screenshot
* `f`: toggle information dialog
* `p`: toggle positional information
* `r`: toggle view mode (full, wireframe, or point mode)

## Screenshots
* http://cl.ly/2T0a352J1z2D12192K04
* http://cl.ly/1d3h411r3C3S1m3O0n2l
* http://cl.ly/0S3U0k153M3R0p2x2c0C