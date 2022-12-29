import numpy as np
from dataclasses import dataclass
from collections import defaultdict

BLOCK_SHAPES = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((0, 1), (1, 2), (1, 1), (1, 0), (2, 1)),
    ((0, 0), (1, 0), (2, 2), (2, 1), (2, 0)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (0, 1), (1, 0), (1, 1)),
]

X_MIN = 0
ROOM_WIDTH = 7
X_START = 2
DY_START = 4


def parse_wind_blow(c: str) -> int:
    match c:
        case "<":
            return -1
        case ">":
            return 1
        case _:
            return 0


@dataclass(slots=True, frozen=True)
class Pattern:
    offset: int
    period: int
    height: int


@dataclass(slots=True, frozen=True)
class TrackerEntry:
    top: int
    height: int


class FallingBlockSimulator:
    def __init__(self, total_blocks_number, wind_pattern):
        self.total_blocks_number = total_blocks_number
        self.wind_pattern = wind_pattern
        self.max_height = 0
        self.max_heights = [0] * ROOM_WIDTH
        self.shape_index = 0
        self.wind_index = 0
        self.stopped_rocks = np.zeros(2000000000000, dtype=np.uint8)
        self.rock_buffer = [(0, 0)] * 5
        self.falling_block = []
        self.pattern: Pattern | None = None
        self.target_index = self.total_blocks_number
        self.tracker: defaultdict[int, list[TrackerEntry]] = defaultdict(list)

    def new_falling_block(self):
        block_type = BLOCK_SHAPES[self.shape_index]
        if self.shape_index < len(BLOCK_SHAPES) - 1:
            self.shape_index += 1
        else:
            self.shape_index = 0
        return [(x + X_START, y + DY_START + self.max_height) for (x, y) in block_type]

    def update_falling_block_from_buffer(self):
        for i in range(len(self.falling_block)):
            self.falling_block[i] = self.rock_buffer[i]

    def simulate_wind(self):
        wind_blow = self.wind_pattern[self.wind_index]
        if self.wind_index < len(self.wind_pattern) - 1:
            self.wind_index += 1
        else:
            self.wind_index = 0
        for i in range(len(self.falling_block)):
            x, y = self.falling_block[i]
            nx = x + wind_blow
            if (
                nx not in range(X_MIN, ROOM_WIDTH)
                or (self.stopped_rocks[y] & (1 << nx)) != 0
            ):
                return
            self.rock_buffer[i] = (nx, y)
        self.update_falling_block_from_buffer()

    def simulate_gravity(self):
        for i in range(len(self.falling_block)):
            x, y = self.falling_block[i]
            ny = y - 1
            if ny < 0 or (self.stopped_rocks[ny] & (1 << x)) != 0:
                return False
            self.rock_buffer[i] = (x, ny)
        self.update_falling_block_from_buffer()
        return True

    def simulate_falling_block(self, round):
        self.falling_block = self.new_falling_block()
        while self.simulate_gravity():
            self.simulate_wind()
        for rock in self.falling_block:
            x, y = rock
            self.stopped_rocks[y] |= 1 << x
            self.max_heights[x] = max(self.max_heights[x], y + 1)
        self.max_height = max(self.max_heights)
        x, y = self.falling_block[0]
        if round == self.target_index and self.pattern is not None:
            return False
        if round != 0:
            self.tracker[round] = [TrackerEntry(self.max_height, self.max_height)]
        for i in [i for i in self.tracker if round % i == 0]:
            height = self.max_height - self.tracker[i][-1].top
            self.tracker[i].append(TrackerEntry(self.max_height, height))
            if (
                len(self.tracker[i]) > 4
                and self.tracker[i][-1].height
                == self.tracker[i][-2].height
                == self.tracker[i][-3].height
                == self.tracker[i][-4].height
                == self.tracker[i][-5].height
            ):
                self.pattern = Pattern(
                    self.tracker[i][0].top, i, self.tracker[i][-1].height
                )
                print("pattern", self.pattern)
                self.tracker.clear()
                self.target_index = round + (
                    (self.total_blocks_number - 1) % self.pattern.period
                )
                return True
            elif (
                len(self.tracker[i]) > 4
                and self.tracker[i][-1].height != self.tracker[i][-2].height
            ):
                del self.tracker[i]
        return True

    def run(self):
        n = 0
        while self.simulate_falling_block(n):
            n += 1
        assert self.pattern is not None
        period, height, offset = (
            self.pattern.period,
            self.pattern.height,
            self.pattern.offset,
        )
        modulus = self.max_height - (offset + ((n // period) - 1) * height)
        return (
            offset + (((self.total_blocks_number - 1) // period) - 1) * height + modulus
        )

    def display(self, bottom=0, top=0):
        if top == 0:
            top = self.max_height + 5
        print("-" * 40)
        for y in reversed(range(bottom, top)):
            for x in range(X_MIN, ROOM_WIDTH):
                p = (x, y)
                c = "."
                if (self.stopped_rocks[y] & (1 << x)) != 0:
                    c = "#"
                elif p in self.falling_block:
                    c = "@"
                print(c, end="")
            print()


with open("input.txt") as input:
    wind_pattern = [parse_wind_blow(c) for c in input.readline().strip()]
    simulator = FallingBlockSimulator(1_000_000_000_000, wind_pattern)
    print(simulator.run())
