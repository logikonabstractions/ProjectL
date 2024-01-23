import random
import string

class GameManager:
    """ the main game engine that runs the game. """
    # def __init__(self, player_1=None, player_2=None):
    def __init__(self, configs_dict):
        self.configs = configs_dict
        self.player_1 = Player(name=configs_dict["players"][0]["name"])
        self.player_2 = Player(name=configs_dict["players"][1]["name"])
    
    def run(self):
        """ loop that runs the game """
        print("Please welcome our players!")
        print(f"Player One: {self.player_1} ")
        print(f"Player Two: {self.player_2} ")
        
        
        
class Player:
    """ a class that describes a player """
    def __init__(self, name=None, cards =(), pieces = (), **kwargs):
        self.cards = cards
        self.pieces = pieces
        self.kwargs = kwargs
        
        self.name = name if name is not None else self.generate_random_name()
        
    def __repr__(self):
        return self.name


    def generate_random_name(self, length=5):
        """ just for fun - generates random names to players if none assigned """
        chars = string.ascii_lowercase
        # Generate a random name of specified length
        return ''.join(random.choice(chars) for _ in range(length))
    