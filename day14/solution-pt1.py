from aocd import get_data
import numpy as np
from typing import List, Tuple, Optional

Map = List[List[str]]
FinalPositions = List[int]

BLANK = '.'
ROUND = 'O'
CUBE = '#'

def parse(data: List[str]) -> Map:
    return [list(line.strip()) for line in data]

def roll_up(row: List[str]) -> FinalPositions:
    most_recent_cube_idx: int = 0
    number_of_round_seen: int = 0
    final_positions: FinalPositions = []
    for idx, ch in enumerate(row):
        if ch == ROUND:
            number_of_round_seen += 1
        if ch == CUBE:
            final_positions.extend(
                range(most_recent_cube_idx, most_recent_cube_idx + number_of_round_seen)
            )
            most_recent_cube_idx = idx + 1
            number_of_round_seen = 0
    final_positions.extend(
        range(most_recent_cube_idx, most_recent_cube_idx + number_of_round_seen)
    )
    return final_positions

def iter_columns(map: Map) -> List[str]:
    for idx in range(len(map[0])):
        yield [map[r][idx] for r in range(len(map))]


if __name__ == '__main__':
    data = (
"""
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
    )
    data: List[str] = get_data(day=14, year=2023).split('\n')
    map = parse(data)
    ROWS, COLS = len(map), len(map[0])

    finals: List[FinalPositions] = []
    for col in iter_columns(map):
        print(roll_up(col))
        finals.append(roll_up(col))

    load: int = 0
    for final in finals:
        load += sum(COLS - p for p in final)
    print(f"The final load is {load}")