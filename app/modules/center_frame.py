import json
import tkinter as tk

from modules.HoverLabel import create_hover_label
from modules.center_frame_utils import (
    tree_create_folder,
    tree_create_playlist,
    tree_update_item,
    tree_remove_item,
    set_quality_mode,
    set_convert_mode,
    download,
    stop_tidal_dl,
    select_folder,
    shorten_path,
    create_tooltip,
)
from modules.constants import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    quality_buttons,
    convert_buttons,
    ROWS,
    COLS,
)
from modules.utils import get_config_par
import tidalapi

from modules.tidal_login import TidalLogin


def create_separator(center_frame, row):
    separator = tk.Frame(center_frame, bg=PRIMARY_COLOR, height=2)  # Höhe von 2 Pixeln
    separator.grid(
        row=row,
        column=0,
        columnspan=COLS["1_1"],
        padx=5,
        pady=(10, 25),
        sticky="we"
    )


def create_center_frame(root):
    center_frame = tk.Frame(root, bg="black") #, width=200)
    center_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
    for i in range(COLS["1_1"]):
        center_frame.grid_columnconfigure(i, weight=1)
    return center_frame


def create_header_label(center_frame, text):
    label = tk.Label(
        center_frame,
        text=text,
        bg="black",
        fg="white",
        font=("Courier New", 16, "bold"),
    )
    return label


def create_entry(center_frame):
    entry = tk.Entry(
        center_frame, bg="#003333", fg="white", insertbackground="white"
    )
    return entry


def create_root_dir_ui(center_frame):
    root_dir_label = create_header_label(center_frame, "Download Folder")
    root_dir_label.grid(
        row=ROWS["ROOT_DIR_TITLE_LABEL"],
        column=0,
        columnspan=COLS["3_4"],
        padx=5,
        pady=5,
        sticky="w",
    )

    create_tooltip(
        center_frame,
        root_dir_label,
        "This is the root folder, where all the playlists will be downloaded.",
    )

    shortened_folder = shorten_path(get_config_par("music_dir"))
    music_dir_label = tk.Label(
        center_frame, text=shortened_folder, bg=PRIMARY_COLOR, fg="white", anchor="w"
    )
    music_dir_label.grid(
        row=ROWS["ROOT_DIR_SELECT"], column=0, columnspan=COLS["3_4"], padx=5, pady=5, sticky="we"
    )

    create_hover_label(
        center_frame,
        "Select Folder",
        lambda: select_folder(music_dir_label),
        bg="blue",
        fg="white",
        bd=2,
        highlightthickness=3,
        highlightbackground="pink",
        highlightcolor="pink",
    ).grid(
        row=ROWS["ROOT_DIR_SELECT"],
        column=COLS["3_4"],
        columnspan=COLS["1_4"],
        padx=5,
        pady=5,
        sticky="ew",
    )


def create_folder_ui(center_frame):
    # Create UI elements for folder
    # Add labels, entries, and descriptions
    # FOLDER NAME
    folder_label = create_header_label(center_frame, text="Folder Name")
    folder_label.grid(
        row=ROWS["FOLDER_TITLE_LABEL"], column=0, columnspan=COLS["1_1"], padx=5, pady=5, sticky="w"
    )
    create_tooltip(
        center_frame,
        folder_label,
        "Store your playlists in folders. \n"
        "If you organize your TIDAL playlists in folders, it is HIGHLY RECOMMENDED to give them the same name!",
    )

    textentry_folder = create_entry(center_frame)
    textentry_folder.grid(
        row=ROWS["FOLDER_ENTRY"], column=0, columnspan=COLS["1_1"], padx=5, pady=5, sticky="ew"
    )

    return textentry_folder


