import tkinter as tk
import os
import yaml
import json
import subprocess
import threading

from modules.constants import SCRIPT_DIR, PLAYLISTS_FILE, CONFIG_FILE


def run_tidal_dl(link, download_dir, text_widget):
    global quality_mode
    process = subprocess.Popen(
        [
            "tidal-dl",
            "--link",
            link,
            "--output",
            download_dir,
            "--quality",
            quality_mode,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    def update_text_widget(stream):
        for line in iter(stream.readline, ""):
            text_widget.insert(tk.END, line)
            text_widget.see(tk.END)  # Scroll to the end of the Text widget
        stream.close()

    threading.Thread(target=update_text_widget, args=(process.stdout,)).start()
    threading.Thread(target=update_text_widget, args=(process.stderr,)).start()

    process.wait()
    text_widget.insert(tk.END, "\nDownload completed.\n")
    text_widget.see(tk.END)


def download(config, playlists_data, text_widget):
    def download_thread():
        music_directory = config["music_directory"]

        for category_name, category_playlists in playlists_data.items():
            for link_name, link in category_playlists.items():
                download_dir = f"{music_directory}/{category_name}/{link_name}"
                run_tidal_dl(link, download_dir, text_widget)

    threading.Thread(target=download_thread).start()


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


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)


def save_config(config):
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
