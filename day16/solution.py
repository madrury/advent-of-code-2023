from aocd import get_data
from abc import abstractmethod
from enum import Enum
from dataclasses import dataclass
from itertools import product
from typing import List, Tuple, List, Set

N_ROW, N_COL = 110, 110

EMPTY = '.'
BACK_MIRROR = '/'
FORWARD_MIRROR = '\\'
HORIZONTAL_SPLITTER = '-'
VERTICAL_SPLITTER = '|'

Map = List[List[str]]
Coordinate = Tuple[int, int]

class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

    def __getitem__(self, idx) -> int:
        return self.value[idx]


BACK_MIRROR_DIRECTION_MAPPING = {
    Direction.NORTH: Direction.EAST,
    Direction.SOUTH: Direction.WEST,
    Direction.EAST: Direction.NORTH,
    Direction.WEST: Direction.SOUTH
}
FORWARD_MIRROR_DIRECTION_MAPPING = {
    Direction.NORTH: Direction.WEST,
    Direction.SOUTH: Direction.EAST,
    Direction.EAST: Direction.SOUTH,
    Direction.WEST: Direction.NORTH
}

@dataclass(frozen=True)
class Photon:
    position: Coordinate
    heading: Direction

    def tick(self, map: Map) -> List["Photon"]:
        p, h = self.position, self.heading
        # print(p, h)
        match map[p[0]][p[1]], h:
            case '.', _:
                return [Photon((p[0] + h[0], p[1] + h[1]), h)]
            case '/', _:
                nh = BACK_MIRROR_DIRECTION_MAPPING[h]
                return [Photon((p[0] + nh[0], p[1] + nh[1]), nh)]
            case '\\', _:
                nh = FORWARD_MIRROR_DIRECTION_MAPPING[h]
                return [Photon((p[0] + nh[0], p[1] + nh[1]), nh)]
            case '-', (Direction.EAST | Direction.WEST):
                return [Photon((p[0] + h[0], p[1] + h[1]), h)]
            case '-', (Direction.NORTH | Direction.SOUTH):
                return [
                    Photon((p[0], p[1] + 1), Direction.EAST),
                    Photon((p[0], p[1] - 1), Direction.WEST),
                ]
            case '|', (Direction.NORTH | Direction.SOUTH):
                return [Photon((p[0] + h[0], p[1] + h[1]), h)]
            case '|', (Direction.EAST | Direction.WEST):
                return [
                    Photon((p[0] - 1, p[1]), Direction.NORTH),
                    Photon((p[0] + 1, p[1]), Direction.SOUTH),
                ]
            case x:
                raise ValueError(f"Awww shit {x}.")

    @property
    def in_bounds(self):
        return (
            (0 <= self.position[0] < N_ROW)
            and (0 <= self.position[1] < N_COL)
        )


class Simulation:

    def __init__(self, photon: Photon):
        self.photons = [photon]
        self.illuminated: Set[Coordinate] = set()
        self.history: Set[Photon] = set()

    @property
    def n_illuminated(self) -> int:
        return len(self.illuminated)

    def run(self, map: Map):
        while self.photons:
            photon = self.photons.pop()
            if (not photon.in_bounds) or (photon in self.history):
                continue
            self.history.add(photon)
            self.illuminated.add(photon.position)
            newphons = photon.tick(map)
            self.photons.extend(newphons)

def iter_initial_photons():
    for i in range(N_ROW):
        yield Photon((i, 0), Direction.EAST)
        yield Photon((i, N_COL - 1), Direction.WEST)
    for j in range(N_COL):
        yield Photon((0, j), Direction.SOUTH)
        yield Photon((0, j), Direction.NORTH)

def solve(map: Map) -> int:
    seen: Set[Photon] = set()
    M = 0
    for p in iter_initial_photons():
        if p in seen:
            continue
        print(f"Running photon: {p.position, p.heading}")
        s = Simulation(p)
        s.run(map)
        M = max(M, s.n_illuminated)
        seen.update(s.history)
    return M

if __name__ == '__main__':
    map: Map = get_data(day=16, year=2023).split('\n')
    map = [list(row) for row in map]

    λ = Photon((0, 0), Direction.EAST)
    s = Simulation(λ)
    s.run(map)
    print(f"The number of illuminated tiles is {len(s.illuminated)}")

    M = solve(map)
    print(f"The maximum illumination is:{M}")