def create_playlist_ui(center_frame):
    # Create UI elements for playlist
    # Add labels, entries, and descriptions
    # PLAYLIST NAME
    playlist_label = create_header_label(center_frame, text="Playlist Name")
    playlist_label.grid(
        row=ROWS["PLAYLIST_TITLE_LABEL"], column=0, columnspan=COLS["1_1"], padx=5, pady=5, sticky="w"
    )
    create_tooltip(
        center_frame,
        playlist_label,
        "Name of TIDAL playlist. \n"
        "GIVE IT THE EXACT SAME NAME!",
    )

    textentry_playlist = create_entry(center_frame)
    textentry_playlist.grid(
        row=ROWS["PLAYLIST_ENTRY"], column=0, columnspan=COLS["1_1"], padx=5, pady=5, sticky="ew"
    )

    return textentry_playlist


def create_url_ui(center_frame):
    # Create UI elements for URL
    # Add labels, entries, and descriptions
    # TIDAL PLAYLIST URL
    url_label = create_header_label(center_frame, text="URL")
    url_label.grid(
        row=ROWS["URL_TITLE_LABEL"], column=0, columnspan=COLS["1_1"], padx=5, pady=5, sticky="w"
    )
    create_tooltip(
        center_frame,
        url_label,
        "URL of your TIDAL playlist. \n"
        "In TIDAL click on \"Share\" -> \"Copy playlist link\" to get the URL of a playlist!",
    )

    textentry_url = create_entry(center_frame)
    textentry_url.grid(
        row=ROWS["URL_ENTRY"], column=0, columnspan=COLS["1_1"], padx=5, pady=5, sticky="ew"
    )

    return textentry_url


def create_buttons_ui(
    center_frame,
    tree,
    textentry_folder,
    textentry_playlist,
    textentry_url,
    playlists_data,
    progress_display,
):
    # Create buttons for actions like create, add, update, remove
    # BUTTONS: tree_create_folder, ADD_PLAYLIST, UPDATE, REMOVE
    create_hover_label(
        center_frame,
        "Create Folder",
        lambda: tree_create_folder(
            tree, textentry_folder, playlists_data, progress_display
        ),
        bg="black",
        fg="white",
        bd=2,
        highlightthickness=3,
        highlightbackground="white",
        highlightcolor="white",
        activebackground="white",
        activeforeground="white",
    ).grid(
        row=ROWS["PLAYLISTS_BUTTONS"],
        column=0,
        columnspan=COLS["1_4"],
        padx=5,
        pady=5,
        sticky="ew",
    )

    create_hover_label(
        center_frame,
        "Add Playlist",
        lambda: tree_create_playlist(
            tree,
            textentry_folder,
            textentry_playlist,
            textentry_url,
            playlists_data,
            progress_display,
        ),
        bg="black",
        fg="white",

    ).grid(
        row=ROWS["PLAYLISTS_BUTTONS"],
        column=COLS["1_4"],
        columnspan=COLS["1_4"],
        padx=5,
        pady=5,
        sticky="ew",
    )

    create_hover_label(
        center_frame,
        "Update",
        lambda: tree_update_item(
            tree,
            textentry_folder,
            textentry_playlist,
            textentry_url,
            playlists_data,
            progress_display,
        ),
        bg="black",
        fg="white",
    ).grid(
        row=ROWS["PLAYLISTS_BUTTONS"],
        column=COLS["1_2"],
        columnspan=COLS["1_4"],
        padx=5,
        pady=5,
        sticky="ew",
    )

    create_hover_label(
        center_frame,
        "Delete",
        lambda: tree_remove_item(tree, playlists_data),
        bg="black",
        fg="white",
    ).grid(
        row=ROWS["PLAYLISTS_BUTTONS"],
        column=COLS["3_4"],
        columnspan=COLS["1_4"],
        padx=5,
        pady=5,
        sticky="ew",
    )


