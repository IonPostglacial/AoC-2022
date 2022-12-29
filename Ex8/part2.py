from functools import partial
from itertools import product


def get_obstacles(area, x, y):
    row_start = y * width
    h = row_start + x
    up = area[x:h:width][::-1]
    down = area[h + width :: width]
    left = area[y * width : h][::-1]
    right = area[h + 1 : ((y + 1) * width)]
    return up, down, left, right


def viewing_distance(h, heights):
    d = 0
    for height in heights:
        d += 1
        if height >= h:
            break
    return d


def scenic_score(area, h, x, y):
    dirs = get_obstacles(area, x, y)
    d_up, d_down, d_left, d_right = map(partial(viewing_distance, h), dirs)
    return d_up * d_down * d_left * d_right


with open("input.txt") as input:
    lines = input.read().splitlines()
    width = 0 if len(lines) == 0 else len(lines[0])
    height = len(lines)
    area = []
    for line in lines:
        for c in line:
            area.append(int(c))
    max_score = 0
    for i, (y, x) in enumerate(product(range(0, height), range(0, width))):
        max_score = max(max_score, scenic_score(area, area[i], x, y))
    print(max_score)
