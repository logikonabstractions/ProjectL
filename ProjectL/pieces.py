import numpy as np
from .utils import plot_image

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
        self.validate_cube()

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
        plot_image(summed_matrix, self.name)
        
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


class Card:

    def __init__(self):
        self.layout = np.zeros(shape=(5, 5), dtype=int)