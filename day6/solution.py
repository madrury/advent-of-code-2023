from aocd import get_data
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
from math import sqrt, ceil, floor, prod

@dataclass
class Race:
    time: int
    distance: int

    @property
    def support(self) -> (int, int):
        dicrim = sqrt(self.time*self.time - 4*self.distance)
        return(
            floor((self.time - dicrim)/2 + 1),
            ceil((self.time + dicrim)/2 - 1),
        )

if __name__ == '__main__':
    RACES = [Race(54, 446), Race(81, 1292), Race(70, 1035), Race(88, 1007)]
    RACE = Race(54817088, 446129210351007)

    supports = [r.support for r in RACES]
    sol = prod(x[1] - x[0] + 1 for x in supports)
    print(f"The product is: {sol}")

    support = RACE.support
    print(f"The number of ways to win is: {support[1] - support[0] + 1}")