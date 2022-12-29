import re

points_re = re.compile(r"(\d+),(\d+)")


class CellType:
    air = "."
    rock = "#"
    sand = "o"


class Grid:
    def __init__(self, top=0, bottom=0, left=500, right=500):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self._cells = []

    def fill_cells(self):
        self._cells = [
            [CellType.air for _ in range(self.left, self.right + 1)]
            for _ in range(self.top, self.bottom + 1)
        ]

    def cell_type(self, x, y):
        if self.contains(x, y):
            return self._cells[y][x - self.left]
        else:
            return CellType.air

    def set_cell_type(self, x, y, type):
        self._cells[y][x - self.left] = type

    def contains(self, x, y):
        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def display(self):
        for line in self._cells:
            for cell in line:
                print(cell, end="")
            print()


with open("input.txt") as input:
    segments: list[tuple[int, int]] = []
    grid = Grid()
    for line in input.read().splitlines():
        points = [(int(x), int(y)) for x, y in points_re.findall(line)]
        for x, y in points:
            grid.bottom = max(grid.bottom, y)
            grid.left = min(grid.left, x)
            grid.right = max(grid.right, x)
        for (x1, y1), (x2, y2) in zip(points[0:], points[1:]):
            if x1 == x2:
                segments += [(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)]
            else:
                segments += [(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)]
    grid.fill_cells()
    for x, y in segments:
        grid.set_cell_type(x, y, CellType.rock)
    sand_units = 0
    sx, sy = 500, 0
    while grid.contains(sx, sy):
        while grid.cell_type(sx, sy + 1) == CellType.air and sy <= grid.bottom:
            sy += 1
        ny = sy + 1
        lx = sx - 1
        rx = sx + 1
        if grid.cell_type(lx, ny) == CellType.air:
            sx, sy = lx, ny
        elif grid.cell_type(rx, ny) == CellType.air:
            sx, sy = rx, ny - 1
        else:
            grid.set_cell_type(sx, sy, CellType.sand)
            sx, sy = 500, 0
            sand_units += 1
    print(sand_units)
