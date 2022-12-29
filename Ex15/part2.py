import re
import multirange as mr

sensor_re = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)
n_min = 0
n_max = 4_000_000
inclusion_range = range(n_min, n_max + 1)


with open("input.txt") as input:
    zones = []
    possible_points = set()
    for line in input.read().splitlines():
        m = sensor_re.findall(line)
        assert len(m) > 0
        sx, sy, bx, by = map(int, m[0])
        zones.append((sx, sy, abs(sx - bx) + abs(sy - by)))
    for ry in range(n_min, n_max + 1):
        excluded_ranges = []
        for sx, sy, d in zones:
            dy = abs(sy - ry)
            dx = d - dy
            if dx > 0:
                excluded_ranges.append(
                    range(max(n_min, sx - dx), min(n_max + 1, sx + dx))
                )
                excluded_ranges = list(mr.normalize_multi(excluded_ranges))
        included_ranges = mr.difference_one_multi(inclusion_range, excluded_ranges)
        for included_range in included_ranges:
            for x in included_range:
                possible_points.add((x, ry))
    candidates = possible_points.copy()
    for x, y in possible_points:
        for sx, sy, d in zones:
            dp = abs(sx - x) + abs(sy - y)
            if dp <= d:
                candidates.discard((x, y))
    assert len(candidates) == 1
    x, y = candidates.pop()
    tuning_freq = 4000000 * x + y
    print(tuning_freq)
