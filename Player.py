from Card import CardValue, Card


class Player:
    def __init__(self, player_deck):
        self.player_deck = player_deck
        self.points = 0
        self.bid = True
        self.limit = 100

    def play_card(self, index):
        return self.player_deck.throw_a_card(index)

    def accept_central_deck(self, central_deck):
        self.player_deck.accept_central_deck(central_deck)

    def spare_card(self, player1, player2):
        player1.accept_card(self.play_card(0))
        player2.accept_card(self.play_card(0))
        self.player_deck.cards = sorted(self.player_deck.cards)

    def accept_card(self, card):
        self.player_deck.accept_card(card)
        self.player_deck.cards = sorted(self.player_deck.cards)

    def cards_to_play_according_to_best_card(self, card, atu):
        filtered = list(filter(lambda x: card.lower_in_suit(x), self.player_deck.cards))
        if filtered:
            return filtered
        filtered = list(filter(lambda x: card.same_suit(x.suit), self.player_deck.cards))
        if filtered:
            return filtered
        if atu is not None:
            filtered = list(filter(lambda x: x.same_suit(atu), self.player_deck.cards))
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

    def find_best_card(self, cards_used, cards_threw, atu, is_player):
        if is_player:
            return 0
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
