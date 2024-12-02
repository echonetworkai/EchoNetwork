import json
import logging
import os
from datetime import datetime

# Setup a logger
def setup_logger(name, log_file, level=logging.INFO):
    """Sets up a logger that outputs to both the console and a log file."""
    logger = logging.getLogger(name)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Example function for generating a unique agent ID
def generate_agent_id():
    """Generates a unique ID based on the current time."""
    return f"agent_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

# Function for saving JSON data to a file
def save_json(data, filename):
    """Saves data to a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Function for loading JSON data from a file
def load_json(filename):
    """Loads data from a JSON file."""
    if os.path.exists(filename):
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    else:
        return {}

# Function to ensure a directory exists
def ensure_directory_exists(directory):
    """Creates the directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

# Helper function to get current timestamp
def get_timestamp():
    """Returns the current timestamp as a string."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Example utility for calculating agent learning progress
def calculate_learning_progress(start_time, current_time, total_steps):
    """Calculates the learning progress as a percentage."""
    time_elapsed = (current_time - start_time).total_seconds()
    progress = (time_elapsed / total_steps) * 100
    return min(progress, 100)  # Ensure that it doesn't exceed 100%
