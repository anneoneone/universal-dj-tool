import subprocess
import os
import json
import yaml
import argparse

# CONFIG_DIR = os.path.expanduser("~/.config/universal-dj-tool/")
CONFIG_DIR = os.path.expanduser("./")
PLAYLISTS_FILE = os.path.join(CONFIG_DIR, "playlists.json")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yaml")


def ensure_config_files():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    if not os.path.exists(PLAYLISTS_FILE):
        with open(PLAYLISTS_FILE, 'w') as f:
            json.dump(categories, f, ensure_ascii=False, indent=4)

    if not os.path.exists(CONFIG_FILE):
        default_config = {
            'music_directory': os.path.expanduser("~/Music"),
            'download_format': 'm4a'
        }
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(default_config, f)


def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)


def load_playlists():
    with open(PLAYLISTS_FILE, 'r') as f:
        return json.load(f)


def save_playlists(playlists):
    with open(PLAYLISTS_FILE, 'w') as f:
        json.dump(playlists, f, ensure_ascii=False, indent=4)


def download_playlists(
    music_directory, download_format, category_name, playlists, single_update_playlist
):
    for playlist_name, link in playlists.items():
        if (
            single_update_playlist == ""
            or single_update_playlist in category_name
            or single_update_playlist in playlist_name
        ):
            print(f"Updating {playlist_name}...")
            download_dir = os.path.join(music_directory, download_format, category_name)
            subprocess.run(["tidal-dl", "-l", link, "-o", download_dir])
            playlist_dir = os.path.join(download_dir, playlist_name)
            subprocess.Popen(["python3", "convert_music_files.py", playlist_dir, "m4a", "mp3"])


def edit_config():
    config = load_config()
    print("Current configuration:")
    for key, value in config.items():
        new_value = input(f"{key} [{value}]: ")
        if new_value:
            config[key] = new_value
    save_config(config)


def add_playlist():
    playlists = load_playlists()
    category = input("Enter category: ")
    playlist_name = input("Enter playlist name: ")
    playlist_link = input("Enter playlist link: ")
    if category not in playlists:
        playlists[category] = {}
    playlists[category][playlist_name] = playlist_link
    save_playlists(playlists)


def main():
    single_update_playlist = ""
    ensure_config_files()
    config = load_config()
    playlists = load_playlists()

    parser = argparse.ArgumentParser(description="Universal DJ Tool")
    parser.add_argument(
        "--config", action="store_true", help="Edit configuration"
    )
    parser.add_argument(
        "--playlist", action="store_true", help="Add or remove playlists"
    )
    parser.add_argument(
        "--update", type=str, required=True, help="Update single category or playlist"
    )

    args = parser.parse_args()

    if args.config:
        edit_config()
    elif args.playlist:
        add_playlist()
    else:
        if args.update:
            single_update_playlist = args.update

        music_directory = config['music_directory']
        download_format = config['download_format']
        for category_name, category_playlists in playlists.items():
            download_playlists(
                music_directory,
                download_format,
                category_name,
                category_playlists,
                single_update_playlist
            )


if __name__ == "__main__":
    main()
