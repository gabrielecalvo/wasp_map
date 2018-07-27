# Wasp Map
Library that lets you load WAsP maps into python objects and apply transformation in the python environment.

## Examples
```python
from wasp_map import WAsP_Map
wasp_map = WAsP_Map.from_file('<path-to-map-file>')

extent = wasp_map.extent
# this return a namedtuple like:
# Extent(min_x=943059.2, max_x=956644.7, min_y=5124678.0, max_y=5139386.0)

contour_lines = wasp_map.lines
# this return a list of WAsP_Line objects like:
# WAsP_Line(r_left=0.03, r_right=0.0, elev=None, n_points=4)

wasp_map.save('<path-to-output-map-file>', elevation=True, roughness=False)
# this will save, in WAsP map format, only the elevation information to the specified path
```