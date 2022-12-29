from dataclasses import dataclass


class Operator:
    SET = {"+": "-", "-": "+", "*": "/", "/": "*", "=": "="}
    add, sub, mul, div, eql = SET.keys()

    @staticmethod
    def rev(op: str):
        return Operator.SET[op]


@dataclass(slots=True, frozen=True)
class Operation:
    operator: str
    left: "Expression"
    right: "Expression"


Expression = Operation | str | int


def eval_expr(e: Expression) -> Expression:
    match e:
        case int() | str():
            return e
        case Operation(op, l, r):
            left = eval_expr(l)
            right = eval_expr(r)
            match op, left, right:
                case Operator.add, int(n), int(m):
                    return n + m
                case Operator.sub, int(n), int(m):
                    return n - m
                case Operator.mul, int(n), int(m):
                    return n * m
                case Operator.div, int(n), int(m):
                    return n // m
                case _:
                    return Operation(op, left, right)
        case _:
            raise Exception("invalid expression")


def each_pre_exprs(monkeys: dict[str, int | dict], name: str):
    pre_expr = monkeys[name]
    match pre_expr:
        case int(n):
            yield name, n
        case {"op": op, "left": left, "right": right}:
            yield from each_pre_exprs(monkeys, left)
            yield from each_pre_exprs(monkeys, right)
            yield name, pre_expr


def path_to_unknown(expr: Expression, path: list[Expression]):
    match expr:
        case int():
            return []
        case str():
            return [*path, expr]
        case Operation(_, left, right):
            path = [*path, expr]
            return path_to_unknown(left, path) + path_to_unknown(right, path)
        case _:
            raise Exception("Unknown expression")


def solve_equation(expr: Expression):
    assert isinstance(expr, Operation) and expr.operator == Operator.eql
    expr = eval_expr(expr)
    assert isinstance(expr, Operation)
    path = path_to_unknown(expr, [])
    solution = expr.left if path[1] != expr.left else expr.right
    for expr, next in zip(path[1:], path[2:]):
        match expr:
            case Operation(op, left, right):
                if left != next:
                    if op == "-":
                        solution = Operation("-", 0, solution)
                    elif op == "/":
                        solution = Operation("/", 1, solution)
                    solution = Operation(Operator.rev(op), solution, left)
                else:
                    solution = Operation(Operator.rev(op), solution, right)
            case str():
                return solution
            case _:
                raise Exception("Cannot simplify expression", expr)
    return eval_expr(solution)


def parse_input(lines: list[str]):
    monkeys: dict[str, int | dict] = {}
    for line in lines:
        monkey, formula = line.split(": ")
        formula = formula.split(" ")
        match formula:
            case [num]:
                expr = int(num)
            case [left, op, right]:
                if op not in Operator.SET:
                    raise Exception("invalid operator:", op)
                expr = {"op": op, "left": left, "right": right}
            case _:
                raise Exception("invalid input:", formula)
        monkeys[monkey] = expr

    monkeys_exprs: dict[str, Expression] = {}

    for name, expr in each_pre_exprs(monkeys, "root"):
        match name, expr:
            case "humn", _:
                ex = "humn"
            case _, int(n):
                ex = n
            case _, {"op": operator, "left": left, "right": right}:
                ex = Operation(
                    Operator.eql if name == "root" else operator,
                    monkeys_exprs[left],
                    monkeys_exprs[right],
                )
            case _:
                raise Exception("wtf", expr)
        monkeys_exprs[name] = ex
    return monkeys_exprs["root"]


root = parse_input(open("input.txt").read().strip().splitlines())
print(solve_equation(root))
