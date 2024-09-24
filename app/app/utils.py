
import json

def load_playlists(file_path):
    """Load playlists from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_playlists(file_path, playlists):
    """Save playlists to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(playlists, file)

def load_config(config_path):
    """Load configuration settings."""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
