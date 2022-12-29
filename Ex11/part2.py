import re
from collections import deque
from dataclasses import dataclass, field
from math import lcm

re_monkey = re.compile(r"Monkey\s+(\d+)")
re_start = re.compile(r"Starting items:\s+(.*)")
re_op = re.compile(r"Operation:\s+new\s+=\s+old\s+([*+/-])\s+(\d+|old)")
re_test = re.compile(r"Test: divisible by (\d+)")
re_throw = re.compile(r"If (true|false): throw to monkey (\d+)")


@dataclass
class Monkey:
    items: deque[int] = field(default_factory=deque)
    operator: str = ""
    operand: str = ""
    test_divisible: int = 0
    throw_on_true: int = 0
    throw_on_false: int = 0
    nb_inspected_items: int = 0


def operate(x: int, operator: str, operand: str) -> int:
    y = x if operand == "old" else int(operand)
    match operator:
        case "*":
            return x * y
        case "+":
            return x + y
        case "/":
            return x // y
        case "-":
            return x - y
    return 0


def turn(limit: int, monkeys: list[Monkey], monkey: Monkey):
    while len(monkey.items) > 0:
        monkey.nb_inspected_items += 1
        worry_lvl = monkey.items.popleft()
        worry_lvl = operate(worry_lvl, monkey.operator, monkey.operand)
        worry_lvl %= limit
        if worry_lvl % monkey.test_divisible == 0:
            monkeys[monkey.throw_on_true].items.append(worry_lvl)
        else:
            monkeys[monkey.throw_on_false].items.append(worry_lvl)


def round(limit: int, monkeys: list[Monkey]):
    for monkey in monkeys:
        turn(limit, monkeys, monkey)


with open("input.txt") as input:
    monkeys = []
    current_monkey = Monkey()
    for line in input.read().splitlines():
        m = re_monkey.findall(line)
        if len(m) > 0:
            current_monkey = Monkey()
            monkeys.append(current_monkey)
            continue
        start = re_start.findall(line)
        if len(start) > 0:
            current_monkey.items = deque(map(int, start[0].split(", ")))
            continue
        op = re_op.findall(line)
        if len(op) > 0:
            current_monkey.operator = op[0][0]
            current_monkey.operand = op[0][1]
            continue
        test = re_test.findall(line)
        if len(test) > 0:
            current_monkey.test_divisible = int(test[0])
        throw = re_throw.findall(line)
        if len(throw) > 0:
            cond, monkey = throw[0]
            match cond:
                case "true":
                    current_monkey.throw_on_true = int(monkey)
                case "false":
                    current_monkey.throw_on_false = int(monkey)
            continue
    limit = lcm(*map(lambda m: m.test_divisible, monkeys))
    for _ in range(10_000):
        round(limit, monkeys)
    monkey_scores = list(sorted(list(map(lambda m: m.nb_inspected_items, monkeys))))
    monkey_scores.sort(reverse=True)
    m1, m2 = monkey_scores[:2]
    print(m1 * m2)
