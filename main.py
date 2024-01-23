import yaml
import os

from game_objects import GameManager

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'configs.yaml')

def main():
    configs_dict = read_yaml(file_path)
    gm = GameManager(configs_dict)
    print(f"Those are the configs: {configs_dict}")
    print(f"And that's our GameManager... let's run it! ")
    gm.run()
    
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        # Parse YAML content
        data = yaml.safe_load(file)
        return data

if __name__ == "__main__":
    main()