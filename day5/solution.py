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

    def eval_range(self, r: range) -> range:
        assert (r.start >= self.range.start) and (r.stop <= self.range.stop)
        return range(
            (r.start - self.source_start) + self.destination_start,
            (r.stop - self.source_start) + self.destination_start
        )

@dataclass
class Map:
    source: str
    target: str
    segments: List[Segment]

    def eval(self, x: int) -> int:
        for s in self.segments:
            maybe = s.eval(x)
            if maybe: return maybe
        return x

    def eval_range(self, r: range) -> List[range]:
        queue: List[range] = [r]
        output: List[range] = []
        for segment in self.segments:
            nqueue = []
            for r in queue:
                nqueue.append(left_difference(r, segment.range))
                nqueue.append(right_difference(r, segment.range))
                i = intersect(r, segment.range)
                if i:
                    output.append(segment.eval_range(i))
            queue = [r for r in nqueue if r is not None]
        return output + queue


# -- range API functions ---
def intersect(r0: range, r1: range) -> range | None:
    if r0.start > r1.start:
        r0, r1 = r1, r0
    if r0.stop <= r1.start:
        return None
    return range(max(r0.start, r1.start), min(r0.stop, r1.stop))

def left_difference(r0: range, r1: range) -> range | None:
    if r0.start < r1.start:
        return range(r0.start, min(r0.stop, r1.start))
    return None

def right_difference(r0: range, r1: range) -> range | None:
    if r0.stop > r1.stop:
        return range(max(r0.start, r1.stop), r0.stop)
    return None


# --- Parsing ---
class ParseStates(Enum):
    SEEDS = 0
    BLANK = 1
    HEADER = 2
    SEGMENT = 3

def parse(data: List[str]) -> (List[Seed], List[Map]):
    state = ParseStates.SEEDS
    seeds: List[int] = []
    maps: List[Map] = []
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
    header = line[0:-5] # Strip the ' map:' suffix.
    source, target = header.split('-to-')
    return Map(source, target, segments=[])

def parse_segment_line(line: str) -> Segment:
    dstart, sstart, rlen = [int(x) for x in line.split(' ')]
    rng = range(sstart, sstart + rlen)
    return Segment(sstart, dstart, range=rng)

def to_seed_ranges(seeds: List[Seed]) -> List[range]:
    return [
        range(x, x + y) for x, y in zip(seeds[0::2], seeds[1::2])
    ]

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

def evaluate_seed_range(seedrange: range, atlas: Dict[str, Map]) -> int:
    map = atlas['seed']
    target = map.target
    xs: List[range] = [seedrange]
    while target:
        if target == 'location':
            return sum([map.eval_range(x) for x in xs], [])
        xs = sum([map.eval_range(x) for x in xs], [])
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

    location_ranges = []
    seed_ranges = to_seed_ranges(seeds)
    for srng in seed_ranges:
        location_ranges.append(evaluate_seed_range(srng, atlas))

    location_ranges = sum(location_ranges, [])
    print(f"The minimum location number is: {min(r.start for r in location_ranges)}")
