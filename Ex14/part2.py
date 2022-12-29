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
        self._cells = {}

    def cell_type(self, x, y):
        return self._cells.get((x, y), CellType.rock if y == self.bottom else CellType.air)

    def set_cell_type(self, x, y, type):
        self._cells[(x, y)] = type

    def fill_cells(self, type, cells):
        for cell in cells:
            self._cells[cell] = type

    def display(self):
        for y in range(self.top, self.bottom + 1):
            for x in range(self.left, self.right + 1):
                print(self.cell_type(x, y), end="")
            print()


with open("input.txt") as input:
    grid = Grid()
    for line in input.read().splitlines():
        points = [(int(x), int(y)) for x, y in points_re.findall(line)]
        for x, y in points:
            grid.bottom = max(grid.bottom, y)
            grid.left = min(grid.left, x)
            grid.right = max(grid.right, x)
        for (x1, y1), (x2, y2) in zip(points[0:], points[1:]):
            if x1 == x2:
                grid.fill_cells(CellType.rock, ((x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)))
            else:
                grid.fill_cells(CellType.rock, ((x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)))
    grid.bottom += 2
    sand_units = 0
    sx, sy = 500, 0
    unblocked = True
    while unblocked:
        while grid.cell_type(sx, sy + 1) == CellType.air:
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
            unblocked = sx != 500 or sy != 0
            sx, sy = 500, 0
            sand_units += 1
    print(sand_units)
