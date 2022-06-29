import copy
import random

import Game
from Card import CardValue, Card
from Deck import PartDeck, PlayerDeck


class Player:
    def __init__(self, player_deck):
        self.player_deck = player_deck
        self.points = 0
        self.bid = True
        self.limit = 100

    def play_card(self, card):
        return self.player_deck.throw_a_card(self.player_deck.cards.index(card))
        # for i in range(len(self.player_deck.cards)):
        #     if self.player_deck.cards[i] == card:
        #         return self.player_deck.throw_a_card(i)

    def play_card_from_index(self, index):
        return self.player_deck.throw_a_card(index)

    def accept_central_deck(self, central_deck):
        self.player_deck.accept_central_deck(central_deck)

    def spare_card(self, player1, player2):
        player1.accept_card(self.play_card_from_index(0))
        player2.accept_card(self.play_card_from_index(0))
        self.player_deck.cards = sorted(self.player_deck.cards)

    def accept_card(self, card):
        self.player_deck.accept_card(card)
        self.player_deck.cards = sorted(self.player_deck.cards)

    def cards_to_play_according_to_best_card(self, card, atu):
        filtered = list(filter(lambda x: card.lower_in_suit(x), self.player_deck.cards))
        if filtered:
            return sorted(filtered)
        filtered = list(filter(lambda x: card.same_suit(x.suit), self.player_deck.cards))
        if filtered:
            return sorted(filtered)
        if atu is not None:
            filtered = list(filter(lambda x: x.same_suit(atu), self.player_deck.cards))
            if filtered:
                return sorted(filtered)
        return sorted(self.player_deck.cards)

    def cards_to_play(self, cards_threw, atu):
        if not cards_threw:
            return self.player_deck.cards
        if len(cards_threw) == 1:
            return self.cards_to_play_according_to_best_card(cards_threw[0], atu)
        else:
            first_card = cards_threw[0]
            second_card = cards_threw[1]
            if atu is None or first_card.suit != atu and second_card.suit != atu:
                if first_card.stronger_without_atu(second_card):
                    return self.cards_to_play_according_to_best_card(first_card, atu)
                return self.cards_to_play_according_to_best_card(second_card, atu)
            else:
                if first_card.suit == atu:
                    if second_card.suit == atu:
                        if first_card.stronger_without_atu(second_card):
                            return self.cards_to_play_according_to_best_card(first_card, atu)
                        return self.cards_to_play_according_to_best_card(second_card, atu)
                    return self.cards_to_play_according_to_best_card(first_card, atu)
                return self.cards_to_play_according_to_best_card(second_card, atu)

    def note_limitation_bidding(self):
        l = 0
        for i in self.player_deck.cards:
            match i.rank:
                case Card.ACE:
                    l += 25
                case Card.TEN:
                    l += 20 if Card(Card.ACE, i.suit) in self.player_deck.cards else 5
                case Card.QUEEN:
                    match i.suit:
                        case Card.SPADE:
                            l += CardValue.SPADE_MARRIAGE if Card(Card.KING, i.suit) in self.player_deck.cards else 7
                        case Card.CLUB:
                            l += CardValue.CLUB_MARRIAGE if Card(Card.KING, i.suit) in self.player_deck.cards else 11
                        case Card.DIAMOND:
                            l += CardValue.DIAMOND_MARRIAGE if Card(Card.KING, i.suit) in self.player_deck.cards else 15
                        case Card.HEART:
                            l += CardValue.HEART_MARRIAGE if Card(Card.KING, i.suit) in self.player_deck.cards else 19
                case Card.KING:
                    match i.suit:
                        case Card.SPADE:
                            l += 8
                        case Card.CLUB:
                            l += 12
                        case Card.DIAMOND:
                            l += 16
                        case Card.HEART:
                            l += 20
                case Card.JACK:
                    l += 10 if Card(Card.ACE, i.suit) in self.player_deck.cards else -5

        # print("With deck: ")
        # for c in self.player_deck.cards:
        #     print(c, end=' ')
        # print()
        # print("I got " + str(round(l, -1)) + " points!\n\n\n")
        self.limit = 100 if round(l, -1) < 100 else round(l, -1)

    def simulate_random_games(self, random_games, cards_used, atu, points_to_win):
        best_card = None
        most_wins = -1
        for c in range(len(self.player_deck.cards)):
            won_games = 0
            for i in range(random_games):
                pd = PartDeck(cards_used + self.player_deck.cards)
                player_decks = pd.generate_players_random_decks()
                # players = [Player(PlayerDeck(sorted(copy.deepcopy(self.player_deck.cards)))),
                players = [Player(PlayerDeck(copy.deepcopy(self.player_deck.cards))),
                           Player(player_decks[0]),
                           Player(player_decks[1])]
                card1 = players[0].play_card_from_index(c)

                cards_threw = [card1]

                if cards_threw[0].rank == Card.QUEEN:
                    if players[0].declare_potential_marriage(cards_threw[0].suit):
                        atu = cards_threw[0].suit

                cards_to_play = players[1].cards_to_play(cards_threw, atu)
                random_card = cards_to_play[random.randrange(0, len(cards_to_play))]
                cards_threw.append(players[1].play_card(random_card))

                cards_to_play = players[2].cards_to_play(cards_threw, atu)
                random_card = cards_to_play[random.randrange(0, len(cards_to_play))]
                cards_threw.append(players[2].play_card(random_card))

                winner = Game.indicate_winner(cards_threw[0], cards_threw[1], cards_threw[2], atu)
                players[winner].points += CardValue.card_values[cards_threw[0].rank] + \
                                          CardValue.card_values[
                                              cards_threw[1].rank] + CardValue.card_values[
                                              cards_threw[2].rank]
                current_player = winner
                while players[current_player].player_deck.cards:
                    cards_threw = []

                    cards_to_play = players[current_player].cards_to_play(cards_threw, atu)
                    random_card = cards_to_play[random.randrange(0, len(cards_to_play))]
                    cards_threw.append(players[winner].play_card(random_card))

                    if cards_threw[0].rank == Card.QUEEN:
                        if players[winner].declare_potential_marriage(cards_threw[0].suit):
                            atu = cards_threw[0].suit

                    cards_to_play = players[(winner+1) % 3].cards_to_play(cards_threw, atu)
                    if len(cards_to_play) < 0:
                        print("t")
                    random_card = cards_to_play[random.randrange(0, len(cards_to_play))]
                    cards_threw.append(players[(winner+1) % 3].play_card(random_card))

                    cards_to_play = players[(winner+2) % 3].cards_to_play(cards_threw, atu)
                    random_card = cards_to_play[random.randrange(0, len(cards_to_play))]
                    cards_threw.append(players[(winner+2) % 3].play_card(random_card))

                    winner = Game.indicate_winner(cards_threw[0], cards_threw[1], cards_threw[2], atu)

                    players[(winner + current_player) % 3].points += CardValue.card_values[cards_threw[0].rank] + \
                                                                     CardValue.card_values[
                                                                         cards_threw[1].rank] + CardValue.card_values[
                                                                         cards_threw[2].rank]
                    current_player = winner

                if players[0].points >= points_to_win:
                    won_games += 1
            if won_games > most_wins:
                best_card = self.player_deck.cards[c]
                most_wins = won_games

        print(best_card)
        print(most_wins)

        for i in range(len(self.player_deck.cards)):
            if best_card == self.player_deck.cards[i]:
                return i

    def find_best_card(self, cards_used, cards_threw, atu, is_player):
        if is_player:
            return self.simulate_random_games(10, cards_used, atu, self.limit - self.points)
        possible_cards = self.cards_to_play(cards_threw, atu)
        for i in range(len(self.player_deck.cards)):
            if possible_cards[0] == self.player_deck.cards[i]:
                return i

    def declare_potential_marriage(self, suit):
        if Card(Card.KING, suit) in self.player_deck.cards:
            print("Declared " + Card.card_suit[suit] + " marriage and this suit is now atu!")
            self.points += CardValue.marriage_values[suit]
            return True
        return False

    def __str__(self):
        return self.player_deck.__str__()
