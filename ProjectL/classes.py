import logging
import random

import numpy as np

from ProjectL.utils import plot_image


class Action:
    """ encapsulates everything an action does - check validity based on card or game state

        Actions can have side effects - they may act on objects passed on to them as arguments.
        Exemples:
            - adding a piece to pieces or card to cards
            - modifying a piece or a card that was passed to it
    """
    def __init__(self, piece=None, card=None, pieces = None, cards=None):
        self.logger = logging.getLogger(__name__)
        self.desc = "action"
        self.piece = piece
        self.card = card
        self.pieces = pieces
        self.cards = cards

    def is_action_valid(self, *args, **kwargs):
        is_valid = False
        self.logger.debug(f"Checking validity of {self.desc}: {is_valid}")  # Detailed
        if FULL_DEBUG and not is_valid:
            self.logger.debug(f"Invalid reason: [context, e.g., no piece/card]")  # Extra for tracing issues
        return is_valid


    def perform_action(self, *args, **kwargs):
        """ performs the action. Will produce side-effect on objects that have been passed to the action -
            e.g. update the Card if a valid piece has been placed, changes the piece if we upgrade it, etc.
        """
        pass

    def __str__(self):
        return self.desc


class TakePiece(Action):
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Take a Piece"

    def perform_action(self):
        """ selects an available piece and returns it
        """


        self.logger.debug(f"Performing {self.desc}")  # Detailed
        # Original logic, with added try-except for errors
        try:
            # choose a piece, for now only Square pieces
            piece = PieceSquare()
            self.pieces.append(piece)
        except Exception as e:
            self.logger.error(f"Error performing {self.desc}: {e}")  # Error logging for robustness


    def is_action_valid(self):
        """ This action is always valid we return True all the time
            :return: True
        """
        return True


class PlacePiece(Action):
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Place a piece"


    def perform_action(self, configuration=None):
        """

        """
        self.logger.debug(f"Performing {self.desc}")  # Detailed
        # Original logic, with added try-except for errors
        try:
            if configuration is None:
                config_no = random.randint(0,self.piece.cube.shape[0]-1)
                configuration = self.piece.cube[config_no,:,:]
            if self.is_action_valid():
                result = self.card.place_piece(configuration)
                return result
            else:
                return False
            # ... existing code ...
        except Exception as e:
            self.logger.error(f"Error performing {self.desc}: {e}")  # Error logging for robustness


    def is_action_valid(self):
        """ must have a piece and a card that is not full
        """
        if self.piece is None:
            # randomly select a piece to be placed as none provided
            if self.pieces:
                self.piece = random.choice(self.pieces)
            else:
                return False        # cannot place a piece if we have none
        if self.card is None:
            # same
            if self.cards:
                self.card = random.choice(self.cards)
            else:
                return False
        return self.card is not None and self.piece is not None


class UpgradePiece(Action):
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Upgrade a piece"
        if self.piece is None:
            self.piece = random.choice(self.pieces)


class TakeCard(Action):
    def __init__(self, piece=None, card=None, pieces = None, cards=None, **kwargs):
        super().__init__(piece, card, pieces, cards, **kwargs)
        self.desc = "Take a card"

    def perform_action(self):
        """ selects a possible piece and returns it
        """
        # choose a piece
        card = Card()
        self.cards.append(card)


    def is_action_valid(self):
        """ checks if we can take a card. This action is always valid we return True all the time
            :return: True
        """

        #TODO: check this
        if len(self.cards) >= 1:
            return False

        return True


class Master(Action):
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Master"


class Reward:
    """
        Describes what we get for finishing a card. Points and/or a piece
    """
    def __init__(self, points = 0, piece = None):
        self.points = points
        self.piece = piece if piece else PieceSquare()


class Card:
    """ Describes the different cards we can play with.

        layout: the numpy array that describes the state of the card (1 = occupied, 0 = empty for each square)
        reward: the object that describes what piece / points we get for completing the card
        mask: a bool numpy array that describes the playable structure of that card within the maximal matrix
    """
    def __init__(self, configs = None):
        if configs:
            self.layout = np.zeros(shape=(5, 5), dtype=int)
            self.mask = np.array(configs["mask"])
            self.reward = Reward(points=configs["reward"]["points"], piece=configs["reward"]["piece"])
        else:
            self.layout = np.zeros(shape=(5, 5), dtype=int)
            self.mask = np.array([[False,False,True,True,False,], [False,False,True,True,False], [False,False,True,True,False], [False,False,False,False,False], [False,False,False,False,False], ])
            self.reward = Reward()
        self.is_full = False


    def place_piece(self, configuration):
        """
            places the provided piece on the card at a given position. returns T/F for success
            piece: a Piece object to be placed on the current card
            configuration: a description of where on the card to place the piece
        """

        if self.placement_valid(configuration):
            self.layout += configuration            # update the layout
            if np.all((self.layout == 1) == self.mask):
                self.is_full = True
            return True
        else:
            return False

    def placement_valid(self, configuration):
        """ checks if the placement of the piece on this card is valid. conditions:
            - no position on self.layout > 1 after self.layout += configuration
            - no bit of configuration falls on a region where the mask is false

        """
        # check config within the mask
        result = self.layout + configuration
        out_sum = np.sum(result[~self.mask])     # should sum to zero

        # check no overlap with already placed piece
        double_occupation = np.any(result > 1)

        return out_sum == 0 and not double_occupation


