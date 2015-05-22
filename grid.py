__author__ = 'nzhang-dev'

import numpy as np
import itertools
import collections

class Grid(object):
    def __init__(self, n):
        """
        :param n: size of matrix (n^2 matrix)
        """
        self.data = np.zeros((n, n), dtype=np.uint16)
        self.color_index = 1  # first color is 1
        self.colors = {}

    def add_color(self, coord1, coord2):
        self.set_color(coord1, self.color_index)
        self.set_color(coord2, self.color_index)
        self.set_source(coord1)
        self.set_source(coord2)
        self.colors[self.color_index] = (coord1, coord2)
        self.color_index += 1

    def set_source(self, coord):
        self.data[coord] |= 1

    def color_at(self, coord):
        return self.data[coord] >> 1

    def set_color(self, coord, color):
        self.data[coord] = color << 1 | self.is_source(coord)

    def is_source(self, coord):
        return self.data[coord] & 1

    def is_valid(self):
        return self.data.all()

    def neighbors(self, coord):


        deltas = [
            (-1, 0),
            (1, 0),
            (0, 1),
            (0, -1)
        ]
        arr = []
        for delta in deltas:
            resultant = tuple(a + b for a, b in zip(coord, delta))
            if resultant in self:
                arr.append(resultant)
        return arr

    def __contains__(self, item):
        return all(0 <= ind < m for ind, m in zip(item, self.data.shape))

    def print_path(self, path):
        path_copy = np.copy(self.data)
        for i, coord in enumerate(path, start=1):
            path_copy[coord] = i
        print(path_copy)

    def __str__(self):
        return str(self.data >> 1)

    @classmethod
    def from_data(cls, data_grid):
        if isinstance(data_grid, list):
            shape = (len(data_grid), len(data_grid[0]))
        else:
            shape = data_grid.shape
        grid = cls(shape[0])  # new grid
        dataset = collections.defaultdict(list)
        side_length = shape[0]
        for i, j in itertools.product(range(side_length), repeat=2):
            if data_grid[i][j] != 0:
                dataset[data_grid[i][j]].append((i, j))
        for coords in dataset.values():
            grid.add_color(*coords)
        return grid