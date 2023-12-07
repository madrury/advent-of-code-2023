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
    print(get_data(day=6, year=2023).split('\n'))
    # data: List[str] = [
    #     line.strip()
    #     for line in get_data(day=6, year=2023).split('\n')
    # ]
    # print(data)
    RACES = [Race(54, 446), Race(81, 1292), Race(70, 1035), Race(88, 1007)]
    RACE = Race(54817088, 446129210351007)
    # RACES = [Race(7, 9), Race(15, 40), Race(30, 200)]
    supports = [r.support for r in RACES]
    print(supports)
    sol = prod(x[1] - x[0] + 1 for x in supports)
    print(f"The product is: {sol}")

    support = RACE.support
    print(f"The number of ways to win is: {support[1] - support[0] + 1}")
