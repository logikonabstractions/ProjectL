import random
import string
import numpy as np
from utils import plot_image

class GameManager:
    """ the main game engine that runs the game. """
    def __init__(self, configs_dict):
        self.configs = configs_dict
        self.configs_actions = configs_dict["game_parameters"]["actions"]
        self.configs_pieces = configs_dict["pieces"]
        
        # game parameters - extraction for easier access
        self.current_turn_number = 1
        self.max_turns = configs_dict["game_parameters"]["max_turns"]
        self.pieces = []
        self.actions = []
        
        # players        
        self.player_1 = Player(name=configs_dict["players"][0]["name"], actions=self.configs_actions)
        self.player_2 = Player(name=configs_dict["players"][1]["name"], actions=self.configs_actions)
        
        # game init
        self.game_init()
        
    def game_init(self):
        """ instantiates the pieces, cards, etc... any setup steps required for the game .
            mostly based on configs 
        """
        self.instantiate_pieces()
    
    def instantiate_pieces(self):
        """ instantiates all the pieces: loads from configs, converts to numpy arrays
            creates the objects, and plots them (For debug at least)
        """
        for piece_confs in self.configs_pieces:
            self.pieces.append(Piece(configs=piece_confs))
            
            # plot the Piece for debug
            # plot_image(self.pieces[-1].configurations_array)
    
    def run(self):
        """ loop that runs the game """
        print("Please welcome our players!")
        print(f"Player One: {self.player_1} ")
        print(f"Player Two: {self.player_2} ")
        
        print("Now let's run the game")
        while self.is_game_running():
            print(f"")
            print(f"====== Playing turn {self.current_turn_number} ======")
            self.player_1.play_turn()
            self.player_2.play_turn()
            
            # update turn number
            self.current_turn_number += 1

    def is_game_running(self):    
        """ checks if the game is running or over"""
        is_running = self.current_turn_number <= self.max_turns
        return is_running



class Player:
    """ a class that describes a player """
    def __init__(self, name=None, cards =(), pieces = (), actions = (), **kwargs):
        
        # attri. that defines the Player itself
        self.name = name if name is not None else self.generate_random_name()
        self.actions_left = 3
        
        # list of objects, game stuff
        self.cards = cards
        self.pieces = pieces
        self.actions = actions
        self.kwargs = kwargs        
        
        
        
    def play_turn(self):
        """  """
        self.actions_left = 3
        while self.actions_left > 0:
            print(f"{self.name} chooses and action...")
            print(f"Action: {self.choose_action()}")
        print(f"{self.name} has no action left.")
        
    def choose_action(self):
        """ decides what the player does this turn"""
        action_selected = random.choice(self.actions)
        self.actions_left -= 1        
        return action_selected
        
    def __repr__(self):
        return self.name

    def generate_random_name(self, length=5):
        """ just for fun - generates random names to players if none assigned """
        chars = string.ascii_lowercase
        # Generate a random name of specified length
        return ''.join(random.choice(chars) for _ in range(length))
    
class Piece:
    """describes a Piece that a Player can place on a Card"""
    
    def __init__(self, configs):
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

            for idx, _ in enumerate(generated_configurations):
                print(f"\nConfiguration:\n {_} idx: {idx}")

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
            print(f"New rolled arrays: {len(new_rolled_arrays)}")
            print(f"unprocessed_arrays : {len(unprocessed_arrays)}")
            print(f"Configurations: {len(self.configurations_array)}")
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
        summed_matrix = np.sum(self.configurations_array, axis=0)        
        plot_image(summed_matrix, self.name)
