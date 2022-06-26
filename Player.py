from Card import CardValue


class Player:
    def __init__(self, player_deck):
        self.player_deck = player_deck
        self.points = 0
        self.bid = True
        self.limit = 100

    def play_card(self, index):
        return self.player_deck.throw_a_card(index)

    def declare_spade_marriage(self, queen_index):
        if self.player_deck.has_spade_marriage():
            if self.player_deck.is_queen_spade(queen_index):
                self.points += CardValue.SPADE_MARRIAGE
                self.player_deck.throw_a_card(queen_index)
            else:
                print("You can't declare marriage with this card!")
        else:
            print("You can't declare this marriage! You don't have queen and king spade!")

    def declare_club_marriage(self, queen_index):
        if self.player_deck.has_club_marriage():
            if self.player_deck.is_queen_club(queen_index):
                self.points += CardValue.CLUB_MARRIAGE
                self.player_deck.throw_a_card(queen_index)
            else:
                print("You can't declare marriage with this card!")
        else:
            print("You can't declare this marriage! You don't have queen and king club!")

    def declare_diamond_marriage(self, queen_index):
        if self.player_deck.has_diamond_marriage():
            if self.player_deck.is_diamond_heart(queen_index):
                self.points += CardValue.DIAMOND_MARRIAGE
                self.player_deck.throw_a_card(queen_index)
            else:
                print("You can't declare marriage with this card!")
        else:
            print("You can't declare this marriage! You don't have queen and king diamond!")

    def declare_heart_marriage(self, queen_index):
        if self.player_deck.has_heart_marriage():
            if self.player_deck.is_queen_heart(queen_index):
                self.points += CardValue.HEART_MARRIAGE
                self.player_deck.throw_a_card(queen_index)
            else:
                print("You can't declare marriage with this card!")
        else:
            print("You can't declare this marriage! You don't have queen and king heart!")

    def accept_central_deck(self, central_deck):
        self.player_deck.accept_central_deck(central_deck)

    def accept_card(self, card):
        self.player_deck.accept_card(card)

    def cards_to_play_according_to_best_card(self, card, atu):
        filtered = list(filter(lambda x: card.lower_in_suit(x), self.player_deck.cards))
        if filtered:
            return filtered
        filtered = list(filter(lambda x: card.same_suit(x.suit), self.player_deck.cards))
        if filtered:
            return filtered
        if atu is not None:
            filtered = list(filter(lambda x: card.same_suit(atu), self.player_deck.cards))
            if filtered:
                return filtered
        return self.player_deck.cards

    def cards_to_play(self, cards_threw, atu):
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
        self.limit = 120

    def find_best_card(self, cards_used, cards_threw, atu, is_player):
        if is_player:
            return 0
        possible_cards = self.cards_to_play(cards_threw, atu)
        for i in range(len(self.player_deck.cards)):
            if possible_cards[0] == self.player_deck.cards[i]:
                return i

    def __str__(self):
        return self.player_deck.__str__()
