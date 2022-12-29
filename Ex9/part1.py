from math import copysign

directions = {
    "U": 0 - 1j,
    "D": 0 + 1j,
    "L": -1 + 0,
    "R": 1 + 0,
}


def normalize(n: int):
    return copysign(min(1, abs(n)), n)


def tail_moved(tail, head):
    d = head - tail
    if max(abs(d.real), abs(d.imag)) <= 1:
        return 0j
    else:
        return normalize(d.real) + normalize(d.imag) * 1j


with open("input.txt") as input:
    h, t = 0j, 0j
    visited = set()
    for line in input.read().splitlines():
        d, s = line.split(" ")
        direction = directions[d]
        n = int(s)
        for _ in range(n):
            h = h + direction
            t = t + tail_moved(t, h)
            visited.add(t)
    print(len(visited))
