from aocd import get_data
import numpy as np
from typing import List, Tuple, Optional

Pattern = np.array
Orientation = int
Symmetry = Tuple[Orientation, int]

VERTICAL = 1
HORIZONTAL = 100
MAPPING = {".": 0, "#": 1}


def parse(data: List[str]) -> List[Pattern]:
    patterns: List[np.array] = []
    pattern: List[List[int]] = []
    for row in data:
        if row.strip() == "":
            patterns.append(np.array(pattern))
            pattern = []
            continue
        pattern.append([MAPPING[ch] for ch in row.strip()])
    patterns.append(np.array(pattern))
    return patterns

def find_symmetry(x: np.array, n_smudges: int = 0) -> Symmetry:
    vs = find_vertical_symmetry(x, n_smudges)
    if vs:
        return (VERTICAL, vs)
    hs = find_vertical_symmetry(x.T, n_smudges)
    return (HORIZONTAL, hs)

def find_vertical_symmetry(x: np.array, n_smudges: int = 0) -> Optional[int]:
    for j in range(1, x.shape[1]):
        left, right = x[:, :j], x[:, j:]
        width = min(left.shape[1], right.shape[1])
        left, right = left[:, -width:], right[:, :width]
        if np.sum(np.abs(left - right[:, ::-1])) == n_smudges:
            return j
    return None


if __name__ == '__main__':
    data: List[str] = get_data(day=13, year=2023).split('\n')
    patterns = parse(data)

    symmetries: List[Symmetry] = []
    for pattern in patterns:
        symmetries.append(find_symmetry(pattern))
    total = sum(o * i for o, i in symmetries)
    print(f"The total is {total}.")

    symmetries: List[Symmetry] = []
    for pattern in patterns:
        symmetries.append(find_symmetry(pattern, n_smudges=1))
    total = sum(o * i for o, i in symmetries)
    print(f"The smuged total is {total}.")