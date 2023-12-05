from aocd import get_data
from dataclasses import dataclass
from string import digits
from typing import List, Set, Dict, Tuple

NON_SYMBOLS = digits + '.'

@dataclass
class Symbol:
    glyph: str
    coordinate: Tuple[int, int]

    def __eq__(self, other) -> bool:
        return self.coordinate == other.coordinate

    def is_gear(self) -> bool:
        return self.glyph == '*'

GearTable = Dict[Tuple[int, int], Symbol]

@dataclass
class Number:
    row: int
    boundary: Tuple[int, int]
    value: int
    adjacent_gears: List[Symbol] = None


def all_glyphs(data: List[str]) -> Set[str]:
    """What are all the symbols that appear in the input?"""
    return set.union(
        *(
            set(c for c in line if c not in NON_SYMBOLS)
            for line in data
        )
    )

def collect_symbols(data: List[str], glyphs: Set[str]) -> List[Symbol]:
    symbols: List[Symbol] = []
    for row, line in enumerate(data):
        for col, ch in enumerate(line):
            if ch in glyphs:
                symbols.append(Symbol(ch, (row, col)))
    return symbols

def number_boundaries(line: str) -> List[Tuple[int, int]]:
    begin_numbers, end_numbers = [], []
    if line[0] in digits:
        begin_numbers.append(0)
    for idx, (ch, next) in enumerate(zip(line, line[1:])):
        if next in digits and ch not in digits:
            begin_numbers.append(idx+1)
    for idx, (ch, next) in enumerate(zip(line, line[1:])):
        if ch in digits and next not in digits:
            end_numbers.append(idx)
    if line[-1] in digits:
        end_numbers.append(len(line))
    return list(zip(begin_numbers, end_numbers))

def parse_numbers_from_line(row: int, line: str) -> List[Number]:
    boundaries = number_boundaries(line)
    numbers = [
        int(line[b:e+1]) for b, e in boundaries
    ]
    return [
        Number(row, bdry, num) for bdry, num in zip(boundaries, numbers)
    ]

def adjacent_glyphs(number: Number, data: List[str]) -> Set[str]:
    n_rows, n_cols = len(data), len(data[0])
    begin = max(0, number.boundary[0] - 1)
    adjacents: Set[str] = set()
    if number.row > 0:
        adjacents.update(data[number.row - 1][begin:number.boundary[1] + 2])
    if number.row < n_rows - 1:
        adjacents.update(data[number.row + 1][begin:number.boundary[1] + 2])
    if number.boundary[0] > 0:
        adjacents.add(data[number.row][number.boundary[0] - 1])
    if number.boundary[1] < n_cols - 1:
        adjacents.add(data[number.row][number.boundary[1] + 1])
    return adjacents

def find_gears_adjacent_to_number(number: Number, gear_table: GearTable) -> Number:
    adjacents: List[Symbol] = []
    adjacents.extend(
        gear_table.get((number.row - 1, col))
        for col in range(number.boundary[0] - 1, number.boundary[1] + 2)
    )
    adjacents.extend(
        gear_table.get((number.row + 1, col))
        for col in range(number.boundary[0] - 1, number.boundary[1] + 2)
    )
    adjacents.append(
        gear_table.get((number.row, number.boundary[0] - 1))
    )
    adjacents.append(
        gear_table.get((number.row, number.boundary[1] + 1))
    )
    number.adjacent_gears = [gear for gear in adjacents if gear]
    return number

def find_numbers_adjacent_to_gears(gear: Symbol, numbers: List[Number]) -> List[Number]:
    adjacents: List[Number] = []
    for n in numbers:
        if any(g == gear for g in n.adjacent_gears):
            adjacents.append(n)
    return adjacents


if __name__ == '__main__':
    data: List[str] = [
        line.strip()
        for line in get_data(day=3, year=2023).split('\n')
    ]
    glyphs = all_glyphs(data)
    symbols = collect_symbols(data, glyphs)

    gear_table: GearTable = {
        (sym.coordinate[0], sym.coordinate[1]): sym
        for sym in symbols
        if sym.is_gear()
    }

    numbers: List[Number] = []
    for row, line in enumerate(data):
        numbers.extend(parse_numbers_from_line(row, line))

    part_numbers = [
        n for n in numbers
        if adjacent_glyphs(n, data) & glyphs
    ]
    print(f"Sum of all part numbers: {sum(n.value for n in part_numbers)}")

    for number in numbers:
        _ = find_gears_adjacent_to_number(number, gear_table)

    ratios: List[int] = []
    gears = list(gear_table.values())
    for gear in gears:
        adjacents = find_numbers_adjacent_to_gears(gear, numbers)
        if len(adjacents) == 2:
            ratios.append(adjacents[0].value * adjacents[1].value)
    print(f"The sum of the gear ratios is: {sum(ratios)}")
