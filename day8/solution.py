from aocd import get_data
from dataclasses import dataclass
from typing import List, Dict, Iterable
from itertools import cycle
from math import lcm

@dataclass(frozen=True)
class Node:
    name: str
    children: (str, str)

    def __hash__(self):
        return hash(self.name)

NodeTable = Dict[str, Node]

def parse_node_line(line: str) -> Node:
    namestr, tuplestr = line.split(' = ')
    leftstr, rightstr = tuplestr[1:-1].split(', ')
    return Node(namestr.strip(), (leftstr.strip(), rightstr.strip()))

def walk(frm: str, to: str, instructions: Iterable[str], tbl: NodeTable) -> int:
    DIRECTION_TO_IDX = {'L': 0, 'R': 1}
    current = tbl[frm]
    for i, direction in enumerate(instructions, start=1):
        current = tbl[current.children[DIRECTION_TO_IDX[direction]]]
        if current.name == to:
            break
    return i

def walktill(frm: str, instructions: Iterable[str], tbl: NodeTable) -> int:
    DIRECTION_TO_IDX = {'L': 0, 'R': 1}
    current = tbl[frm]
    for i, direction in enumerate(instructions, start=1):
        current = tbl[current.children[DIRECTION_TO_IDX[direction]]]
        if current.name.endswith('Z'):
            break
    return i


if __name__ == '__main__':
    data: List[str] = [
        line.strip()
        for line in get_data(day=8, year=2023).split('\n')
    ]

    nodes = [parse_node_line(line) for line in data[2:]]
    nodetable: NodeTable = {n.name: n for n in nodes}

    instructions = cycle(data[0])
    steps = walk('AAA', 'ZZZ', instructions, nodetable)
    print(f"It takes {steps} steps to get from AAA to ZZZ")

    starts = [n.name for n in nodes if n.name.endswith('A')]
    stepcounts: List[int] = []
    for start in starts:
        instructions = cycle(data[0])
        stepcounts.append(walktill(start, instructions, nodetable))

    print(f"It takes {lcm(*stepcounts)} to Z it all out.")
