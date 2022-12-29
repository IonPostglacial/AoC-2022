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
    for i, (left_text, right_text) in enumerate(zip(lines[0::3], lines[1::3])):
        left = json.loads(left_text)
        right = json.loads(right_text)
        if compare(left, right) < 0:
            sum_indices += i + 1
    print(sum_indices)
