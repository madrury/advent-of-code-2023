from aocd import get_data
from dataclasses import dataclass
from typing import List, Self, Dict, Tuple
from itertools import cycle
from math import lcm

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

VALID_EXITS_DIRECTIONS = {
    '.': [],
    '-': [LEFT, RIGHT],
    '|': [UP, DOWN],
    'L': [UP, RIGHT],
    'F': [DOWN, RIGHT],
    'J': [UP, LEFT],
    '7': [DOWN, LEFT]
}
VALID_DESTINATIONS = {
    LEFT: ['-', 'L', 'F', 'S'],
    RIGHT: ['-', 'J', '7', 'S'],
    UP: ['|', '7', 'F', 'S'],
    DOWN: ['|', 'J', 'L', 'S'],
}

Coordinate = Tuple[int, int]

class Tile:

    def __init__(self, glyph: str, coordinate: Coordinate):
        self.glyph = glyph
        self.coordinate = coordinate
        self.exits: List[Self] = []

    def __repr__(self) -> str:
        return f"Tile({self.glyph}, exits={self.exits})"

    def __eq__(self, other: Self) -> bool:
        return self.coordinate == other.coordinate

    def find_exits(self, map: Dict[Coordinate, Self]):
        if self.glyph == 'S': return
        for (di, dj) in VALID_EXITS_DIRECTIONS[self.glyph]:
            exit_coord = (self.coordinate[0] + di, self.coordinate[1] + dj)
            exit_tile = map.get(exit_coord)
            exit_is_valid = (
                exit_tile is not None
                and exit_tile.glyph in VALID_DESTINATIONS[(di, dj)]
            )
            if exit_is_valid:
                self.exits.append(exit_coord)


def parse(data: List[str]) -> Dict[Coordinate, Tile]:
    map: Dict[Coordinate, Tile] = {}
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            map[(i, j)] = Tile(glyph=char, coordinate=(i, j))
    return map

def amend_exits_adjacent_to_start(start: Tile, map: Dict[Coordinate, Tile]):
    for (di, dj) in VALID_DESTINATIONS.keys():
        exit_coord = (start.coordinate[0] + di, start.coordinate[1] + dj)
        exit_tile = map.get(exit_coord)
        if exit_tile and start.coordinate in exit_tile.exits:
            start.exits.append(exit_tile.coordinate)

def walk(start: Tile, map: Dict[Coordinate, Tile]) -> List[Tile]:
    path = [start]
    prev: Tile = start
    current: Tile = map[start.exits[0]]
    while current != start:
        path.append(current)
        next_coord = [c for c in current.exits if c != prev.coordinate][0]
        prev = current
        current = map[next_coord]
    return path

def interior_lattice_points(path: List[Tile]) -> int:
    path.append(path[0])
    A = 0
    # Greens theorem for the area of a polygon.
    for current, nxt in zip(path[:-1], path[1:]):
        x = current.coordinate[1]
        dy = nxt.coordinate[0] - current.coordinate[0]
        A += x * dy
    # We may have the negative area if we walked in the wrong direction.
    if A < 0:
        A = -1 * A
    # Picks theorem for the number of interior lattice points given the area and
    # number of vertex lattice points.
    return A + 1 - (len(path) - 1) / 2


if __name__ == '__main__':
    data: List[str] = [
        line.strip()
        for line in get_data(day=10, year=2023).split('\n')
    ]

    map = parse(data)
    for _, tile in map.items():
        tile.find_exits(map)
    start = next(tile for tile in map.values() if tile.glyph == 'S')
    amend_exits_adjacent_to_start(start, map)

    path = walk(start, map)
    print(f"The half length of the path is: {len(path) // 2}")

    area = interior_lattice_points(path)
    print(f"The count of interior lattice points is: {int(area)}")