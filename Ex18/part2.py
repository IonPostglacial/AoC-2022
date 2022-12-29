from collections import deque
from itertools import product
import sys

CUBES_NEIGHBORS = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)


def can_exit_box(start, cubes, box):
    xmin, xmax, ymin, ymax, zmin, zmax = box
    visited_set = set()
    open_list = deque()
    open_list.append(start)

    while open_list:
        x, y, z = open_list.popleft()
        if x < xmin or x > xmax or y < ymin or y > ymax or z < zmin or z > zmax:
            return True
        for dx, dy, dz in CUBES_NEIGHBORS:
            neighbor = x + dx, y + dy, z + dz
            if neighbor not in visited_set and neighbor not in cubes:
                visited_set.add(neighbor)
                open_list.append(neighbor)
    return False


with open("input.txt") as input:
    cubes = {(*map(int, line.split(",")),) for line in input.read().splitlines()}
    trapped_air = set()
    unconnected_sides = 0
    xmin, xmax = sys.maxsize, -sys.maxsize
    ymin, ymax = sys.maxsize, -sys.maxsize
    zmin, zmax = sys.maxsize, -sys.maxsize

    for x, y, z in cubes:
        xmin, xmax = min(xmin, x), max(xmax, x)
        ymin, ymax = min(ymin, y), max(ymax, y)
        zmin, zmax = min(zmin, z), max(zmax, z)
    for cube in product(
        range(xmin, xmax + 1), range(ymin, ymax + 1), range(zmin, zmax + 1)
    ):
        if not cube in cubes and not can_exit_box(
            cube, cubes, (xmin, xmax, ymin, ymax, zmin, zmax)
        ):
            trapped_air.add(cube)
    droplet = cubes | trapped_air
    for x, y, z in cubes:
        for dx, dy, dz in CUBES_NEIGHBORS:
            if (x + dx, y + dy, z + dz) not in droplet:
                unconnected_sides += 1
    print(unconnected_sides)