class Piece:
    """describes a Piece that a Player can place on a Card"""

    def __init__(self, configs = None):
        self.level = None
        self.shape = None
        self.name = None
        self.configurations_array = []
        self.cube = None
        if configs:
            self.level = configs["level"]
            self.shape = np.array(configs["shape"])
            self.name = configs["name"]
            self.configurations_array = []
            self.cube = None
            self.generate_cube()


    def generate_cube(self):
        """ To be efficient in computation, we represent each Piece as a 3D matrix.

            The 3rd axis of the matrix represents all the possible configuration of the Piece.

            They are laid onto a (i, j) matrice of the same dimension as the largest possible
            dimension of a card.
        """
        configurations_arrays = [self.shape]  # what we're trying to generate here; all the translations/rotations of tat piece on a card
        unprocessed_arrays = [self.shape]  # need to roll all of those
        generated_configurations = []  # new ones, just to avoid modifying a list we're iterating on (unprocessed_arrays). adding new arrays here

        while len(generated_configurations) + len(unprocessed_arrays) > 0:
            generated_configurations = self.processe_arrays(unprocessed_arrays)

            # for idx, _ in enumerate(generated_configurations):
            #     print(f"\nConfiguration:\n {_} idx: {idx}")

            to_remove = []
            for idx, new_arr in enumerate(generated_configurations):
                if any([arr.tobytes() == new_arr.tobytes() for arr in configurations_arrays]):  # duplicate matrice
                    to_remove.append(idx)

            for id in reversed(to_remove):
                generated_configurations.pop(id)
            unprocessed_arrays = generated_configurations
            configurations_arrays += generated_configurations
            self.configurations_array = configurations_arrays
        # self.plot_configurations()
        self.cube = np.stack(self.configurations_array, axis=0)
        # self.validate_cube()

    def processe_arrays(self, unprocessed_arrays):
        new_rolled_arrays = []
        while unprocessed_arrays:
            candidate_positions = self.generate_rolled_arrays(unprocessed_arrays.pop())
            for candidate in candidate_positions:
                if any([arr.tobytes() == candidate.tobytes() for arr in new_rolled_arrays]):    # duplicate matrice
                    # plot_image(candidate, f"Candidate already in configurations")
                    pass
                else:
                    new_rolled_arrays.append(candidate)
            # print(f"New rolled arrays: {len(new_rolled_arrays)}")
            # print(f"unprocessed_arrays : {len(unprocessed_arrays)}")
            # print(f"Configurations: {len(self.configurations_array)}")
        return new_rolled_arrays

    def generate_rolled_arrays(self, array):
        """ from the give array, generate all rolled arrays that are valid for Project L from the given array

            Translates the piece to the right (by rolling matrice indices). Checks that the resulting matrice is valid
            for the game.
        """
        new_arrays = []
        temp = array
        # rolling the columns to the right
        while np.sum(temp[:, -1]) == 0:
            temp = np.roll(temp, 1, axis=1)
            new_arrays.append(temp)

        # rolling the rows down = but need to re-initialize temp to array
        temp = array
        while np.sum(temp[-1, :]) == 0:
            temp = np.roll(temp, 1, axis=0)
            new_arrays.append(temp)

        return new_arrays

    def plot_configurations(self):
        """ for debug - plots the configurations for our piece """
        for idx, arr in enumerate(self.configurations_array):
            plot_image(arr, f"Configuration {idx}/{len(self.configurations_array)}")

    def validate_cube(self):
        summed_matrix = np.sum(self.cube, axis=0)
        # plot_image(summed_matrix, self.name)

    def __repr__(self):
        return self.name


class PieceSquare(Piece):
    """ a subclass for easy access to a basic piece, e.g. a simpe square"""

    def __init__(self):
        configs = {"name": "square_1", "level": 1, "shape": [[1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}
        super().__init__(configs)
        # self.level = configs["level"]
        # self.shape = np.array(configs["shape"])
        # self.name = configs["name"]
        # self.configurations_array = []
        # self.cube = None
        # self.generate_cube()
