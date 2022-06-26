from unittest import TestCase

from Card import Card
from Game import Game


class TestGame(TestCase):
    def test_indicate_winner(self):
        g = Game()
        g.atu_color = Card.CLUB
        winner = g.indicate_winner(Card(Card.QUEEN, Card.CLUB), Card(Card.JACK, Card.CLUB), Card(Card.ACE, Card.CLUB))
        assert winner == 2
