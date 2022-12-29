import functools
import json


def compare(left: int | list, right: int | list) -> int:
    match left, right:
        case int(l), int(r):
            return l - r
        case list(ls), list(rs):
            for l, r in zip(ls, rs):
                cmp = compare(l, r)
                if cmp != 0:
                    return cmp
            return len(ls) - len(rs)
        case int(), list():
            return compare([left], right)
        case list(), int():
            return compare(left, [right])
    return 0


with open("input.txt") as input:
    lines = input.read().splitlines()
    sum_indices = 0
    sep1 = [[2]]
    sep2 = [[6]]
    packets = [sep1, sep2]
    for left_text, right_text in zip(lines[0::3], lines[1::3]):
        left = json.loads(left_text)
        right = json.loads(right_text)
        packets.append(left)
        packets.append(right)
    packets.sort(key=functools.cmp_to_key(compare))
    print((packets.index(sep1) + 1) * (packets.index(sep2) + 1))
