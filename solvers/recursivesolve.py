__author__ = 'nzhang-dev'

from grid import Grid
import collections
import numpy as np
import time


def solve(g, heuristic):
    colors = [
        (heuristic(points), color, points) for
        color, points in g.colors.items()
    ]
    colors.sort()
    ordered = [(color, points) for _, color, points in colors]
    t = time.time()
    res = _solve(g, ordered, 0)
    print(time.time() - t)
    return res


def _solve(g, colors, index):
    if index >= len(colors):
        return g.is_valid()
    color, (start, end) = colors[index]
    for path in get_paths(g, start, end):
        for coord in path:
            if not g.is_source(coord):
                g.set_color(coord, color)
        if _solve(g, colors, index + 1):
            return True
        for coord in path:
            if not g.is_source(coord):
                g.set_color(coord, 0)
    return False


def failfast(g):
    """
    every free spot must have a path to a source node
    """
    cp = np.copy(g.data)


def longest_distance_heuristic(points):
    distance = sum(abs(a-b) for a, b in zip(*points))
    return distance


def shortest_distance_heuristic(points):
    return -longest_distance_heuristic(points)


def _cache_get_paths(func):
    def key(g, start, end):
        filled_data = tuple((g.data == 0).ravel())
        start_color = g.color_at(start)
        end_color = g.color_at(end)
        return filled_data, start, end, start_color, end_color

    cache = {}

    def wrapper(g, start, end):
        k = key(g, start, end)
        if k in cache:
            return cache[k]
        paths = func(g, start, end)
        cache[k] = paths
        return paths
    return wrapper

@_cache_get_paths
def _get_paths(g, start, end):
    if start == end:
        return (end,),
    start_color = g.color_at(start)
    paths = []
    neighbors = g.neighbors(start)
    neighbors = sorted(neighbors, key=lambda c: manhattan(c, end))
    for neighbor in neighbors:
        if neighbor == end:
            paths.append((start, (end,)))
            continue
        if g.color_at(neighbor) != 0:
            continue
        g.set_color(neighbor, start_color)
        for path in _get_paths(g, neighbor, end):
            paths.append((start, path))
        g.set_color(neighbor, 0)
    return paths


def flatten(path):
    p = []
    while len(path) != 1:
        p.append(path[0])
        path = path[1]
    return p


def get_paths(g, start, end):
    paths = _get_paths(g, start, end)
    for path in paths:
        yield flatten(path)


def manhattan(coord, target):
    return sum(abs(a-b) for a, b in zip(coord, target))

if __name__ == '__main__':
    from grid import Grid
    datagrid = [
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 2, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 3, 0, 0, 5, 0, 5],
        [0, 0, 0, 1, 0, 0, 0, 6]
    ]
    grid = Grid.from_data(datagrid)
    solve(grid, shortest_distance_heuristic)