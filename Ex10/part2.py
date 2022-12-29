def draw_pixel(state):
    if state:
        return "#"
    else:
        return "."


class Machine:
    def __init__(self):
        self.__clock = 0
        self.__buffer = [False for _ in range(50)]
        self.__buffer[1] = True
        self.__buffer[2] = True
        self.__screen = [False for _ in range(40 * 6)]
        self.x = 1
        self.draw_sprite(self.x, True)

    def increment_clock(self):
        self.__clock += 1
        pos = self.__clock - 1
        self.__screen[pos] = self.__buffer[pos % 40]

    def noop(self):
        self.increment_clock()

    def draw_sprite(self, x: int, lit: bool):
        self.__buffer[x - 1] = lit
        self.__buffer[x] = lit
        self.__buffer[x + 1] = lit

    def addx(self, n: int):
        self.increment_clock()
        self.increment_clock()
        self.draw_sprite(self.x, False)
        self.x += n
        self.draw_sprite(self.x, True)

    def print_screen(self):
        screen = list(map(draw_pixel, self.__screen))
        for row in range(6):
            print("".join(screen[row * 40 : (row + 1) * 40]))


with open("input.txt") as input:
    m = Machine()
    for line in input.read().splitlines():
        match line.split(" "):
            case ["noop"]:
                m.noop()
            case ["addx", txt]:
                m.addx(int(txt))
    m.print_screen()
