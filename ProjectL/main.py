import yaml
import os
import logging
from logging.handlers import RotatingFileHandler
import datetime
import random
from game_objects import GameManager

# Global flag for Full Debug mode (set during setup)
FULL_DEBUG = False

# Function to set up logging based on configs
def setup_logging(configs):
    global FULL_DEBUG
    logging_config = configs.get('logging', {})
    logging_mode = logging_config.get('level', 'NORMAL').upper()
    log_dir = logging_config.get('log_dir', 'logs')

    # Map mode to logging level
    if logging_mode in ['DETAILED', 'FULL_DEBUG']:
        level = logging.DEBUG
        FULL_DEBUG = (logging_mode == 'FULL_DEBUG')  # Enable extra debug logs
    else:
        level = logging.INFO  # Default to NORMAL

    # Generate human-readable, unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
    os.makedirs(log_dir, exist_ok=True)  # Create log directory if needed
    log_filename = os.path.join(log_dir, f"game_log_{timestamp}_{unique_id}.log")

    # Set up rotating file handler (rotates at 5MB, keeps 5 backups)
    file_handler = RotatingFileHandler(log_filename, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(level)

    # Console handler for real-time output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Standard formatter for readability
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Configure root logger
    logging.basicConfig(level=level, handlers=[file_handler, console_handler])
    logging.info(f"Logging initialized in {logging_mode} mode. Log file: {log_filename}")


# TODO: configure as a default general configs the maximal dimensions of the card
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(dir_path)                  # since configs are in project root
file_path = os.path.join(parent_dir, 'configs.yaml')


def main():
    logger = logging.getLogger(__name__)  # Logger for this module
    configs_dict = read_yaml(file_path)
    setup_logging(configs_dict)  # Set up logging after loading configs
    logger.info(f"Configs loaded successfully")  # High-level, replaces print
    if FULL_DEBUG:
        logger.debug(f"Full config details: {configs_dict}")  # Extra for Full Debug

    gm = GameManager(configs_dict)
    logger.info("GameManager initialized")
    gm.run()



def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data

if __name__ == "__main__":
    main()
