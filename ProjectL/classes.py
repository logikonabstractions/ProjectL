import random

import numpy as np

from ProjectL.utils.utils import plot_image


class Action:
    """ encapsulates everything an action does - check validity based on card or game state

        Actions can have side effects - they may act on objects passed on to them as arguments.
        Exemples:
            - adding a piece to pieces or card to cards
            - modifying a piece or a card that was passed to it
    """
    def __init__(self, piece=None, card=None, pieces = None, cards=None, game_manager=None):
        self.desc = "action"
        self.piece = piece
        self.card = card
        self.pieces = pieces
        self.cards = cards
        self.game_manager = game_manager


    def is_action_valid(self, *args, **kwargs):
        """ checks if the action is valid
            :return: Bool
        """

        return False

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

    def perform_action(self, piece_name=None):
        """ selects an available piece from the bank and returns it
        """
        if self.game_manager:
            # Get a piece from the bank
            piece = self.game_manager.get_piece(piece_name)
            if piece:
                self.pieces.append(piece)
                return True
        else:
            # Fallback to the original behavior for backward compatibility
            piece = PieceSquare()
            self.pieces.append(piece)
            return True
        return False


    def is_action_valid(self):
        """ This action is valid if there are pieces available in the bank
        """
        if self.game_manager:
            # Check if any pieces are available in the bank
            return any(pieces for pieces in self.game_manager.piece_bank.values())
        # Fallback to original behavior
        return True

class PlacePiece(Action):
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Place a piece"


    def perform_action(self, configuration=None):
        """

        """
        if configuration is None:
            config_no = random.randint(0,self.piece.cube.shape[0]-1)
            configuration = self.piece.cube[config_no,:,:]
        if self.is_action_valid():
            result = self.card.place_piece(configuration)
            return result
        else:
            return False

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

    def __repr__(self):
        return f"Points: {self.points} with piece: {self.piece.name}"

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

    def __repr__(self):
        return f"Mask: {self.mask}, full: {self.is_full}, reward: {self.reward}"

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
        """ To be efficient in computation, we represent all the possible positions of a piece within a card as a 3D matrix.

            The axis=0 of the matrix (numpy array) represents all the possible configuration of that Piece. This method is responsible for generating all that. A valid cube must:
            1 - contain only layouts laying entirely within a card (5x5)
            2 - contain only continuous piece position (cannot overflow or wrap around)
            3 - only contain 0,1 values where 1 == a square occupied by the piecce and 0 == not occupied
            4 - all possible translations AND rotations possible must be represented by 1 slice along axis 0
            5 - there must be no duplicated layouts
        """
        # First, generate all distinct rotations of the base shape
        rotated_shapes = self.generate_rotations(self.shape)

        configurations_arrays = []  # All configurations (translations of all rotations)

        # Process each rotation
        for rotated_shape in rotated_shapes:
            # Start with the rotated shape
            unprocessed_arrays = [rotated_shape]
            rotation_configs = [rotated_shape]

            # Generate all translations for this rotation
            while unprocessed_arrays:
                generated_configurations = self.processe_arrays(unprocessed_arrays)
                to_remove = []

                # identify any duplication in generated_configurations
                for idx, new_arr in enumerate(generated_configurations):
                    if any([arr.tobytes() == new_arr.tobytes() for arr in rotation_configs]):  # duplicate matrice
                        to_remove.append(idx)

                # remove them
                for id in reversed(to_remove):
                    generated_configurations.pop(id)

                # anything left needs to be processed
                unprocessed_arrays = generated_configurations
                rotation_configs.extend(generated_configurations)

            # Add all configurations for this rotation to the main list
            configurations_arrays.extend(rotation_configs)

        # Remove any duplicates across different rotations
        unique_configurations = []
        for config in configurations_arrays:
            if not any([arr.tobytes() == config.tobytes() for arr in unique_configurations]):
                unique_configurations.append(config)

        self.configurations_array = unique_configurations
        # stacking all valid configurations generated into axis 0 so we get a cube
        self.cube = np.stack(self.configurations_array, axis=0)

    def generate_rotations(self, shape):
        """Generate all distinct rotations of the given shape.

        Returns:
            list: List of unique rotated arrays
        """
        rotations = [shape]  # Start with the original shape

        # Generate 90, 180, and 270 degree rotations
        current = shape
        for _ in range(3):  # 3 more rotations to try
            current = np.rot90(current)  # Rotate 90 degrees

            # Check if this rotation is unique
            if not any([np.array_equal(current, rot) for rot in rotations]):
                rotations.append(current.copy())

        return rotations


    def processe_arrays(self, unprocessed_arrays):
        new_rolled_arrays = []
        while unprocessed_arrays:
            candidate_positions = self.generate_rolled_arrays(unprocessed_arrays.pop())
            for candidate in candidate_positions:
                if any([arr.tobytes() == candidate.tobytes() for arr in new_rolled_arrays]):    # duplicate matrice
                    pass
                else:
                    new_rolled_arrays.append(candidate)

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
        return f"{self.name} - lvl {self.level}"


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