def create_quality_ui(center_frame):
    # Create UI elements for quality selection
    # Add labels for quality options
    # QUALITY
    quality_label = create_header_label(center_frame, text="Quality & Format")
    quality_label.grid(
        row=ROWS["QUALITY_TITLE_LABEL"], column=0, columnspan=COLS["1_1"], padx=5, pady=5, sticky="w"
    )
    create_tooltip(
        center_frame,
        quality_label,
        "TIDAL allows downloading files in four different qualities.\n"
        "\"Normal\" and \"High\" => m4a-files with many metadata\n"
        "\"HiFi\" and \"Master\" => flac-files with not so many metadata",
    )

    tk.Label(center_frame, text="m4a", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["QUALITY_FORMAT_LABEL"],
        column=0,
        columnspan=COLS["1_2"],
        padx=5,
        pady=5,
        sticky="we",
    )
    tk.Label(center_frame, text="flac", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["QUALITY_FORMAT_LABEL"],
        column=COLS["1_2"],
        columnspan=COLS["1_2"],
        padx=5,
        pady=5,
        sticky="we",
    )

    quality_mode_label_list = []

    for text, col in quality_buttons:
        col = col * COLS["1_4"]
        label = tk.Label(
            center_frame,
            text=text,
            bg=SECONDARY_COLOR,
            fg="white",
            padx=10,  # Padding innerhalb des Labels
            pady=5,  # Padding innerhalb des Labels
        )
        label.grid(
            row=ROWS["QUALITY_BUTTONS"],
            column=col,
            columnspan=COLS["1_4"],
            padx=5,
            pady=5,
            sticky="we",
        )

        quality_mode_label_list.append(label)

        # Füge ein Bind-Event hinzu, um die Label-Funktion beim Klicken aufzurufen
        label.bind(
            "<Button-1>",
            lambda event, label=label, text=text: set_quality_mode(
                event=event, label=label, quality=text
            ),
        )

    # set quality label active from config
    config_quality_mode = get_config_par('quality_mode')
    quality_index = next(
        (
            index
            for index, (text, _) in enumerate(quality_buttons)
            if text == config_quality_mode
        ),
        0,
    )
    active_label = quality_mode_label_list[quality_index]
    set_quality_mode(label=active_label, quality=quality_buttons[quality_index][0])


def create_convert_ui(center_frame):
    # Create UI elements for conversion options
    # Add labels for conversion options
    # CONVERT
    convert_label = create_header_label(center_frame, text="Convert After Download")
    convert_label.grid(
        row=ROWS["CONVERT_TITLE_LABEL"],
        column=0,
        columnspan=COLS["1_1"],
        padx=5,
        pady=5,
        sticky="w",
    )
    create_tooltip(
        center_frame,
        convert_label,
        "Automatically convert your files after download. \n"
    )

    convert_mode_label_list = []

    for text, col in convert_buttons:
        col = col * COLS["1_4"]
        label = tk.Label(
            center_frame,
            text=text,
            bg=SECONDARY_COLOR,
            fg="white",
            padx=10,  # Padding innerhalb des Labels
            pady=5,  # Padding innerhalb des Labels
        )
        label.grid(
            row=ROWS["CONVERT_BUTTONS"],
            column=col,
            columnspan=COLS["1_4"],
            padx=5,
            pady=5,
            sticky="we",
        )

        convert_mode_label_list.append(label)

        # Füge ein Bind-Event hinzu, um die Label-Funktion beim Klicken aufzurufen
        label.bind(
            "<Button-1>",
            lambda event, label=label, text=text: set_convert_mode(
                event=event, label=label, convert=text
            ),
        )

    # set convert label active from config
    config_convert_mode = get_config_par('convert_mode')
    convert_index = next(
        (
            index
            for index, (text, _) in enumerate(convert_buttons)
            if text == config_convert_mode
        ),
        0,
    )
    active_label = convert_mode_label_list[convert_index]
    set_convert_mode(label=active_label, convert=convert_buttons[convert_index][0])


