from collections import namedtuple

Extent = namedtuple('Extent', 'min_x max_x min_y max_y')


class WAsP_Map:
    def __init__(self):
        self.header = []
        self.lines = []

    def __repr__(self):
        return f"WAsP_Map (header={bool(self.header)}, {len(self.lines)} lines)"

    @classmethod
    def from_file(cls, fpath: str):
        """Reads and parses the WAsP map into this object"""
        with open(fpath, 'r') as f:
            content = f.readlines()

        self = cls()
        self.header = ''.join(content[:4])

        wline = None
        pairs_to_next_metadata_line = 0
        for l in content[4:]:
            if pairs_to_next_metadata_line == 0:
                wline = WAsP_Line.from_metadata_string(l)
                pairs_to_next_metadata_line = wline.n_points
            else:
                n_pairs = wline.add_coordinates_from_string(l)
                pairs_to_next_metadata_line -= n_pairs

            if pairs_to_next_metadata_line == 0 and wline:
                self.lines.append(wline)

        return self

    def _get_map_string(self, *args, **kwargs) -> str:
        """Converts the information in the object to string, ready to be output to file"""
        body_str = ''.join([l.to_str(*args, **kwargs) for l in self.lines])
        return self.header + body_str

    def save(self, fpath: str, elevation=True, roughness=True):
        """
        Saves the information to the specified location in WAsP map format
        :param fpath: location where the file will be written
        :param elevation: boolean flag, True allows the elevation information to be saved
        :param roughness: boolean flag, True allows the roughness information to be saved
        """
        with open(fpath, 'w') as f:
            f.write(self._get_map_string(elevation=elevation, roughness=roughness))

    @property
    def extent(self):
        """Calculates the extent of the map. Returns a namedtuple with min_x, max_x, min_y and max_y"""
        if not self.lines: return None

        min_x, max_x, min_y, max_y = self.lines[0].extent
        for l in self.lines[1:]:
            l_extent = l.extent
            min_x = min(min_x, l_extent.min_x)
            max_x = max(max_x, l_extent.max_x)
            min_y = min(min_y, l_extent.min_y)
            max_y = max(max_y, l_extent.max_y)
        
        return Extent(min_x, max_x, min_y, max_y)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class WAsP_Line:
    def __init__(self, r_left=None, r_right=None, elev=None, n_points=None):
        self.r_left = r_left
        self.r_right = r_right
        self.elev = elev
        self.n_points = n_points
        self.coordinates = []

    def __repr__(self):
        return f"WAsP_Line(r_left={self.r_left}, r_right={self.r_right}, elev={self.elev}, n_points={self.n_points})"

    @classmethod
    def from_metadata_string(cls, metadata_str: str) -> object:
        """Extracts the line metadata (roughnesses, elevation and number of points) from the metadata
        string coming from the map file"""
        self = cls()

        metadata = metadata_str.split()
        self.n_points = int(metadata.pop())

        if len(metadata) > 1:
            self.r_left = float(metadata.pop(0))
            self.r_right = float(metadata.pop(0))
        if metadata:
            self.elev = float(metadata.pop(0))

        assert not metadata  # nothing left

        return self

    def add_coordinates_from_string(self, s: str) -> int:
        """Adds points coordinates as found in the string from the file to this object"""
        coords = s.split()
        pairs = [(float(i), float(j)) for i, j in zip(coords[::2], coords[1::2])]
        self.coordinates.extend(pairs)
        return len(pairs)

    def to_str(self, elevation=True, roughness=True) -> str:
        """Converts the line information to string, ready to be written file"""
        has_something_to_write = (elevation and self.elev is not None) or (roughness and self.r_left is not None)
        if not has_something_to_write: return ''

        line_string = ' ' * 4
        if self.r_left is not None and roughness: line_string += f"{self.r_left:<10} {self.r_right:<10} "
        if self.elev is not None and elevation: line_string += f"{self.elev:<10} "
        line_string += f"{self.n_points}\n"

        for i in range(0, len(self.coordinates), 4):
            pair_quartet = self.coordinates[i:i + 4]
            line_string += ' ' * 5 + '    '.join(['{}    {}'.format(*j) for j in pair_quartet]) + '\n'

        return line_string

    @property
    def extent(self):
        """Calculates the extent of the line. Returns a namedtuple with min_x, max_x, min_y and max_y"""
        if not self.coordinates: return None

        min_x, max_x = self.coordinates[0][0], self.coordinates[0][0]
        min_y, max_y = self.coordinates[0][1], self.coordinates[0][1]
        for c in self.coordinates[1:]:
            min_x = min(min_x, c[0])
            max_x = max(max_x, c[0])
            min_y = min(min_y, c[1])
            max_y = max(max_y, c[1])

        return Extent(min_x, max_x, min_y, max_y)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

