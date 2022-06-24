class Card:
    card_rank = ["9", "J", "Q", "K", "10", "A"]
    NINE = 0
    JACK = 1
    QUEEN = 2
    KING = 3
    TEN = 4
    ACE = 5

    card_suit = ["\u2660", "\u2663", "\u2666", "\u2665"]
    SPADE = 0
    CLUB = 1
    DIAMOND = 2
    HEART = 3

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.card_rank[self.rank] + self.card_suit[self.suit]

    def __lt__(self, obj):
        return self.rank < obj.rank or self.rank == obj.rank and self.suit < obj.suit

    def __gt__(self, obj):
        return self.rank > obj.rank or self.rank == obj.rank and self.suit > obj.suit

    def __le__(self, obj):
        return self.rank < obj.rank or self.rank == obj.rank and self.suit <= obj.suit

    def __ge__(self, obj):
        return self.rank > obj.rank or self.rank == obj.rank and self.suit >= obj.suit

    def __eq__(self, obj):
        return self.rank == obj.rank and self.suit == obj.suit

    def __repr__(self):
        return self.card_rank[self.rank] + self.card_suit[self.suit]


class CardValue:
    NINE = 0
    TEN = 10
    JACK = 2
    QUEEN = 3
    KING = 4
    ACE = 11

    SPADE_MARRIAGE = 40
    CLUB_MARRIAGE = 60
    DIAMOND_MARRIAGE = 80
    HEART_MARRIAGE = 100

