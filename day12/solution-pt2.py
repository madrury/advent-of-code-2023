from aocd import get_data
from typing import List, Tuple
from functools import cache

OPERATIONAL = "."
DAMAGED = "#"
UNKNOWN = "?"

Condition = str
Contiguous = Tuple[int]


def parse_line(line: str, repeats: int = 5) -> Tuple[Condition, Contiguous]:
    condition, contigstr = line.strip().split(' ')
    condition = '?'.join([condition]*repeats)
    contigstr = ','.join([contigstr]*repeats)
    contiguous = tuple(int(n) for n in contigstr.split(','))
    return condition, contiguous

@cache
def search(condition: Condition, contiguous: Contiguous) -> int:
    if is_hopeless(condition, contiguous):
        return 0
    if is_complete(condition, contiguous):
        return 1
    if condition[0] == UNKNOWN:
        return (
            search(condition[1:], contiguous)
            + search(DAMAGED + condition[1:], contiguous)
        )
    if condition[0] == OPERATIONAL:
        return search(condition[1:], contiguous)
    if condition[0] == DAMAGED:
        chunksize = contiguous[0]
        segment = set(condition[0:chunksize])
        if not segment.issubset({DAMAGED, UNKNOWN}):
            # For example, cannot continue #?.? if we need a chunk of 4 damaged
            # next.
            return 0
        # Need to continue with the charecter following the chunk as a '.'.
        if chunksize < len(condition) and condition[chunksize] == DAMAGED:
            return 0
        # Our continuation is forced.
        return search(condition[chunksize + 1:], contiguous[1:])

@cache
def is_hopeless(condition: Condition, contiguous: Contiguous) -> bool:
    damaged_count = condition.count(DAMAGED)
    unknown_count = condition.count(UNKNOWN)
    if damaged_count + unknown_count < sum(contiguous):
        return True
    if not contiguous and damaged_count > 0:
        return True
    return False

@cache
def is_complete(condition: Condition, contiguous: Contiguous) -> bool:
    damaged_count = condition.count(DAMAGED)
    return not contiguous and (damaged_count == 0)


if __name__ == '__main__':
    data: List[str] = [
        line.strip()
        for line in get_data(day=12, year=2023).split('\n')
    ]

    solution_counts: List[int] = []
    for line in data:
        condition, contiguous = parse_line(line, repeats=5)
        solution_counts.append(search(condition, contiguous))
    print(f"Total solutions counts: {sum(solution_counts)}")