def create_download_buttons_ui(root, center_frame, playlists_data, progress_display):
    # Create buttons for downloading selected and all items
    # BUTTONS DOWNLOAD_SELECTED, DOWNLOAD_ALL
    create_hover_label(
        center_frame,
        "Download Selected",
        lambda: login_tl(progress_display),
        # lambda: download(playlists_data, progress_display),
        bg="#004499",
        fg="white",
    ).grid(
        row=ROWS["DOWNLOAD_BUTTONS"],
        column=0,
        columnspan=COLS["1_3"],
        padx=5,
        pady=5,
        sticky="ew",
    )

    create_hover_label(
        center_frame,
        "Download All",
        lambda: download(playlists_data, progress_display),
        bg="#009944",
        fg="white",
    ).grid(
        row=ROWS["DOWNLOAD_BUTTONS"],
        column=COLS["1_3"],
        columnspan=COLS["1_3"],
        padx=5,
        pady=5,
        sticky="ew",
    )

    # Button für "Abbrechen"
    create_hover_label(
        center_frame,
        "Cancel Download",
        lambda: stop_tidal_dl(progress_display),  # Funktion, um den Prozess zu stoppen
        bg="red",
        fg="white",
    ).grid(
        row=ROWS["DOWNLOAD_BUTTONS"],
        column=COLS["2_3"],
        columnspan=COLS["1_3"],
        padx=5,
        pady=5,
        sticky="ew",
    )


def get_playlist_name():

    # Eine Session starten
    session = tidalapi.Session()
    session.login_oauth_simple()  # Benutzer muss sich hier mit den Zugangsdaten anmelden

    # Playlist ID extrahieren aus der URL
    url = "https://tidal.com/browse/playlist/5e1a1604-29db-4653-be92-b1d6ebd26448"
    playlist_id = url.split("/")[-1]

    # Playlist-Details abrufen
    playlist = tidalapi.playlist.Playlist(session, playlist_id)
    print(f"Playlist Name: {playlist.name}")

    # playlist_id = "https://tidal.com/browse/playlist/e460cae9-a583-42a1-94ca-bd4d3b323a6a"
    # playlist = tidalapi.playlist.Playlist(tidal.session, playlist_id)
    # print(f"Playlist Name: {playlist.name}")


def login_tl(progress_display):
    tidal = TidalLogin(progress_display=progress_display)
    # Lade den gespeicherten Token, falls vorhanden
    tidal.load_token()
    # Falls der Token nicht geladen werden konnte, manuell anmelden
    if not tidal.session.check_login():
        tidal.login()

    # url = "https://tidal.com/browse/playlist/5e1a1604-29db-4653-be92-b1d6ebd26448"
    url = "https://tidal.com/browse/playlist/e460cae9-a583-42a1-94ca-bd4d3b323a6a"
    playlist_id = url.split("/")[-1]

    # playlist = tidalapi.playlist.Playlist(tidal.session, playlist_id)
    # print(f"Playlist Name: {playlist.name}")

    # tidal.display_user_playlists()
    # Regelmäßig die Queue verarbeiten, um GUI zu aktualisieren
    # def update_display():
    #     tidal.process_queue()
    #     root.after(100, update_display)  # Alle 100 ms die Queue überprüfen

    # tidal.display_playlist_tracks(playlist)

    tidal.generate_rekordbox_files()

    # update_display()

def setup_center_frame(root, playlists_data, tree, progress_display):
    center_frame = create_center_frame(root)
    create_root_dir_ui(center_frame)
    create_separator(center_frame, ROWS["ROOT_DIR_SEPARATOR"])

    textentry_folder = create_folder_ui(center_frame)
    textentry_playlist = create_playlist_ui(center_frame)
    textentry_url = create_url_ui(center_frame)
    create_buttons_ui(
        center_frame,
        tree,
        textentry_folder,
        textentry_playlist,
        textentry_url,
        playlists_data,
        progress_display,
    )
    create_separator(center_frame, ROWS["PLAYLISTS_SEPARATOR"])

    create_quality_ui(center_frame)
    create_convert_ui(center_frame)
    create_separator(center_frame, ROWS["BUTTONS_SEPERATOR"])

    create_download_buttons_ui(root, center_frame, playlists_data, progress_display)


    return textentry_folder, textentry_playlist, textentry_url
