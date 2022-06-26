from Card import CardValue, Card
from Deck import WholeDeck
from Player import Player


def indicate_winner_without_atu(card1, card2, card3):
    if card1.stronger_without_atu(card2):
        if card1.stronger_without_atu(card3):
            return 0
        return 2
    if card2.stronger_without_atu(card3):
        return 1
    return 2


class Game:
    def __init__(self):
        self.central_deck = None
        self.players = []
        self.atu_color = None
        self.limit = 100
        self.turn = 0
        self.player = 0
        print("Starting game...")

    def indicate_winner(self, card1, card2, card3):
        if self.atu_color is None:
            return indicate_winner_without_atu(card1, card2, card3)
        if card1.suit == self.atu_color:
            if card2.suit == self.atu_color:
                if card3.suit == self.atu_color:
                    return indicate_winner_without_atu(card1, card2, card3)
                if card1.stronger_without_atu(card2):
                    return 0
                return 1
            if card3.suit == self.atu_color:
                if card1.stronger_without_atu(card3):
                    return 0
                return 2
            return 0
        if card2.suit == self.atu_color:
            if card3.suit == self.atu_color:
                if card2.stronger_without_atu(card3):
                    return 1
                return 2
            return 1
        if card3.suit == self.atu_color:
            return 2
        return indicate_winner_without_atu(card1, card2, card3)

    def deal(self):
        deck = WholeDeck()
        deck.shuffle()
        decks = deck.generate_players_decks()
        self.players.append(Player(decks[0]))
        self.players.append(Player(decks[1]))
        self.players.append(Player(decks[2]))
        print("DECKS:")
        for i in self.players:
            print(i.__str__())
        self.central_deck = decks[3]
        print("Your cards: " + self.players[0].__str__())
        for player in self.players:
            player.note_limitation_bidding()
        active_players = 3
        print("Let's start bid! Player 3 has 100 by default")
        while active_players > 1:
            if self.turn == 0:
                print("Do you want to bid 10 more? - y - yes, n - no")
                response = input()
                if response == "y":
                    self.limit += 10
                    print("Player 1 raised to " + str(self.limit))
                else:
                    active_players -= 1
                    self.players[self.turn].bid = False
                    print("Player 1 folded")
            elif self.players[self.turn].limit > self.limit:
                self.limit += 10
                print("Player " + str(self.turn + 1) + " raised to " + str(self.limit))
            else:
                active_players -= 1
                self.players[self.turn].bid = False
                print("Player " + str(self.turn + 1) + " folded")

            self.turn = (self.turn + 1) % 3
            while not self.players[self.turn].bid:
                self.turn = (self.turn + 1) % 3
        self.player = self.turn
        print("Player " + str(self.player + 1) + " won the bidding phase with value: " + str(self.limit))
        if self.player == 0:
            print(
                "Do you want to raise limit?"
                " - value greater than 0 if yes (value you want to play, for instance 210)"
                " - 0 if no")
            response = input()
            response = int(response)
            if response > 0:
                self.limit = response
        else:
            self.limit = self.players[self.player].limit
        print("Player " + str(self.turn + 1) + " will try to get " + str(self.limit) + " points!")
        if self.limit > 100:
            print("Central deck is: ")
            for c in self.central_deck.cards:
                print(c, end=' ')
        self.players[self.player].accept_central_deck(self.central_deck)
        self.players[self.player].spare_card(self.players[(self.player + 1) % 3], self.players[(self.player + 2) % 3])
        cards_used = []

        while self.players[0].player_deck.cards:
            cards_threw = []
            print("\n\n\n")
            if self.player == 0:
                print("Choose a card to play")
                print(self.players[0].__str__())
                for i in range(1, len(self.players[0].player_deck.cards) + 1):
                    print(i, end='   ')
                print()
                response = input()
                response = int(response)
                cards_threw.append(self.players[0].play_card(response - 1))
                print(
                    "Player " + str(self.player + 1) + " played\n" + cards_threw[len(cards_threw) - 1].__str__())
            else:
                cards_threw.append(self.players[self.player].play_card(
                    self.players[self.player].find_best_card(cards_used, cards_threw, self.atu_color, True)))
                print("Player " + str(self.player + 1) + " played\n" + cards_threw[len(cards_threw) - 1].__str__())
            if cards_threw[0].rank == Card.QUEEN:
                if self.players[self.player].declare_potential_marriage(cards_threw[0].suit):
                    self.atu_color = cards_threw[0].suit
            self.turn = (self.turn + 1) % 3
            for i in range(2):
                if self.turn == 0:
                    print("Choose a card to play, Your deck")
                    print(self.players[0].__str__())
                    for i in range(1, len(self.players[0].player_deck.cards) + 1):
                        print(i, end='   ')
                    print()
                    print("cards, that you can put: ")
                    cards_to_play = self.players[0].cards_to_play(cards_threw, self.atu_color)
                    for c in cards_to_play:
                        print(c, end='')
                    print()
                    response = input()
                    response = int(response)
                    cards_threw.append(self.players[0].play_card(response - 1))
                    print(
                        "Player " + str(self.turn + 1) + " played\n" + cards_threw[len(cards_threw) - 1].__str__())
                else:
                    cards_threw.append(
                        self.players[self.turn].play_card(
                            self.players[self.turn].find_best_card(cards_used, cards_threw, self.atu_color, False)))
                    print(
                        "Player " + str(self.turn + 1) + " played\n" + cards_threw[len(cards_threw) - 1].__str__())
                self.turn = (self.turn + 1) % 3
            won_card = self.indicate_winner(cards_threw[0], cards_threw[1],
                                            cards_threw[2])
            print("Player " + str((won_card + self.turn) % 3 + 1) + " won")
            self.players[(won_card + self.turn) % 3].points += CardValue.card_values[cards_threw[0].rank] + \
                                                               CardValue.card_values[
                                                                   cards_threw[1].rank] + CardValue.card_values[
                                                                   cards_threw[2].rank]
            self.player = (won_card + self.turn) % 3
            self.turn = self.player
            cards_used += cards_threw
        print("Score:")
        print("Player1: " + str(self.players[0].points))
        print("Player2: " + str(self.players[1].points))
        print("Player3: " + str(self.players[2].points))
