import random

from Card import Card


class PlayerDeck:
    def __init__(self, cards):
        self.cards = sorted(cards)

    def __str__(self):
        return ', '.join([str(x) for x in self.cards])

    def throw_a_card(self, index):
        return self.cards.pop(index)

    def has_spade_marriage(self):
        return Card.QUEEN * 4 + Card.SPADE in self.cards \
               and Card.KING + Card.SPADE in self.cards

    def has_club_marriage(self):
        return Card.QUEEN * 4 + Card.CLUB in self.cards \
               and Card.KING + Card.CLUB in self.cards

    def has_diamond_marriage(self):
        return Card.QUEEN * 4 + Card.DIAMOND in self.cards \
               and Card.KING + Card.DIAMOND in self.cards

    def has_heart_marriage(self):
        return Card.QUEEN * 4 + Card.HEART in self.cards \
               and Card.KING + Card.HEART in self.cards

    def has_marriage(self):
        return self.has_spade_marriage() \
               or self.has_club_marriage() \
               or self.has_diamond_marriage() \
               or self.has_heart_marriage()

    def is_queen_spade(self, queen_index):
        return self.cards[queen_index].rank == Card.QUEEN \
               and self.cards[queen_index].suit == Card.SPADE

    def is_queen_club(self, queen_index):
        return self.cards[queen_index].rank == Card.QUEEN \
               and self.cards[queen_index].suit == Card.CLUB

    def is_queen_diamond(self, queen_index):
        return self.cards[queen_index].rank == Card.QUEEN \
               and self.cards[queen_index].suit == Card.DIAMOND

    def is_queen_heart(self, queen_index):
        return self.cards[queen_index].rank == Card.QUEEN \
               and self.cards[queen_index].suit == Card.HEART


class WholeDeck:
    cards = []

    def __init__(self):
        for i in range(24):
            self.cards.append(Card(i // 4, i % 4))

    def __str__(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

    def generate_players_decks(self):
        deck1 = PlayerDeck(self.cards[:7])
        deck2 = PlayerDeck(self.cards[7:14])
        deck3 = PlayerDeck(self.cards[14:22])
        central_deck = PlayerDeck(self.cards[22:])
        return deck1, deck2, deck3, central_deck
