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
    rope = [0j] * 10
    visited = set()
    for line in input.read().splitlines():
        d, s = line.split(" ")
        direction = directions[d]
        n = int(s)
        for _ in range(n):
            rope[0] += direction
            for i in range(1, len(rope)):
                rope[i] += tail_moved(rope[i], rope[i - 1])
            visited.add(rope[-1])
    print(len(visited))
