# Constants for the GUI Application

WINDOW_SIZE = "1000x700"
PRIMARY_COLOR = "#8822FF"
SECONDARY_COLOR = "#FF2288"
ACTIVE_LABEL_BG = PRIMARY_COLOR
INACTIVE_LABEL_BG = SECONDARY_COLOR

# Button configurations
quality_buttons = [("Normal", 0), ("High", 1), ("HiFi", 2), ("Master", 3)]

convert_buttons = [("Don't Convert", 0), ("mp3", 1), ("aiff", 2), ("wav", 3)]

# Layout rows
ROWS = {
    "FOLDER_TITLE_LABEL": 0,
    "FOLDER_DESC_LABEL": 1,
    "FOLDER_ENTRY": 2,
    "PLAYLIST_TITLE_LABEL": 3,
    "PLAYLIST_DESC_LABEL": 4,
    "PLAYLIST_ENTRY": 5,
    "URL_TITLE_LABEL": 6,
    "URL_DESC_LABEL": 7,
    "URL_ENTRY": 8,
    "PLAYLISTS_BUTTONS": 9,
    "QUALITY_TITLE_LABEL": 10,
    "QUALITY_FORMAT_LABEL": 11,
    "QUALITY_BUTTONS": 12,
    "CONVERT_TITLE_LABEL": 13,
    "CONVERT_BUTTONS": 14,
    "DOWNLOAD_BUTTONS": 15,
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
