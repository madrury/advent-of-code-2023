from aocd import get_data
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Round:
    red: int = 0
    blue: int = 0
    green: int = 0

GameId = int
Game = List[Round]

# Maximum cubes allowed in any round (part I).
MAX_ROUND = Round(red=12, blue=14, green=13)


def parse_line(line: str) -> Tuple[GameId, Game]:
    prefix, suffix = line.strip().split(':')
    # Parse game id from prefix
    _, id = prefix.split(' ')
    # Rounds are seperated by semicolons
    roundstrs = [r.strip() for r in suffix.strip().split(';')]
    rounds: List[Round] = [Round() for _ in roundstrs]
    for round, roundstr in zip(rounds, roundstrs):
        for cubestr in roundstr.split(', '):
            match cubestr.split(' '):
                case [n, "red"]: round.red = int(n)
                case [n, "blue"]: round.blue = int(n)
                case [n, "green"]: round.green = int(n)
    return int(id), rounds

def is_valid_game(game: Game) -> bool:
    return (
        all(round.red <= MAX_ROUND.red for round in game)
        and all(round.blue <= MAX_ROUND.blue for round in game)
        and all(round.green <= MAX_ROUND.green for round in game)
    )

def minimum_cubes(game: Game) -> Round:
    return Round(
        red = max(round.red for round in game),
        blue = max(round.blue for round in game),
        green = max(round.green for round in game)
    )


if __name__ == '__main__':
    data: List[str] = [
        line.strip()
        for line in get_data(day=2, year=2023).split('\n')
    ]
    games: Dict[GameId, Game] = {
        id: game
        for id, game in map(parse_line, data)
    }

    # Part 1
    valid_game_ids = [
        id
        for id, game in games.items()
        if is_valid_game(game)
    ]
    print(f"Sum of valid game ids: {sum(valid_game_ids)}")

    # Part 2
    mcubes = {
        id: minimum_cubes(game) for id, game in games.items()
    }
    powers = [
        r.red * r.blue * r.green for r in mcubes.values()
    ]
    print(f"Sum of powers of minimum games: {sum(powers)}")