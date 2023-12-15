from aocd import get_data
from typing import List, Tuple, Set
from itertools import cycle

N_ROWS, N_COLS = 100, 100

Coordinate = Tuple[int, int]
Cubes = Set[Coordinate]
Rollers = Set[Coordinate]

BLANK = '.'
CUBE = '#'
ROLLER = 'O'

def parse(data: List[str]) -> Tuple[Cubes, Rollers]:
    cubes, rollers = set(), set()
    for i, line in enumerate(data):
        for j, ch in enumerate(line):
            if ch == CUBE: cubes.add((i, j))
            if ch == ROLLER: rollers.add((i, j))
    return cubes, rollers

def display(cubes: Cubes, rollers: Rollers):
    rows = []
    for i in range(N_ROWS):
        row = []
        for j in range(N_COLS):
            if (i, j) in cubes: row.append(CUBE)
            elif (i, j) in rollers: row.append(ROLLER)
            else: row.append(BLANK)
        rows.append(''.join(row))
    print('\n'.join(rows))

def load(rollers: Rollers) -> int:
    return sum(N_ROWS - i for (i, j) in rollers)

def flip_vertical(xs: Set[Coordinate]) -> Set[Coordinate]:
    return {(N_ROWS - i - 1, j) for (i, j) in xs}

def flip_horizontal(xs: Set[Coordinate]) -> Set[Coordinate]:
    return {(i, N_COLS - j - 1) for (i, j) in xs}

def roll_north(cubes: Cubes, rollers: Rollers) -> Rollers:
    final_positions: Rollers = set()
    for j in range(N_COLS):
        most_recent_cube_idx: int = -1
        number_of_rollers_seen: int = 0
        for i in range(N_ROWS):
            if (i, j) in rollers:
                number_of_rollers_seen += 1
            if (i, j) in cubes:
                final_positions.update(
                    (most_recent_cube_idx + x + 1, j) for x in
                    range(number_of_rollers_seen)
                )
                most_recent_cube_idx = i
                number_of_rollers_seen = 0
            final_positions.update(
                (most_recent_cube_idx + x + 1, j) for x in
                range(number_of_rollers_seen)
            )
    return final_positions

def roll_south(cubes: Cubes, rollers: Rollers) -> Rollers:
    fcubes = flip_vertical(cubes)
    frollers = flip_vertical(rollers)
    return flip_vertical(roll_north(fcubes, frollers))

def roll_west(cubes: Cubes, rollers: Rollers) -> Rollers:
    final_positions: Rollers = set()
    for i in range(N_ROWS):
        most_recent_cube_idx: int = -1
        number_of_rollers_seen: int = 0
        for j in range(N_COLS):
            if (i, j) in rollers:
                number_of_rollers_seen += 1
            if (i, j) in cubes:
                final_positions.update(
                    (i, most_recent_cube_idx + x + 1) for x in
                    range(number_of_rollers_seen)
                )
                most_recent_cube_idx = j
                number_of_rollers_seen = 0
            final_positions.update(
                (i, most_recent_cube_idx + x + 1) for x in
                range(number_of_rollers_seen)
            )
    return final_positions

def roll_east(cubes: Cubes, rollers: Rollers) -> Rollers:
    fcubes = flip_horizontal(cubes)
    frollers = flip_horizontal(rollers)
    return flip_horizontal(roll_west(fcubes, frollers))


NORTH, WEST, SOUTH, EAST = 0, 1, 2, 3
DIRECTION_TABLE = {
    NORTH: roll_north,
    WEST: roll_west,
    SOUTH: roll_south,
    EAST: roll_east
}
Cycle = Tuple[int, int]

class Solver:

    def __init__(self, cubes: Cubes, rollers: Rollers):
        self.cubes = cubes
        self.rollers = rollers
        self.cache = {}

    def solve(self) -> Cycle:
        cubes, rollers = self.cubes, self.rollers
        for n, direction in enumerate(cycle([NORTH, WEST, SOUTH, EAST])):
            key = (direction, frozenset(rollers))
            if key in self.cache:
                return self.cache[key], n
            self.cache[key] = n
            rollers = DIRECTION_TABLE[direction](cubes, rollers)


if __name__ == '__main__':
    data: List[str] = get_data(day=14, year=2023).split('\n')

    cubes, rollers = parse(data)

    solver = Solver(cubes, rollers)
    start, stop = solver.solve()
    print(f"Detected cycle from {start} -> {stop}")

    N = 1_000_000_000 * 4
    final_idx = (N - start) % (stop - start) + start
    _, finalrollers = next(k for k, v in solver.cache.items() if v == final_idx)
    print(f"The final load is {load(finalrollers)}")