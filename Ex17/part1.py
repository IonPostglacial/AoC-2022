BLOCK_TYPES = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((0, 1), (1, 2), (1, 1), (1, 0), (2, 1)),
    ((0, 0), (1, 0), (2, 2), (2, 1), (2, 0)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (0, 1), (1, 0), (1, 1)),
]

X_MIN = 0
X_MAX = 7
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


class FallingBlockSimulator:
    def __init__(self):
        self.max_height = 0
        self.current_type = 0
        self.wind = 0
        self.stopped_rocks = set()
        self.rock_buffer = [(0, 0)] * 5
        self.falling_block = []

    def new_falling_block(self):
        block_type = BLOCK_TYPES[self.current_type]
        if self.current_type < len(BLOCK_TYPES) - 1:
            self.current_type += 1
        else:
            self.current_type = 0
        return [(x + X_START, y + DY_START + self.max_height) for (x, y) in block_type]

    def update_falling_block_from_buffer(self):
        for i in range(len(self.falling_block)):
            self.falling_block[i] = self.rock_buffer[i]

    def simulate_wind(self):
        wind_blow = wind_pattern[self.wind]
        if self.wind < len(wind_pattern) - 1:
            self.wind += 1
        else:
            self.wind = 0
        for i in range(len(self.falling_block)):
            x, y = self.falling_block[i]
            nx = x + wind_blow
            np = (nx, y)
            if nx not in range(X_MIN, X_MAX) or np in self.stopped_rocks:
                return
            self.rock_buffer[i] = (nx, y)
        self.update_falling_block_from_buffer()

    def simulate_gravity(self):
        for i in range(len(self.falling_block)):
            x, y = self.falling_block[i]
            ny = y - 1
            np = (x, ny)
            if ny < 0 or np in self.stopped_rocks:
                return False
            self.rock_buffer[i] = (x, ny)
        self.update_falling_block_from_buffer()
        return True

    def simulate_falling_block(self):
        self.falling_block = self.new_falling_block()
        while self.simulate_gravity():
            self.simulate_wind()
        for rock in self.falling_block:
            _, y = rock
            self.stopped_rocks.add(rock)
            self.max_height = max(self.max_height, y + 1)

    def display(self):
        print("-" * 40)
        for y in reversed(range(self.max_height + 5)):
            for x in range(X_MIN, X_MAX):
                p = (x, y)
                c = "."
                if p in self.stopped_rocks:
                    c = "#"
                elif p in self.falling_block:
                    c = "@"
                print(c, end="")
            print()


with open("input.txt") as input:
    wind_pattern = [parse_wind_blow(c) for c in input.readline().strip()]
    simulator = FallingBlockSimulator()
    for _ in range(2022):
        simulator.simulate_falling_block()
    print(simulator.max_height)
