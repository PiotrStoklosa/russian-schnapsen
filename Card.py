class Card:
    card_rank = ["NINE", "TEN", "JACK", "QUEEN", "KING", "ACE"]
    NINE = 0
    TEN = 1
    JACK = 2
    QUEEN = 3
    KING = 4
    ACE = 5

    card_suit = ["SPADE", "CLUB", "DIAMOND", "HEART"]
    SPADE = 0
    CLUB = 1
    DIAMOND = 2
    HEART = 3

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.card_rank[self.rank] + '-' + self.card_suit[self.suit]


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
