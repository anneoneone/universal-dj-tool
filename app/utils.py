import os
import yaml
import json

# Ermittle den Pfad des aktuellen Skripts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYLISTS_FILE = os.path.join(SCRIPT_DIR, 'playlists.json')
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.yaml")


# Lade die Playlists
def load_playlists():
    try:
        with open(PLAYLISTS_FILE, 'r') as f:
            playlists = json.load(f)
            return playlists
    except FileNotFoundError:
        return {}


# Speichere die Playlists
def save_playlists(playlists):
    with open(PLAYLISTS_FILE, 'w') as f:
        json.dump(playlists, f, indent=4)


def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)


def ensure_config_files():
    if not os.path.exists(SCRIPT_DIR):
        os.makedirs(SCRIPT_DIR)

    # if not os.path.exists(PLAYLISTS_FILE):
    #     with open(PLAYLISTS_FILE, 'w') as f:
    #         json.dump(categories, f, ensure_ascii=False, indent=4)

    if not os.path.exists(CONFIG_FILE):
        default_config = {
            'music_directory': os.path.expanduser("~/Music"),
            'download_format': 'm4a'
        }
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(default_config, f)
