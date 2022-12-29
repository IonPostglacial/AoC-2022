import re

sensor_re = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)
ry = 2000000

with open("input.txt") as input:
    excluded = set()
    for line in input.read().splitlines():
        m = sensor_re.findall(line)
        assert len(m) > 0
        sx, sy, bx, by = map(int, m[0])
        d = abs(sx - bx) + abs(sy - by)
        dy = abs(sy - ry)
        dx = d - dy
        excluded |= set(range(sx - dx, sx + dx))
    print(len(excluded))
