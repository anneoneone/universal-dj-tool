# Constants for the GUI Application
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYLISTS_FILE = os.path.join(SCRIPT_DIR, "..", "playlists.json")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "..", "config.yaml")

WINDOW_SIZE = "1200x800"
PRIMARY_COLOR = "#8822FF"
SECONDARY_COLOR = "#FF2288"
ACTIVE_LABEL_BG = PRIMARY_COLOR
INACTIVE_LABEL_BG = SECONDARY_COLOR

# Button configurations
quality_buttons = [("Normal", 0), ("High", 1), ("HiFi", 2), ("Master", 3)]

convert_buttons = [("Don't Convert", 0), ("mp3", 1), ("aiff", 2), ("wav", 3)]

COLS = {
    "1_1": 12,
    "3_4": 9,
    "2_3": 8,
    "1_2": 6,
    "1_3": 4,
    "1_4": 3,
}

# Layout rows
ROWS = {
    "ROOT_DIR_TITLE_LABEL": 0,
    "ROOT_DIR_DESC_LABEL": 1,
    "ROOT_DIR_SELECT": 2,
    "ROOT_DIR_SEPARATOR": 3,
    "FOLDER_TITLE_LABEL": 4,
    "FOLDER_DESC_LABEL": 5,
    "FOLDER_ENTRY": 6,
    "PLAYLIST_TITLE_LABEL": 7,
    "PLAYLIST_DESC_LABEL": 8,
    "PLAYLIST_ENTRY": 9,
    "URL_TITLE_LABEL": 10,
    "URL_DESC_LABEL": 11,
    "URL_ENTRY": 12,
    "PLAYLISTS_BUTTONS": 13,
    "PLAYLISTS_SEPARATOR": 14,
    "QUALITY_TITLE_LABEL": 15,
    "QUALITY_FORMAT_LABEL": 16,
    "QUALITY_BUTTONS": 17,
    "CONVERT_TITLE_LABEL": 18,
    "CONVERT_BUTTONS": 19,
    "BUTTONS_SEPERATOR": 20,
    "DOWNLOAD_BUTTONS": 21,
}

welcome_text = """


 ┌──────────────────────────────────────────────┐
 │                                              │
 │                                              │
 │   ______   __                                │
 │  /\__  _\ /\ \                               │
 │  \/_/\ \/ \ \/      ___ ___                  │
 │     \ \ \  \/     /' __` __`\                │
 │      \_\ \__      /\ \/\ \/\ \               │
 │      /\_____\     \ \_\ \_\ \_\              │
 │      \/_____/      \/_/\/_/\/_/              │
 │                         ____     _____       │
 │                        /\  _`\  /\___ \      │
 │                __      \ \ \/\ \ /__/\ \     │
 │              /'__`\     \ \ \ \ \  _\ \ \    │
 │             /\ \L\.\_    \ \ \_\ \/\ \_\ \   │
 │             \ \__/.\_\    \ \____/\ \____/   │
 │              \/__/\/_/     \/___/  \/___/    │
 │   ______                 ___        __       │
 │  /\__  _\               /\_ \      /\ \      │
 │  \/_/\ \/    ___     ___\ /\ \     \ \ \     │
 │     \ \ \   / __`\  / __`\\ \ \     \ \ \    │
 │      \ \ \  \ \L\ \/\ \L\ \\_\ \_    \ \_\   │
 │       \ \_\\ \____/\ \____//\____\    \/\_\  │
 │        \/_/ \/___/  \/___/ \/____/     \/_/  │
 │                                              │
 │                                              │
 └──────────────────────────────────────────────┘


"""
