from unittest import TestCase

from Card import Card
from Deck import PlayerDeck
from Player import Player


class TestPlayer(TestCase):
    def test_cards_to_play(self):
        p = Player(PlayerDeck([Card(Card.NINE, Card.SPADE), Card(Card.KING, Card.SPADE)]))
        cards_to_play = p.cards_to_play([Card(Card.QUEEN, Card.SPADE)], None)
        assert cards_to_play == [Card(Card.KING, Card.SPADE)]