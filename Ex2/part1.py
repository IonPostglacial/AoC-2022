class Hand:
    rock = 1
    paper = 2
    scissors = 3


loss = 0
draw = 3
win = 6


def decode(c: str):
    match c:
        case "A" | "X":
            return Hand.rock
        case "B" | "Y":
            return Hand.paper
        case "C" | "Z":
            return Hand.scissors
        case _:
            return 0


def victory_score(mine, his):
    match mine, his:
        case Hand.rock, Hand.paper:
            return loss
        case Hand.rock, Hand.scissors:
            return win
        case Hand.paper, Hand.rock:
            return win
        case Hand.paper, Hand.scissors:
            return loss
        case Hand.scissors, Hand.rock:
            return loss
        case Hand.scissors, Hand.paper:
            return win
        case _:
            return draw


with open("input.txt") as input:
    score = 0
    for (h, _, m, *_) in input.readlines():
        mine, his = decode(m), decode(h)
        score += mine + victory_score(mine, his)
    print(score)
