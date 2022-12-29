import re
from dataclasses import dataclass

line_re = re.compile(
    r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
)


@dataclass(slots=True)
class Valve:
    id: int
    ref: str
    flow: int
    neighbors: list["Valve"]


@dataclass(slots=True, frozen=True)
class SolutionId:
    valve: int
    remaining_time: int
    open_valves: tuple


class GraphExplorer:
    def __init__(self, graph: list[Valve]):
        n = 0
        for valve in graph:
            if valve.flow > 0:
                n += 1
        self._nb_valves_to_open = n
        self.graph = graph
        self._cache: dict[SolutionId, int] = {}

    def cache(self, solution_id: SolutionId, result: int) -> int:
        self._cache[solution_id] = result
        return result

    def best_pressure(
        self, start: Valve, timeout: int, open_valves: tuple, nb_open=0, pressure=0
    ):
        sol_id = SolutionId(start.id, timeout, open_valves)
        if timeout == 0 or nb_open >= self._nb_valves_to_open:
            return pressure
        if sol_id in self._cache:
            return self._cache[sol_id]
        next_remaining_time = timeout - 1
        best = max(
            self.best_pressure(
                neighbor, next_remaining_time, open_valves, nb_open, pressure
            )
            for neighbor in start.neighbors
        )
        if start.flow > 0 and open_valves[start.id] is None:
            best = max(
                best,
                self.best_pressure(
                    start,
                    next_remaining_time,
                    tuple(
                        (next_remaining_time if i == start.id else open_valves[i])
                        for i in range(len(open_valves))
                    ),
                    nb_open + 1,
                    pressure + next_remaining_time * start.flow,
                ),
            )
        return self.cache(sol_id, best)


def parse(filename: str):
    with open(filename) as input:
        valve_info_by_ref = {}
        graph = []
        nb_to_open = 0
        for id, line in enumerate(input.read().splitlines()):
            m = line_re.findall(line)
            assert len(m) == 1
            valve_ref, flow_txt, valves_txt = m[0]
            flow = int(flow_txt)
            if flow > 0:
                nb_to_open += 1
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
explorer = GraphExplorer(valves)
max_pressure = explorer.best_pressure(starting_valve, 30, (None,) * len(valves))
print(max_pressure)
