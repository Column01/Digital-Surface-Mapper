# General plan for how the software should work

1. Map out the printer bed using the indicator so we have a baseline for flatness.
2. Have the user place their part under the indicator close to the zero location on the print bed and tell the software safe dimensions to move (100mm x 25mm)
3. Calculate a set of grid points and sweep the indicator over them taking readings at each point (maybe have a resolution option so the user could move in increments of 1mm, 10mm or 25mm?)
4. Offset all readings by the baseline flatness of the printer bed to account for the lack of flatness inherent in the system
5. Create a graphical visualization of the surface so the user can see how flat (or not flat) their object is.

## Calculating grid points

Using something like `numpy.arange()` we can generate a set of points given a min and max coordinate as well as a resolution value. Now the caveat to this is you need to ensure your edge distance is configured well or you may end up with points off the edge of your part or very close to the edge. There is no way to guarantee your part is completely square to the travel of the printer so having a good safe edge distance ensures you don't drop off of the part while measuring and risk ruining your measurements.

For example:

```python
import numpy as np

resolution = 1 # step over for each measurement in mm
edge_distance = 3 # distance from edge in mm
max_x = 200 # Max X coordinate
max_y = 200 # Max Y coordinate

part_max_x = 100
part_max_y = 100

bed_xs = np.arange(edge_distance, max_x - edge_distance, resolution)
bed_ys = np.arange(edge_distance, max_y - edge_distance, resolution)

part_xs = np.arange(edge_distance, part_max_x - edge_distance, resolution)
part_ys = np.arange(edge_distance, part_max_y - edge_distance, resolution)
```

Now that we have a list of coordinates to probe, we can move the machine to each coordinate using `G1` commands and then gather a reading from the indicator or multiple readings to average out vibration noise if we want.

## Mesh Theory

Given a certain set of points mapping out the print bed, we should be able to interpolate from our map of measured points on our part to the mesh of the bed and cancel out the error from warped or not flat beds.

```python
from scipy import interpolate

# Do measurements of the bed here and collect a list of Z coordinates at each X and Y from bed_xs and bed_ys
# This is a stunt double :P
bed_zs = [0.0, -0.1, -0.2, -0.3]

# Now we have a function to interpolate a coordinate on the bed's actual value
f_interp = interpolate.interp2d(bed_xs, bed_ys, bed_zs)

# Do measurements of part and collect a list of Z coordinates at each X and Y from part_xs and part_yz
# This is also a stunt double
part_zs = [0.01, 0.02, 0.03, 0.04]

# Now given a known X and Y coordinate, we can account for the bed warp given the interpolated Z value from our measured bed mesh
bed_interp_z = f_interp(part_xs[0], part_ys[0])
if bed_interp_z > 0:
    # Subtract the interpolated value since the bed raises towards the part
    actual_z = part_zs[0] - bed_interp_z
elif bed_interp_z < 0:
    # Add the interpolated value since the bed dips away from the part
    actual_z = part_zs[0] + bed_interp_z
else:
    actual_z = part_zs[0]

print(f"Final part measurement at: x={part_xs[0]} y={part_ys[0]} is {actual_z}")

```
