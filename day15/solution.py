from aocd import get_data
from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Lens:
    label: str
    focal: int

    def __eq__(self, other) -> bool:
        return self.label == other.label

    def __repr__(self) -> str:
        return f"⦅{self.label}:{self.focal}⦆"


class Box:
    def __init__(self, id: int):
        self.id = id
        self.contents: List[Lens] = []

    def __repr__(self) -> str:
        return "[" + " ".join(str(l) for l in self.contents) + "]" + f"⚡︎{self.power}"

    @property
    def power(self) -> int:
        return sum(
            (self.id + 1) * i * l.focal for i, l in enumerate(self.contents, start=1)
        )


class Facility:
    def __init__(self):
        self.boxes: Dict[int, Box] = {
            i: Box(i) for i in range(256)
        }

    def __getitem__(self, id: int) -> Box:
        return self.boxes[id]

    def run(self, program: List["Instruction"]):
        for instruction in program:
            instruction.execute(self)

    @property
    def power(self) -> int:
        return sum(b.power for b in self.boxes.values())


class Instruction:
    @abstractmethod
    def execute(self, facility: Facility):
        pass


class DashInstruction(Instruction):
    def __init__(self, label: str):
        self.label = label
        self.boxid = evaluate(label)

    @staticmethod
    def from_str(s: str) -> "DashInstruction":
        return DashInstruction(s[:-1])

    def execute(self, facility: Facility):
        box = facility[self.boxid]
        box.contents = [l for l in box.contents if l.label != self.label]

class EqualsInstruction(Instruction):
    def __init__(self, label: str, focal: int):
        self.label = label
        self.boxid = evaluate(label)
        self.focal = focal

    @staticmethod
    def from_str(s: str) -> "EqualsInstruction":
        left, right = s.split("=")
        return EqualsInstruction(left, int(right))

    def execute(self, facility: Facility):
        box = facility[self.boxid]
        lens = Lens(self.label, self.focal)
        try:
            box.contents[box.contents.index(lens)] = lens
        except ValueError:
            box.contents.append(lens)


def parse(data: str) -> List[Instruction]:
    steps = data.split(',')
    program: List[Instruction] = []
    for s in steps:
        if '-' in s and '=' in s:
            raise ValueError("Cannot parse instruction.")
        elif '-' in s:
            program.append(DashInstruction.from_str(s))
        elif '=' in s:
            program.append(EqualsInstruction.from_str(s))
        else:
            raise ValueError("Unknown instruction.")
    return program


def residues_kp_mod_n(k: int, n: int) -> List[int]:
    residue = k
    resudues = [k]
    for _ in range(n):
        residue = (residue * k) % n
        resudues.append(residue)
    return resudues

RESIDUES_MOD_256 = residues_kp_mod_n(17, 256)


def evaluate(step: str) -> int:
    return sum(ord(c) * r for c, r in zip(reversed(step), RESIDUES_MOD_256)) % 256


if __name__ == '__main__':
    data = get_data(day=15, year=2023).split('\n')[0]

    facility = Facility()
    program = parse(data)
    facility.run(program)

    for i, b in facility.boxes.items():
        print(i, b)

    print(f"The total focusing power is {facility.power}")