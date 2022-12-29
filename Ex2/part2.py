class Hand:
    rock = 1
    paper = 2
    scissors = 3


class Result:
    loss = 0
    draw = 3
    win = 6


def decode_hand(c: str):
    match c:
        case "A":
            return Hand.rock
        case "B":
            return Hand.paper
        case "C":
            return Hand.scissors
        case _:
            return 0


def decode_result(c):
    match c:
        case "X":
            return Result.loss
        case "Y":
            return Result.draw
        case "Z":
            return Result.win
        case _:
            return 0


def infer_hand(hand, expected_result):
    match hand, expected_result:
        case Hand.rock, Result.loss:
            return Hand.scissors
        case Hand.rock, Result.win:
            return Hand.paper
        case Hand.paper, Result.loss:
            return Hand.rock
        case Hand.paper, Result.win:
            return Hand.scissors
        case Hand.scissors, Result.loss:
            return Hand.paper
        case Hand.scissors, Result.win:
            return Hand.rock
        case _, Result.draw:
            return hand


with open("input.txt") as input:
    score = 0
    for (h, _, v, *_) in input.readlines():
        his, res = decode_hand(h), decode_result(v)
        mine = infer_hand(his, res)
        score += mine + res
    print(score)
