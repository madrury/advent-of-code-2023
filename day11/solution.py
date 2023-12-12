from aocd import get_data
from dataclasses import dataclass
from typing import List, Self, Dict, Tuple, Set
from itertools import combinations


Galaxy = Tuple[int, int]

def find_empty_rows(data: List[str]) -> Set[int]:
    rowids: List[int] = []
    for i, row in enumerate(data):
        if all(ch == '.' for ch in row):
            rowids.append(i)
    return set(rowids)

def find_empty_columns(data: List[str]) -> Set[int]:
    colids: List[int] = []
    for j in range(len(data[0])):
        col = [row[j] for row in data]
        if all(ch == '.' for ch in col):
            colids.append(j)
    return set(colids)

def find_galaxys(
    data: List[str],
    empty_rows: Set[int],
    empty_cols: Set[int],
    expansion_factor: int
) -> List[Galaxy]:
    galaxys: List[Galaxy] = []
    for i, row in enumerate(data):
        for j, ch in enumerate(row):
            if ch == '#':
                x = i + expansion_factor * sum(p in empty_rows for p in range(i))
                y = j + expansion_factor * sum(p in empty_cols for p in range(j))
                galaxys.append((x, y))
    return galaxys

def distance(g1: Galaxy, g2: Galaxy) -> int:
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])


if __name__ == '__main__':
    data: List[str] = [
        line.strip()
        for line in get_data(day=11, year=2023).split('\n')
    ]

    empty_rows = find_empty_rows(data)
    empty_cols = find_empty_columns(data)

    galaxys = find_galaxys(data, empty_rows, empty_cols, expansion_factor=1)
    total = sum(distance(g1, g2) for g1, g2 in combinations(galaxys, r=2))
    print(f"The total galaxy distance is: {total}")

    galaxys = find_galaxys(data, empty_rows, empty_cols, expansion_factor=999_999)
    total = sum(distance(g1, g2) for g1, g2 in combinations(galaxys, r=2))
    print(f"The total galaxy distance is: {total}")