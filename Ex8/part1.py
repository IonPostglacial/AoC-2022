from itertools import product


def get_obstacles(area, x, y):
    row_start = y * width
    h = row_start + x
    up = (area[x:h:width],)
    down = (area[h + width :: width],)
    left = (area[y * width : h],)
    right = (area[h + 1 : ((y + 1) * width)],)
    return up, down, left, right


def is_visible(area, width, x, y):
    up, down, left, right = get_obstacles(area, x, y)
    h = area[x + y * width]
    return h > max(up) or h > max(down) or h > max(left) or h > max(right)


with open("input.txt") as input:
    lines = input.read().splitlines()
    width = 0 if len(lines) == 0 else len(lines[0])
    height = len(lines)
    area = []
    for line in lines:
        for c in line:
            area.append(int(c))
    nb_visible = (width + height) * 2 - 4
    for y, x in product(range(1, height - 1), range(1, width - 1)):
        if is_visible(area, width, x, y):
            nb_visible += 1
    print(nb_visible)
