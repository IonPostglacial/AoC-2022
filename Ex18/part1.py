CUBES_NEIGHBORS = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)

with open("input.txt") as input:
    cubes = {(*map(int, line.split(",")),) for line in input.read().splitlines()}
    unconnected_sides = 0
    for x, y, z in cubes:
        for dx, dy, dz in CUBES_NEIGHBORS:
            if (x + dx, y + dy, z + dz) not in cubes:
                unconnected_sides += 1
    print(unconnected_sides)