from aocd import get_data
from dataclasses import dataclass
from typing import List, Tuple, List, Iterator, Dict

Tag = str
Part = Dict[str, int]
Space = Dict[str, range]

def intersect(r0: range, r1: range) -> range | None:
    if r0.start > r1.start:
        r0, r1 = r1, r0
    if r0.stop <= r1.start:
        return None
    return range(max(r0.start, r1.start), min(r0.stop, r1.stop))


class Instruction:
    def execute(self, part: Part):
        return self

@dataclass
class Redirect(Instruction):
    tag: Tag

@dataclass
class Accept(Instruction):
    pass
# Singleton object.
ACCEPT = Accept()

@dataclass
class Reject(Instruction):
    pass
# Singlgeton Object.
REJECT = Reject()

@dataclass
class Next(Instruction):
    pass
# Singlgeton Object.
NEXT = Next()

LOOKUP = {'A': ACCEPT, 'R': REJECT}

@dataclass
class Conditional(Instruction):
    variable: str
    inequality: str
    comparator: int
    outcome: Redirect | Accept | Reject

    def subset(self, space: Space) -> Space:
        r = space[self.variable]
        space = {k: v for k, v in space.items() if k != self.variable}
        if self.inequality == '<':
            crange = range(1, self.comparator)
            space[self.variable] = intersect(r, crange)
        if self.inequality == '>':
            crange = range(self.comparator + 1, 4001)
            space[self.variable] = intersect(r, crange)
        return space

    def complement(self, space: Space) -> Space:
        r = space[self.variable]
        space = {k: v for k, v in space.items() if k != self.variable}
        # >=
        if self.inequality == '<':
            crange = range(self.comparator, 4001)
            space[self.variable] = intersect(r, crange)
        # <=
        if self.inequality == '>':
            crange = range(1, self.comparator + 1)
            space[self.variable] = intersect(r, crange)
        return space

@dataclass
class Subroutine(Instruction):
    tag: Tag
    routine: List[Instruction]

@dataclass
class Program:
    subroutines: Dict[Tag, Subroutine]

    def executeall(self, start: Tag, space: Space) -> Iterator[Space]:
        sub = self.subroutines[start]
        for inst in sub.routine:
            if inst == ACCEPT:
                yield space
            if isinstance(inst, Redirect):
                yield from self.executeall(inst.tag, space)
            if isinstance(inst, Conditional):
                subspace = inst.subset(space)
                space = inst.complement(space)
                if inst.outcome == ACCEPT:
                    yield subspace
                elif isinstance(inst.outcome, Redirect):
                    yield from self.executeall(inst.outcome.tag, subspace)

def parse(data: List[str]) -> Tuple[Program, List[Part]]:
    program: Dict[Tag, Subroutine] = {}
    for line in data:
        if line.strip() == "":
            break
        tag, sub = parse_subroutine(line)
        program[tag] = sub
    return Program(program)

def parse_subroutine(line: str) -> Tuple[Tag, Subroutine]:
    tag, substr = line.strip().split('{')
    inststr = substr[:-1].split(',')
    routine: List[Instruction] = []
    for inst in inststr:
        if ':' in inst:
            conditional, result = inst.split(':')
            e, ineq, comparator = conditional[0], conditional[1], conditional[2:]
            routine.append(Conditional(
                e, ineq, int(comparator), LOOKUP.get(result, Redirect(result))
            ))
        else:
            routine.append(LOOKUP.get(inst, Redirect(inst)))
    return tag, Subroutine(tag, routine)

def volume(space: Space) -> int:
    return len(space['x']) * len(space['m']) * len(space['a']) * len(space['s'])

if __name__ == '__main__':
    data = get_data(day=19, year=2023).split('\n')
    program = parse(data)
    program.subroutines['A'] = Subroutine('A', [ACCEPT])
    program.subroutines['R'] = Subroutine('R', [REJECT])

    space = {k: range(1, 4001) for k in 'xmas'}
    accepted = []
    for s in program.executeall('in', space):
        accepted.append(s)
    print(f"The total number of accepted parts is: {sum(volume(a) for a in accepted)}")