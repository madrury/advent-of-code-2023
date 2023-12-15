from aocd import get_data
from dataclasses import dataclass
from typing import List, Self, Tuple, Iterator

OPERATIONAL = "."
DAMAGED = "#"
UNKNOWN = "?"
TERMINATOR = "X"

ConditionRecord = List[str]
ContiguousRecord = List[int]
ConditionPtr = int

@dataclass
class StackEntry:
    condition: ConditionRecord
    contiguous: ContiguousRecord
    ptr: ConditionPtr

    def copy(self) -> Self:
        return StackEntry(self.condition[:], self.contiguous[:], self.ptr)

    def increment(self) -> Self:
        self.ptr += 1
        return self

    def set(self, chr: str) -> Self:
        self.condition[self.ptr] = chr
        if chr == DAMAGED and self.condition[self.ptr - 1] == DAMAGED:
            self.contiguous[-1] += 1
        if chr == DAMAGED and self.condition[self.ptr - 1] == OPERATIONAL:
            self.contiguous.append(1)
        if chr == DAMAGED and self.condition[self.ptr - 1] == TERMINATOR:
            self.contiguous.append(1)
        return self

    def finish(self) -> Self:
        for i, chr in enumerate(self.condition):
            if chr == UNKNOWN:
                self.condition[i] = OPERATIONAL
        return self


def parse_line(line: str, expand: bool = False) -> Tuple[ConditionRecord, ContiguousRecord]:
    conditionstr, contigstr = line.strip().split(' ')
    if expand:
        conditionstr = '?'.join([conditionstr]*5)
        contigstr = ','.join([contigstr]*5)
    condition = list(conditionstr)
    contiguous = [int(n) for n in contigstr.split(',')]
    return condition, contiguous


class Solver:

    def __init__(self, condition: ConditionRecord, contiguous: ContiguousRecord):
        self.condition = [TERMINATOR] + condition + [TERMINATOR]
        self.target = contiguous
        self.solutions: List[ConditionRecord] = []
        # Setup the initial stack.
        initial_condition = [TERMINATOR] + [UNKNOWN]*len(condition) + [TERMINATOR]
        initial_contiguous = []
        self.stack: List[StackEntry] = [
            StackEntry(initial_condition, initial_contiguous, 1)
        ]

    def solve(self) -> Self:
        while self.stack:
            entry = self.stack.pop()
            if self.is_finished(entry):
                if entry.contiguous == self.target:
                    self.solutions.append(entry.finish().condition)
                continue
            if self.is_hopeless(entry):
                continue
            # Push next states onto the stack.
            for next in self.propose(entry):
                self.stack.append(next)
        return self

    def is_finished(self, entry: StackEntry) -> bool:
        return entry.condition[entry.ptr] == TERMINATOR

    def is_hopeless(self, entry: StackEntry) -> bool:
        if len(entry.contiguous) > len(self.target):
            return True
        if not all(c == t for c, t in zip(entry.contiguous[:-1], self.target[:-1])):
            return True
        for c, t in zip(entry.contiguous, self.target):
            if c > t:
                return True
        return False

    def propose(self, entry: StackEntry) -> Iterator[StackEntry]:
        if self.condition[entry.ptr] in TERMINATOR:
            return
        elif self.condition[entry.ptr] in {DAMAGED, OPERATIONAL}:
            yield entry.copy().set(self.condition[entry.ptr]).increment()
        elif self.condition[entry.ptr] == UNKNOWN:
            yield entry.copy().set(DAMAGED).increment()
            yield entry.copy().set(OPERATIONAL).increment()




if __name__ == '__main__':
    datastr = (
"""
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
    )
    data: List[str] = [
        line.strip()
        for line in get_data(day=12, year=2023).split('\n')
    ]

    solvers: List[Solver] = []
    for condition, contiguous in (parse_line(l, expand=False) for l in data):
        s = Solver(condition, contiguous).solve()
        print(f"Solved, with {len(s.solutions)} solutions.")
        solvers.append(s)
    total = sum(len(s.solutions) for s in solvers)
    print(f"There are {total} total solutions")