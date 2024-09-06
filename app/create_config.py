import os
import json
import configparser
import getpass

CONFIG_DIR = os.path.expanduser("~/.config/universal-dj-tool")
PLAYLISTS_FILE = os.path.join(CONFIG_DIR, "playlists.json")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.conf")

def prompt_yes_no(question):
    """Prompt user for yes or no answer."""
    while True:
        response = input(question + " (y/n): ").strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Invalid input. Please enter 'y' or 'n'.")

def create_config_files():
    """Create the configuration files with user input."""
    # Ensure the config directory exists
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # Create or overwrite playlists.json
    if os.path.exists(PLAYLISTS_FILE):
        if not prompt_yes_no("The file 'playlists.json' already exists. Overwrite?"):
            print("Skipping 'playlists.json' creation.")
        else:
            playlists = {
                "Digital 💾": {},
                "Vinyl 📀": {},
                "Recherche ❓": {},
                "Radio Moafunk 🎙️": {},
                "Partys 🎉": {}
            }
            with open(PLAYLISTS_FILE, 'w') as f:
                json.dump(playlists, f, indent=4)
            print(f"'playlists.json' has been created/overwritten at {PLAYLISTS_FILE}.")
    else:
        playlists = {
            "Digital 💾": {},
            "Vinyl 📀": {},
            "Recherche ❓": {},
            "Radio Moafunk 🎙️": {},
            "Partys 🎉": {}
        }
        with open(PLAYLISTS_FILE, 'w') as f:
            json.dump(playlists, f, indent=4)
        print(f"'playlists.json' has been created at {PLAYLISTS_FILE}.")

    # Create or overwrite settings.conf
    if os.path.exists(SETTINGS_FILE):
        if not prompt_yes_no("The file 'settings.conf' already exists. Overwrite?"):
            print("Skipping 'settings.conf' creation.")
        else:
            config = configparser.ConfigParser()

            config['DEFAULT'] = {
                'MusicDirectory': os.path.expanduser('~/Music')
            }

            with open(SETTINGS_FILE, 'w') as configfile:
                config.write(configfile)
            print(f"'settings.conf' has been created/overwritten at {SETTINGS_FILE}.")
    else:
        config = configparser.ConfigParser()

        config['DEFAULT'] = {
            'MusicDirectory': os.path.expanduser('~/Music')
        }

        with open(SETTINGS_FILE, 'w') as configfile:
            config.write(configfile)
        print(f"'settings.conf' has been created at {SETTINGS_FILE}.")

def main():
    create_config_files()

if __name__ == "__main__":
    main()
