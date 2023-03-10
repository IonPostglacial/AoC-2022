import re
from dataclasses import dataclass
from heapq import heappop, heappush
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
    valve: Valve
    remaining_time: int
    open_valves: tuple
    closed_valves: dict[int, int]
    pressure: int = 0
    previous: Optional["Node"] = None

    def get_id(self):
        return (self.valve.id, self.remaining_time, self.open_valves)

    def make_next_move(self, valve: Valve):
        return Node(
            valve,
            remaining_time=self.remaining_time - 1,
            pressure=self.pressure,
            open_valves=self.open_valves,
            closed_valves=self.closed_valves,
            previous=self,
        )

    def make_next_open(self):
        next_remaining_time = self.remaining_time - 1
        closed_valves = self.closed_valves.copy()
        del closed_valves[self.valve.id]
        return Node(
            self.valve,
            remaining_time=next_remaining_time,
            pressure=self.pressure + self.valve.flow * next_remaining_time,
            open_valves=tuple(
                (next_remaining_time if i == self.valve.id else self.open_valves[i])
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
        yield from (self.make_next_move(n) for n in self.valve.neighbors)
        if self.open_valves[self.valve.id] is None and self.valve.flow > 0:
            yield self.make_next_open()

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

    def nest_path(self, start: Valve, remaining_time):
        open_list: list[Node] = []
        closed_list: dict[tuple[int, int, tuple], Node] = {}
        open_valves = (None,) * len(self.valves)
        heappush(
            open_list, Node(start, remaining_time=remaining_time, open_valves=open_valves, closed_valves=self.ordered_valves)
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
path = xp.nest_path(starting_valve, 30)
for i, step in enumerate(path):
    open_valves = ", ".join(valves[id].ref for id in step.open_valves if id is not None)
    print("=" * 40)
    print("minute:", i)
    print("valve:", step.valve.ref)
    print("open valves:", open_valves)
    print("pressure:", step.pressure)
