import random

from Card import Card


class PlayerDeck:
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        return ', '.join([str(x) for x in self.cards])


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
        deck1 = PlayerDeck(self.cards[:8])
        deck2 = PlayerDeck(self.cards[8:16])
        deck3 = PlayerDeck(self.cards[16:])
        return deck1, deck2, deck3
