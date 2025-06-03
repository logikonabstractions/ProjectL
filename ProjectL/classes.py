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
        # New: Extract the minimal shape (trim surrounding zeros) for easier rotation and placement
        minimal_shape = self.get_minimal_shape(self.shape)

        # New: Generate all 4 possible rotations of the minimal shape
        rotations = [
            minimal_shape,  # 0° (original)
            np.rot90(minimal_shape, 1),  # 90°
            np.rot90(minimal_shape, 2),  # 180°
            np.rot90(minimal_shape, 3)  # 270°
        ]

        # New: For each rotation, generate all valid translated positions within 5x5
        configurations_arrays = []
        for rotated_shape in rotations:
            configs = self.generate_configurations(rotated_shape)
            configurations_arrays.extend(configs)

        # Existing: Remove duplicates by comparing byte representations
        unique_configs = []
        for config in configurations_arrays:
            if not any(np.array_equal(config, existing) for existing in unique_configs):
                unique_configs.append(config)

        self.configurations_array = unique_configs

        # Existing: Stack into a cube if there are valid configurations
        if unique_configs:
            self.cube = np.stack(unique_configs, axis=0)
        else:
            self.cube = np.array([])  # Empty if no valid configs (edge case)

    # New helper method: Extracts the minimal bounding box of the shape (removes outer zeros)
    def get_minimal_shape(self, array):
        """Extract the minimal bounding box of the non-zero elements in the array."""
        rows = np.any(array, axis=1)
        cols = np.any(array, axis=0)
        if not np.any(rows) or not np.any(cols):
            return np.array([])  # Empty shape
        ymin, ymax = np.where(rows)[0][[0, -1]]
        xmin, xmax = np.where(cols)[0][[0, -1]]
        return array[ymin:ymax + 1, xmin:xmax + 1]

    # New helper method: Replaces generate_rolled_arrays and processe_arrays
    # Generates all valid 5x5 configurations by placing the (rotated) minimal shape at every possible position
    def generate_configurations(self, minimal_shape):
        """For a given (rotated) minimal shape, generate all possible translations within a 5x5 grid."""
        if minimal_shape.size == 0:
            return []  # No configurations for empty shape

        h, w = minimal_shape.shape
        configurations = []

        # Iterate over all possible top-left positions where the shape fits
        for i in range(5 - h + 1):
            for j in range(5 - w + 1):
                # Create a 5x5 zero array and place the minimal shape at (i, j)
                config = np.zeros((5, 5), dtype=int)
                config[i:i + h, j:j + w] = minimal_shape
                configurations.append(config)

        return configurations


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
