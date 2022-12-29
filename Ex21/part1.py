from enum import Enum
from dataclasses import dataclass

class Operator(Enum):
    plus = 0
    minus = 1
    mul = 2
    div = 3

@dataclass
class Expression:
    operator: Operator
    left: str
    right: str

def eval(monkeys: dict[str, Expression|int], e: Expression|int) -> int:
    match e:
        case int(n):
            return n
        case Expression(op, l, r):
            left = eval(monkeys, monkeys[l])
            right = eval(monkeys, monkeys[r])
            match op:
                case Operator.plus:
                    return left + right
                case Operator.minus:
                    return left - right
                case Operator.mul:
                    return left * right
                case Operator.div:
                    return left // right
                case _:
                    raise Exception("invalid operator")
        case _:
            raise Exception("invalid expression")

lines = open("input.txt").read().strip().splitlines()
monkeys: dict[str, int|Expression] = {}
for line in lines:
    monkey, formula = line.split(": ")
    formula = formula.split(" ")
    match formula:
        case [num]:
            expr = int(num)
        case [left, op, right]:
            match op:
                case "+":
                    operator = Operator.plus
                case "-":
                    operator = Operator.minus
                case "*":
                    operator = Operator.mul
                case "/":
                    operator = Operator.div
                case _:
                    raise Exception("invalid operator:", op)
            expr = Expression(operator, left, right)
        case _:
            raise Exception("invalid input:", formula)
    monkeys[monkey] = expr
print(eval(monkeys, monkeys["root"]))