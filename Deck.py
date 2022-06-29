import random

from Card import Card, card, card_value


class PlayerDeck:
    def __init__(self, cards):
        self.cards = sorted(cards)

    def __str__(self):
        return ', '.join([str(x) for x in self.cards])

    def throw_a_card(self, index):
        return self.cards.pop(index)

    def accept_card(self, c):
        self.cards.append(c)

    def accept_central_deck(self, central_deck):
        self.cards += central_deck.cards

    def has_spade_marriage(self):
        return Card.QUEEN * 4 + Card.SPADE in map(card_value, self.cards) \
               and Card.KING + Card.SPADE in map(card_value, self.cards)

    def has_club_marriage(self):
        return card(Card.QUEEN, Card.CLUB) in map(card_value, self.cards) \
               and card(Card.KING, Card.CLUB) in map(card_value, self.cards)

    def has_diamond_marriage(self):
        return card(Card.QUEEN, Card.DIAMOND) in map(card_value, self.cards) \
               and card(Card.KING, Card.DIAMOND) in map(card_value, self.cards)

    def has_heart_marriage(self):
        return card(Card.QUEEN, Card.HEART) in map(card_value, self.cards) \
               and card(Card.KING, Card.HEART) in map(card_value, self.cards)

    def has_marriage(self):
        return self.has_spade_marriage() \
               or self.has_club_marriage() \
               or self.has_diamond_marriage() \
               or self.has_heart_marriage()


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
        deck3 = PlayerDeck(self.cards[14:21])
        central_deck = PlayerDeck(self.cards[21:])
        return deck1, deck2, deck3, central_deck


class PartDeck:
    cards = []

    def throw_a_card(self, index):
        return self.cards.pop(index)

    def __init__(self, cards_excluded):
        self.cards = []
        for i in range(24):
            c = Card(i // 4, i % 4)
            if c not in cards_excluded:
                self.cards.append(Card(i // 4, i % 4))

    def generate_players_random_decks(self):
        round_count = len(self.cards) // 2
        deck1 = PlayerDeck(self.cards[:round_count])
        deck2 = PlayerDeck(self.cards[round_count:])
        return deck1, deck2
