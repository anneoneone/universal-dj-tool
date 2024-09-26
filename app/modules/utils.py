import os
import yaml
import json

from modules.constants import SCRIPT_DIR, PLAYLISTS_FILE, CONFIG_FILE

config = None


# Lade die Playlists
def load_playlists():
    try:
        with open(PLAYLISTS_FILE, "r") as f:
            playlists = json.load(f)
            return playlists
    except FileNotFoundError:
        return {}


# Speichere die Playlists
def save_playlists(playlists):
    with open(PLAYLISTS_FILE, "w") as f:
        json.dump(playlists, f, indent=4)


def load_config(config_file):
    global config
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)


def save_config():
    global config
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f)


def ensure_config_files():
    if not os.path.exists(SCRIPT_DIR):
        os.makedirs(SCRIPT_DIR)

    # if not os.path.exists(PLAYLISTS_FILE):
    #     with open(PLAYLISTS_FILE, 'w') as f:
    #         json.dump(categories, f, ensure_ascii=False, indent=4)

    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "music_directory": os.path.expanduser("~/Music"),
            "download_format": "m4a",
        }
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(default_config, f)


def get_config_par(par):
    # Greife auf das globale config-Dictionary zu
    if config and par in config:
        return config[par]
    else:
        raise KeyError(f"Parameter {par} not found in config file")
    

def set_config_par(par, value):
    global config
    if config is not None:
        config[par] = value
    else:
        raise ValueError("Konfiguration wurde nicht geladen.")
