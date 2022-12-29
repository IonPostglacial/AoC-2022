from io import StringIO
import re

re_crates = re.compile(r"[A-Z]")
re_stacknum = re.compile(r"\d+")


def parse_create_stacks(input):
    in_crates = True
    stacks = []
    while in_crates:
        line = input.readline()
        crates = line[1::4]
        m = re_crates.findall(crates)
        in_crates = len(m) > 0
        if in_crates:
            if stacks is None:
                stacks = [[] for _ in range(len(crates))]
            for i, crate in enumerate(crates):
                if not crate.isspace():
                    stacks[i].append(crate)
    for stack in stacks:
        stack.reverse()
    return stacks


with open("input.txt", "r") as input:
    stacks = parse_create_stacks(input)
    while line := input.readline():
        m = re_stacknum.findall(line)
        if len(m) != 3:
            continue
        nb, start, end = map(int, m)
        for _ in range(nb):
            stacks[end - 1].append(stacks[start - 1].pop())
    res = StringIO()
    for stack in stacks:
        if len(stack) > 0:
            res.write(stack[-1])
    print(res.getvalue())
