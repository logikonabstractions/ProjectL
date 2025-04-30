import random
from ProjectL.actions import *


class Strategy:
    """ making it possible to either implement fixed sequences of actions, or make decisions that
        fa0vor some directions etc... Use by the Player class
    """
    def __init__(self, player, actions_sequence=None, action_list=None):
        self.player = player                # need a ref to player or player state in order to make in-game decisions
        self.action_sequence = actions_sequence if actions_sequence else ()      # predetermined action sequences if applicable to sthis strat
        self.actions = action_list if action_list else (TakePiece, PlacePiece, UpgradePiece,  TakeCard, Master)
        self.actions_left = 3

    def play_turn(self):
        raise NotImplemented

    @property
    def pieces(self):
        return self.player.pieces
    @property
    def cards(self):
        return self.player.cards
    @cards.setter
    def cards(self, value):
        self.player.cards = value
    @property
    def full_cards(self):
        return self.player.full_cards
    @full_cards.setter
    def full_cards(self, value):
        self.player.full_cards = value
    @property
    def name(self):
        return self.player.name

class RandomStrat(Strategy):
    """ just chooses stuff at random."""

    def __init__(self, player, **kwargs):
        super().__init__(player, **kwargs)

    def choose_action(self):
        """ decides what the player does this turn"""
        action_selected = random.choice(self.actions)(pieces=self.pieces, cards=self.cards)
        self.actions_left -= 1
        return action_selected

    def play_turn(self):
        self.actions_left = 3
        while self.actions_left > 0:
            print(f"{self.name} chooses and action...")
            action = self.choose_action()
            print(f"Action: {action}")
            valid_action = False
            while not valid_action:             # ensure we choose a valid action for that part of a turn
                if action.is_action_valid():
                    valid_action = True
                    result = action.perform_action()
                else:
                    print(f"Action not valid - choosing another... {action}")
                    action = self.choose_action()
                    valid_action = action.is_action_valid()
            print(f"{self}")
        print(f"{self.name} has no action left.")
        print(f"{self}")


class BasicStrat(Strategy):
    """ a pre-determined sequence of 3 actions that we just repeat:
        1 - if card & piece, place a piece
        2 - Take a piece if no pieces
        3 - take a card if no card
        4 - do that until EOT
     """

    def __init__(self, player, **kwargs):
        super().__init__(player, **kwargs)

    def play_turn(self):
        self.actions_left = 3
        # sort out full cards, TODO: handle that better
        if any(card.is_full for card in self.cards):
            self.full_cards.extend(card for card in self.cards if card.is_full)
            self.cards = [card for card in self.cards if not card.is_full]

        while self.actions_left > 0 :
            # place if you can
            if self.cards and self.pieces:
                piece = self.pieces.pop()
                action = PlacePiece(piece, self.cards[0])
                result = action.perform_action()
                if result:
                    self.actions_left -= 1
                    # also check if card is full, is so, move to full cards


                else:
                    action = TakePiece(pieces=self.pieces)        # we couldn't place, perform backup action
                    action.perform_action()
                    self.actions_left -= 1
            elif not self.pieces:
                action = TakePiece(pieces=self.pieces)
                action.perform_action()
                self.actions_left -= 1

            elif not self.cards:
                action = TakeCard(cards=self.cards)
                result = action.perform_action()
                if result:
                    self.actions_left -= 1
                else:
                    action = TakePiece(pieces=self.pieces)        # we couldn't place, perform backup action
                    action.perform_action()
