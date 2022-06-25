from Deck import WholeDeck
from Player import Player


class Game:
    def __init__(self):
        self.central_deck = None
        self.players = []
        self.atu_color = None
        self.limit = 100
        self.turn = 0
        self.player = 0
        print("Starting game...")

    def deal(self):
        deck = WholeDeck()
        deck.shuffle()
        decks = deck.generate_players_decks()
        self.players.append(Player(decks[0]))
        self.players.append(Player(decks[1]))
        self.players.append(Player(decks[2]))
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
        while self.players[0].player_deck.cards:
            if self.turn == 0:
                print("Choose a card to play")
                print(self.players[0].__str__())
                for i in range(1, len(self.players[0].player_deck.cards) + 1):
                    print(i, end='   ')
                print()
                response = input()
                response = int(response)
                self.players[0].play_card(response - 1)
