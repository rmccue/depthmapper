# Reflection

## Known Bugs
* One major known bug is that coloration of cubes in the displayer does not
  always work. The code written should make nearer cubes a red color, with
  distant cubes white, however, this does not always occur.

  Consultation with members of the Ogre IRC channel indicates that this may be
  dependent on the graphics card used, and the shaders used during rendering.
  While the coloration does work on the development machine used, it is known
  to not work on others tested.

* The displayer may crash while run depending on the graphics card used. Less
  powerful graphics cards are unable to have as many objects, meaning that the
  number of cubes created will have to be changed. A class property is provided
  for this (`DisplayApplication.displayModulo`), however a dynamic system would
  be a better way to handle this.

  Unfortunately, it is not possible to catch this error as an exception, as the
  crash occurs on the GPU itself.

## Future Improvements
* One place where the project could be expanded is to create an animation of the
  3D environment. The `Timeline` class is written to allow this purpose, however
  both the collector and the displayer use `PointCloud` objects. Rewriting this
  would be fairly trivial, however would most likely require an indepth
  knowledge of the Ogre system in addition to requiring extra algorithms to move
  the point cubes instead of destroying and recreating millions of objects.

* Hardware independence could be achieved by creating extra classes for
  different hardware. The collector module (`depthmapper.collector`) would need
  a small amount of rewriting, but the changes would be localised to that module
  as all other modules use the abstraction.

* The libfreenect drivers could be used in place of the official Kinect SDK
  drivers to allow the collector to work on non-Windows platforms. Initial
  research indicated that the amount of documentation for these unofficial
  drivers was of lower quality than the official drivers and did not have 100%
  coverage of all methods. In addition, these drivers are non-official, so they
  may have issues as they are not guaranteed to work by Microsoft.

* If the bug with the coloration of the cubes in the displayer can be resolved,
  the next step would be to use the image data from the Kinect's camera to color
  the cubes. This would make the image much more recognisable from a glance.

  Initial research showed that while this is possible, it might be very hard,
  due to the two cameras using different refresh rates. This could possibly be
  resolved by using two `Timeline` objects and getting the latest data from
  both at the same time, however could cause problems if combined with
  animation.

* A live display of the data as it is collected would also make collecting the
  data a better user experience. Due to the time taken to create and render all
  the cube objects, this is not possible without significant time delays. (See
  next point for how this may be resolved.)

* Rather than creating cubes for each of the points, a mesh could be created
  dynamically from the points. This would reduce the number of objects
  significantly and enable a live display in addition to fixing the bug
  mentioned above.

  However, this requires algorithms to find contiguous shapes in the data. This
  is unfortunately beyond the author's current mathematical ability, however it
  would be possible for a programmer with a better grasp on the mathematical
  algorithms to fix this.
