import re
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import product
from typing import Optional

line_re = re.compile(
    r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
)


@dataclass(slots=True)
class Valve:
    id: int
    ref: str
    flow: int
    neighbors: list["Valve"]

    def __hash__(self) -> int:
        return self.id

@dataclass(slots=True)
class ClosedValveInfo:
    id: int
    flow: int

    def __lt__(self, other):
        return self.flow < other.flow

@dataclass(slots=True)
class Node:
    valves: tuple[Valve, Valve]
    remaining_time: int
    open_valves: tuple
    closed_valves: dict[int, int]
    pressure: int = 0
    previous: Optional["Node"] = None

    def get_id(self):
        return ((self.valves[0].id, self.valves[1].id), self.remaining_time, self.open_valves)

    def make_next_move(self, valves: tuple[Valve, Valve]):
        return Node(
            valves,
            remaining_time=self.remaining_time - 1,
            pressure=self.pressure,
            open_valves=self.open_valves,
            closed_valves=self.closed_valves,
            previous=self,
        )

    def make_next_open(self, valves: list[Valve]):
        next_remaining_time = self.remaining_time - 1
        closed_valves = self.closed_valves.copy()
        ids = set()
        next_pressure = self.pressure
        for valve in valves:
            if valve.id in ids:
                continue
            ids.add(valve.id)
            next_pressure += valve.flow * next_remaining_time
            del closed_valves[valve.id]
        return Node(
            self.valves,
            remaining_time=next_remaining_time,
            pressure=next_pressure,
            open_valves=tuple(
                (next_remaining_time if i in ids else self.open_valves[i])
                for i in range(len(self.open_valves))
            ),
            closed_valves=closed_valves,
            previous=self,
        )

    def heuristic(self):
        sum = self.pressure
        rem = self.remaining_time
        for flow in self.closed_valves.values():
            if rem <= 0:
                break
            rem -= 1
            sum += rem * flow
        return sum

    def explore_neighbors(self):
        neighbors_pairs = product(self.valves[0].neighbors, self.valves[1].neighbors)
        yield from (self.make_next_move(n) for n in neighbors_pairs)
        valve_hum, valve_el = self.valves
        for valves in ([valve_hum], [valve_el], [valve_hum, valve_el]):
            if all(self.open_valves[valve.id] is None and valve.flow > 0 for valve in valves):
                yield self.make_next_open(valves)

    def __lt__(self, other):
        return self.heuristic() > other.heuristic()


def _reconstruct_path(goal: Node):
    path = []
    currentNode = goal

    while currentNode is not None:
        path.append(currentNode)
        currentNode = currentNode.previous
    return reversed(path)

class GraphExporer:
    def __init__(self, valves: list[Valve]):
        self.valves = valves
        ordered_valves = [ClosedValveInfo(v.id, v.flow) for v in valves]
        ordered_valves.sort(reverse=True)
        self.ordered_valves: dict[int, int] = {}
        for v in ordered_valves:
            if v.flow > 0:
                self.ordered_valves[v.id] = v.flow

    def best_path(self, start: Valve, remaining_time):
        open_list: list[Node] = []
        closed_list: dict[tuple[tuple[int, int], int, tuple], Node] = {}
        open_valves = (None,) * len(self.valves)
        heappush(
            open_list, Node((start, start), remaining_time=remaining_time, open_valves=open_valves, closed_valves=self.ordered_valves)
        )

        while len(open_list) > 0:
            node = heappop(open_list)

            if node.remaining_time == 0:
                return _reconstruct_path(node)
            for neighbor in node.explore_neighbors():
                id = neighbor.get_id()
                old_node = closed_list.get(id)
                if old_node is None or neighbor.pressure > old_node.pressure:
                    closed_list[id] = neighbor
                    heappush(open_list, neighbor)
        return []


def parse(filename: str):
    with open(filename) as input:
        valve_info_by_ref = {}
        graph = []
        for id, line in enumerate(input.read().splitlines()):
            m = line_re.findall(line)
            assert len(m) == 1
            valve_ref, flow_txt, valves_txt = m[0]
            flow = int(flow_txt)
            valve = Valve(id, valve_ref, flow, [])
            graph.append(valve)
            valve_info_by_ref[valve_ref] = {
                "valve": valve,
                "neighbors_refs": valves_txt.split(", "),
            }
        for valve in graph:
            valve.neighbors = [
                valve_info_by_ref[ref]["valve"]
                for ref in valve_info_by_ref[valve.ref]["neighbors_refs"]
            ]
    return valve_info_by_ref["AA"]["valve"], graph


starting_valve, valves = parse("input.txt")
xp = GraphExporer(valves)
path = xp.best_path(starting_valve, 26)
for i, step in enumerate(path):
    open_valves = ", ".join(valves[id].ref for id in step.open_valves if id is not None)
    print("=" * 40)
    print("minute:", i)
    print("valves:", [valve.ref for valve in step.valves])
    print("open valves:", open_valves)
    print("pressure:", step.pressure)
