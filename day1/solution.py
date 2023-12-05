from aocd import get_data
from typing import List, Set
from string import digits

Digit = str
CalibrationValue = int

DIGITS: Set[Digit] = set(digits)
REPLACEMENTS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

def parse_digits(lines: List[str]) -> List[Digit]:
    for line in lines:
        yield [c for c in line if c in DIGITS]

def digits_to_number(digits: List[Digit]) -> int:
    match digits:
        case []: return 0
        case [x]: return 10*int(x) + int(x)
        case _: return 10*int(digits[0]) + int(digits[-1])

def replace_words_with_digits(line: str) -> str:
    while True:
        positions = {
            word: line.find(word) for word in REPLACEMENTS
        }
        positions = {
            word: position for word, position in positions.items()
            if position >= 0
        }
        if not positions:
            break
        word = min(positions, key=positions.get)
        line = line.replace(word, REPLACEMENTS[word], 1)
    return line


if __name__ == '__main__':
    data: str = get_data(day=1, year=2023)
    lines: List[str] = [line.strip() for line in data.split('\n')]

    # Part 1.
    print(sum(digits_to_number(d) for d in parse_digits(lines)))

    # Part 2
    lines = [replace_words_with_digits(line) for line in lines]
    print(sum(digits_to_number(d) for d in parse_digits(lines)))