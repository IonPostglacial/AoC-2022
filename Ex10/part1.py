class Machine:
    def __init__(self):
        self.__clock = 0
        self.__probe = []
        self.x = 1

    def increment_clock(self):
        self.__clock += 1
        if self.__clock <= 220 and (self.__clock - 20) % 40 == 0:
            self.__probe.append(self.__clock * self.x)

    def noop(self):
        self.increment_clock()

    def addx(self, n: int):
        self.increment_clock()
        self.increment_clock()
        self.x += n

    def sum_signals(self):
        return sum(self.__probe)


with open("input.txt") as input:
    m = Machine()

    for line in input.read().splitlines():
        match line.split(" "):
            case ["noop"]:
                m.noop()
            case ["addx", txt]:
                m.addx(int(txt))
    print(m.sum_signals())
