from aocd import get_data
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Self
from collections import Counter
from functools import total_ordering

CARD_VALUES = (
    {c: int(c) for c in '23456789'}
    | {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
)
NON_JOKERS = "23456789TQKA"
JOKER_CARD_VALUES = (
    {c: v for c, v in CARD_VALUES.items() if c != 'J'}
    | {'J': 1}
)

@total_ordering
class HandRank(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

    def __lt__(self, other: Self) -> bool:
        return self.value < other.value


@total_ordering
class Hand:
    def __init__(self, cards: str, score: int):
        self.cards = cards.strip()
        self.histogram = Counter(self.cards)
        self.rank = self._rank()
        self.score = int(score)

    def __repr__(self) -> str:
        return f"Hand({self.cards}, {self.rank}, {self.score})"

    def __eq__(self, other: Self) -> bool:
        return self.cards == other.cards

    def __lt__(self, other: Self) -> bool:
        if self.rank != other.rank:
            return self.rank < other.rank
        for mine, theirs in zip(self.cards, other.cards):
            if mine != theirs:
                return CARD_VALUES[mine] < CARD_VALUES[theirs]
        raise ValueError(f"{self} and {other} are the same hand.")

    def _rank(self) -> HandRank:
        (argmax, themax), *_ =  self.histogram.most_common()
        counts = set(self.histogram.values())
        countscounts = Counter(self.histogram.values())
        if themax == 5:
            return HandRank.FIVE_OF_A_KIND
        if themax == 4:
            return HandRank.FOUR_OF_A_KIND
        if counts == {3, 2}:
            return HandRank.FULL_HOUSE
        if themax == 3:
            return HandRank.THREE_OF_A_KIND
        if countscounts[2] == 2:
            return HandRank.TWO_PAIR
        if countscounts[2] == 1:
            return HandRank.ONE_PAIR
        return HandRank.HIGH_CARD

@total_ordering
class JokerHand:
    def __init__(self, cards: str, score: int):
        self.cards = cards.strip()
        self.hands = [
            Hand(cards=cards.replace('J', r), score=score)
            for r in NON_JOKERS
        ]
        self.rank = max(h.rank for h in self.hands)
        self.score = int(score)

    def __repr__(self) -> str:
        return f"Hand({self.cards}, {self.rank}, {self.score})"

    def __eq__(self, other: Self) -> bool:
        return self.cards == other.cards

    def __lt__(self, other: Self) -> bool:
        if self.rank != other.rank:
            return self.rank < other.rank
        for mine, theirs in zip(self.cards, other.cards):
            if mine != theirs:
                return JOKER_CARD_VALUES[mine] < JOKER_CARD_VALUES[theirs]
        raise ValueError(f"{self} and {other} are the same hand.")


def parse_line_into_hand(line: str) -> Hand:
    cards, score = line.split()
    return Hand(cards=cards, score=score)

def parse_line_into_joker_hand(line: str) -> Hand:
    cards, score = line.split()
    return JokerHand(cards=cards, score=score)


if __name__ == '__main__':
    data: List[str] = [
        line.strip()
        for line in get_data(day=7, year=2023).split('\n')
    ]

    # Part 1.
    hands: List[Hand] = [parse_line_into_hand(line) for line in data]
    hands = sorted(hands)
    score = sum(
        rank*hand.score for rank, hand in  enumerate(hands, start=1)
    )
    print(f"Your total score is: {score}")

    # Part 2.
    hands: List[JokerHand] = [parse_line_into_joker_hand(line) for line in data]
    hands = sorted(hands)
    score = sum(
        rank*hand.score for rank, hand in  enumerate(hands, start=1)
    )
    print(f"Your total score is: {score}")