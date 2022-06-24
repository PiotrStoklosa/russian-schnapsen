from Card import CardValue


class Player:
    def __init__(self, player_deck):
        self.player_deck = player_deck
        self.points = 0

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

    def __str__(self):
        return self.player_deck.__str__()
