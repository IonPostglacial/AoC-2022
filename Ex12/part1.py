from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional


@dataclass
class Node:
    step: tuple[int, int]
    heuristic: int
    cost: int
    previous: Optional["Node"] = None

    @property
    def score(self):
        return self.cost + self.heuristic

    def __lt__(self, other):
        return other is None or self.score < other.score


class Grid:
    width: int
    height: int
    start: tuple[int, int]
    end: tuple[int, int]
    _cells: list[list[int]]

    def __init__(self, input: list[str]):
        self.height = len(input)
        self.width = len(input[0]) if len(input) > 0 else 0
        self._cells = []
        for y, line in enumerate(input):
            l = []
            for x, c in enumerate(line):
                match c:
                    case "S":
                        self.start = x, y
                        l.append(0)
                    case "E":
                        self.end = x, y
                        l.append(25)
                    case _:
                        l.append(ord(c) - ord("a"))
            self._cells.append(l)

    def distance_between(self, start, end) -> int:
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def is_traversable(self, px: int, py: int, x: int, y: int):
        in_bounds = x >= 0 and x < self.width and y >= 0 and y < self.height
        if in_bounds:
            prev_h = self._cells[py][px]
            h = self._cells[y][x]
            return (h - prev_h) <= 1
        else:
            return False

    def get_neighbors(self, step: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = step
        neighbors = []
        if self.is_traversable(x, y, x, y - 1):
            neighbors.append((x, y - 1))
        if self.is_traversable(x, y, x, y + 1):
            neighbors.append((x, y + 1))
        if self.is_traversable(x, y, x - 1, y):
            neighbors.append((x - 1, y))
        if self.is_traversable(x, y, x + 1, y):
            neighbors.append((x + 1, y))
        return neighbors


def _reconstruct_path(start, goal: Node):
    path = []
    currentNode = goal

    while currentNode is not None and currentNode.step != start:
        if currentNode is not None:
            path.append(currentNode.step)
            currentNode = currentNode.previous
        else:
            return []
    return path


def path_between(grid: Grid, start, end):
    closed_list = {}
    open_list = []
    h = grid.distance_between(start, end)
    heappush(open_list, Node(start, h, 0))

    while len(open_list) > 0:
        node = heappop(open_list)

        if node.step == end:
            return _reconstruct_path(start, node)
        for neighbor in grid.get_neighbors(node.step):
            heuristic = grid.distance_between(neighbor, end)
            cost = node.cost + 1
            new_node = Node(neighbor, heuristic, cost, node)
            old_node = closed_list.get(neighbor)
            if old_node is None or new_node.score < old_node.score:
                closed_list[neighbor] = new_node
                heappush(open_list, new_node)
    return []


with open("input.txt") as input:
    grid = Grid(input.read().splitlines())
    path = path_between(grid, grid.start, grid.end)
    print(len(path))
