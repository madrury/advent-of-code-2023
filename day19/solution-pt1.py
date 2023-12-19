from aocd import get_data
import json
from dataclasses import dataclass
from typing import List, Tuple, List, Iterator, Dict

Tag = str
Part = Dict[str, int]

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
    outcome: Redirect | Accept | Reject | Next

    def execute(self, part: Part) -> Redirect | Accept | Reject | Next:
        if self.inequality == '<':
            if part[self.variable] < self.comparator:
                return self.outcome
            else:
                return NEXT
        elif self.inequality == '>':
            if part[self.variable] > self.comparator:
                return self.outcome
            else:
                return NEXT
        else:
            raise ValueError(f"Unknown inequality {self.inequality}")

@dataclass
class Subroutine(Instruction):
    tag: Tag
    routine: List[Instruction]

    def exectute(self, part: Part) -> Accept | Reject | Redirect:
        stack = list(reversed(self.routine))
        while stack:
            inst = stack.pop().execute(part)
            if inst == NEXT:
                continue
            if inst == ACCEPT or inst == REJECT:
                return inst
            if isinstance(inst, Redirect):
                return inst
        raise ValueError(f"Empty stack!")

@dataclass
class Program:
    subroutines: Dict[Tag, Subroutine]

    def execute(self, part: Part, start: Tag) -> Accept | Reject:
        sub = self.subroutines[start]
        while True:
            result = sub.exectute(part)
            if result == ACCEPT or result == REJECT:
                return result
            # It's a redirect
            sub = self.subroutines[result.tag]


def parse(data: List[str]) -> Tuple[Program, List[Part]]:
    program: Dict[Tag, Subroutine] = {}
    parts: List[Part] = []
    reading_subroutines = True
    for line in data:
        if line.strip() == "":
            reading_subroutines = False
            continue

        if reading_subroutines:
            tag, sub = parse_subroutine(line)
            program[tag] = sub
        else:
            parts.append(parse_part(line))
    return Program(program), parts

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

def parse_part(line: str) -> Part:
    part: Part = {}
    for s in line.strip()[1:-1].split(','):
        v, i = s.split('=')
        part[v] = int(i)
    return part

def rating(part: Part) -> int:
    return sum(part.values())


if __name__ == '__main__':
#     data = (
# """
# px{a<2006:qkq,m>2090:A,rfg}
# pv{a>1716:R,A}
# lnx{m>1548:A,A}
# rfg{s<537:gd,x>2440:R,A}
# qs{s>3448:A,lnx}
# qkq{x<1416:A,crn}
# crn{x>2662:A,R}
# in{s<1351:px,qqz}
# qqz{s>2770:qs,m<1801:hdj,R}
# gd{a>3333:R,R}
# hdj{m>838:A,pv}

# {x=787,m=2655,a=1222,s=2876}
# {x=1679,m=44,a=2067,s=496}
# {x=2036,m=264,a=79,s=2244}
# {x=2461,m=1339,a=466,s=291}
# {x=2127,m=1623,a=2188,s=1013}
# """.strip().split('\n')
#     )
    data = get_data(day=19, year=2023).split('\n')
    program, parts = parse(data)

    accepted, rejected = [], []
    for part in parts:
        result = program.execute(part, start="in")
        if result == ACCEPT:
            accepted.append(part)
        elif result == REJECT:
            rejected.append(part)
        else:
            print(f"Part was niether accepted or rejected: {part}")
    print(f"Accepted: {len(accepted)}, Rejected {len(rejected)}")
    print(f"Total rating for accepted parts: {sum(rating(p) for p in accepted)}")

