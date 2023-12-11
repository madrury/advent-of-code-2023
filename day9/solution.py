from aocd import get_data
from dataclasses import dataclass
from typing import List, Dict, Iterable
from itertools import cycle
from math import lcm

class History:

    def __init__(self, history: List[int]):
        self.history: List[int] = history
        self.reduction = self.reduce(history)

    @staticmethod
    def reduce(history: List[int]) -> List[List[int]]:
        reduction = [history[:]]
        current = history[:]
        while any(x != 0 for x in current):
            current = [x - y for x, y in zip(current[1:], current[:-1])]
            reduction.append(current)
        return reduction

def parse_line(line: str) -> History:
    return History([int(x) for x in line.split(' ')])


if __name__ == '__main__':
    data: List[str] = [
        line.strip()
        for line in get_data(day=9, year=2023).split('\n')
    ]

    histories = [parse_line(line) for line in data]
    total = sum(r[-1] for h in histories for r in h.reduction)
    print(f"The total is {total}")

    totals = []
    for h in histories:
        initials = [r[0] for r in h.reduction]
        totals.append(sum(initials[::2]) - sum(initials[1::2]))
    print(f"The alternating total is {sum(totals)}")