from aocd import get_data
from enum import Enum
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List, Tuple, List, Set, Iterable

N_ROW, N_COL = 141, 141

Coordinate = Tuple[int, int]
Map = List[str]

class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

    def __getitem__(self, idx) -> int:
        return self.value[idx]


OPPOSITE_DIRECTION = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST
}

@dataclass(frozen=True)
class Node:
    coordinate: Coordinate
    direction: Direction
    times: int

    def nexts(self) -> Iterable["Node"]:
        c, d, t = self.coordinate, self.direction, self.times
        for nd in Direction:
            if nd == OPPOSITE_DIRECTION[d]:
                continue
            elif nd == d:
                if t < 3:
                    yield Node((c[0] + nd[0], c[1] + nd[1]), nd, t + 1)
            else:
                yield Node((c[0] + nd[0], c[1] + nd[1]), nd, 1)

    def ultranexts(self) -> Iterable["Node"]:
        c, d, t = self.coordinate, self.direction, self.times
        if t < 4:
            yield Node((c[0] + d[0], c[1] + d[1]), d, t + 1)
            return
        for nd in Direction:
            if nd == OPPOSITE_DIRECTION[d]:
                continue
            elif nd == d:
                if t < 10:
                    yield Node((c[0] + nd[0], c[1] + nd[1]), nd, t + 1)
            else:
                yield Node((c[0] + nd[0], c[1] + nd[1]), nd, 1)

    @property
    def in_bounds(self):
        return (
            (0 <= self.coordinate[0] < N_ROW)
            and (0 <= self.coordinate[1] < N_COL)
        )


@dataclass(order=True)
class SearchStep:
    node: Node = field(compare=False)
    loss: int


class Solver:

    def __init__(self, map: Map):
        self.map = map
        self.queue: PriorityQueue[SearchStep] = PriorityQueue()
        self.seen: Set[Node] = set()

    def solve(self, start: Node, end: Coordinate):
        self.queue.put(SearchStep(start, 0))
        current: SearchStep = None
        while True:
            current = self.queue.get()
            node = current.node
            if node in self.seen or not node.in_bounds:
                continue
            self.seen.add(node)
            c = node.coordinate
            if c == end and node.times >= 4:
                return current.loss + int(map[c[0]][c[1]])
            for nxt in node.ultranexts():
                self.queue.put(
                    SearchStep(nxt, current.loss + int(map[c[0]][c[1]]))
                )


if __name__ == '__main__':
    map: Map = get_data(day=17, year=2023).split('\n')

    s = Solver(map)
    loss = s.solve(
        Node((0, 0), Direction.NORTH, 10),
        (N_ROW - 1, N_COL - 1)
    )
    print(f"The minimum loss is {loss - int(map[0][0])}")