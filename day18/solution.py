from aocd import get_data
from enum import Enum
from math import copysign
from dataclasses import dataclass
from typing import List, Tuple, List, Iterator

Coordinate = Tuple[int, int]

class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

    def __getitem__(self, idx) -> int:
        return self.value[idx]

    @staticmethod
    def from_str(s: str) -> "Direction":
        return {
            'U': Direction.NORTH,
            'D': Direction.SOUTH,
            'L': Direction.WEST,
            'R': Direction.EAST
        }[s]

    def from_hex(s: str) -> "Direction":
        #0 means R, 1 means D, 2 means L, and 3 means U
        return {
            '3': Direction.NORTH,
            '1': Direction.SOUTH,
            '2': Direction.WEST,
            '0': Direction.EAST
        }[s]


@dataclass
class Instruction:
    direction: Direction
    n: int
    RGB: str

    def execute(self, p: Coordinate) -> Iterator[Coordinate]:
        for i in range(1, self.n+1):
            yield (
                p[0] + i * self.direction[0],
                p[1] + i * self.direction[1],
            )

    def from_rgb(self) -> "Instruction":
        return Instruction(
            Direction.from_hex(self.RGB[-1]),
            int(self.RGB[:-1], 16),
            self.RGB
        )

Program = List[Instruction]

def parse(line: str) -> Instruction:
    d, n, rgb = line.strip().split(' ')
    return Instruction(Direction.from_str(d), int(n), rgb[2:-1])

def sign(x: int) -> int:
    if x == 0: return 0
    else: return copysign(1.0, x)

def area(program: Program) -> int:
    A = 0
    N = 0
    position = (0, 0)
    for instruction in program:
        end = (
            position[0] + instruction.direction[0] * instruction.n,
            position[1] + instruction.direction[1] * instruction.n,
        )
        A += instruction.n * position[1] * sign(end[0] - position[0])
        N += instruction.n
        position = end
    A = copysign(A, 1.0)
    return A + (N + 2) / 2


if __name__ == '__main__':
    data = get_data(day=18, year=2023).split('\n')
    program: Program = [parse(line) for line in data]
    print(f"The area of the hole is {area(program)}")

    program = [i.from_rgb() for i in program]
    print(f"The area of the giant hole is {area(program)}")
