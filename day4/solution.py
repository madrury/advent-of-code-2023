from aocd import get_data
from dataclasses import dataclass
from string import digits
from typing import List, Set, Dict, Tuple

@dataclass
class Card:
    n: int
    winning: Set[int]
    have: Set[int]
    copies: int = 1

    @property
    def matches(self) -> Set[int]:
        return self.have & self.winning

    @property
    def points(self) -> int:
        if not self.matches:
            return 0
        return 2**(len(self.matches) - 1)

def parse_line(line: str) -> Card:
    cardstr, numberstr = line.split(':')
    *_, cardnumstr = cardstr.split(' ')
    winningstr, havestr = numberstr.split('|')
    winnings = {int(s) for s in winningstr.split()}
    havings = {int(s) for s in havestr.split()}
    return Card(int(cardnumstr), winnings, havings)

def reduce_cards(ogcards: List[Card]) -> List[Card]:
    ogcards = list(reversed(ogcards)) # We pop off the END of lists.
    endcards: List[Card] = []
    while ogcards:
        card = ogcards.pop()
        endcards.append(card)
        n_matches = len(card.matches)
        match_range = set(range(card.n + 1, card.n + n_matches + 1))
        for remainingcard in ogcards:
            if remainingcard.n in match_range:
                remainingcard.copies += card.copies
    return endcards



if __name__ == '__main__':
    data: List[str] = [
        line.strip()
        for line in get_data(day=4, year=2023).split('\n')
    ]
    cards = [parse_line(line) for line in data]
    # Part 1.
    print(f"The total points across all cards is: {sum(card.points for card in cards)}")
    # Part 2:
    cards = reduce_cards(cards)
    print(f"The reduced card score is: {sum(c.copies for c in cards)}")