from aocd import get_data
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

Seed = int

@dataclass
class Segment:
    source_start: int
    destination_start: int
    range: range

    def eval(self, x: int) -> int | None:
        if x in self.range:
            return (x - self.source_start) + self.destination_start
        return None

@dataclass
class Map:
    source: str
    target: str
    segments: [Segment]

    def eval(self, x: int) -> int:
        for s in self.segments:
            maybe = s.eval(x)
            if maybe: return maybe
        return x

class ParseStates(Enum):
    SEEDS = 0
    BLANK = 1
    HEADER = 2
    SEGMENT = 3

def parse(data: List[str]) -> (List[Seed], List[Map]):
    state = ParseStates.SEEDS
    seeds: [int] = []
    maps: [Map] = []
    for line in data:
        if line == '':
            state = ParseStates.BLANK
        match state:
            case ParseStates.SEEDS:
                seeds = parse_seeds_line(line)
                state = ParseStates.BLANK
            case ParseStates.BLANK:
                state = ParseStates.HEADER
            case ParseStates.HEADER:
                maps.append(parse_header_line(line))
                state = ParseStates.SEGMENT
            case ParseStates.SEGMENT:
                maps[-1].segments.append(parse_segment_line(line))
    return seeds, maps

def parse_seeds_line(line: str) -> List[int]:
    _, seedstr = line.split(':')
    return [int(x) for x in seedstr.strip().split(' ')]

def parse_header_line(line: str) -> Map:
    header = line[0:-5] # String the ' map:' suffix.
    source, target = header.split('-to-')
    return Map(source, target, segments=[])

def parse_segment_line(line: str) -> Segment:
    dstart, sstart, rlen = [int(x) for x in line.split(' ')]
    rng = range(sstart, sstart + rlen)
    return Segment(sstart, dstart, range=rng)

def evaluate_seed(seed: Seed, atlas: Dict[str, Map]) -> int:
    map = atlas['seed']
    target = map.target
    x: int = seed
    while target:
        if target == 'location':
            return map.eval(x)
        x = map.eval(x)
        map = atlas[target]
        target = map.target


if __name__ == '__main__':
    data: List[str] = [
        line.strip()
        for line in get_data(day=5, year=2023).split('\n')
    ]
    seeds, maps = parse(data)
    atlas: Dict[str, Map] = {
        map.source: map for map in maps
    }

    locations = []
    for seed in seeds:
        locations.append(evaluate_seed(seed, atlas))
    print(f"The minimum location number is: {min(locations)}")