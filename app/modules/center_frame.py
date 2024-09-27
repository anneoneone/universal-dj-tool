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
)
from modules.constants import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    quality_buttons,
    convert_buttons,
    ROWS,
)
from modules.utils import get_config_par


def create_center_frame(root):
    center_frame = tk.Frame(root, bg="black") #, width=200)
    center_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
    for i in range(4):
        center_frame.grid_columnconfigure(i, weight=1)
    return center_frame


def create_root_dir_ui(center_frame):
    tk.Label(center_frame, text="Download Folder", bg=PRIMARY_COLOR, fg="white").grid(
        row=ROWS["ROOT_DIR_TITLE_LABEL"], column=0, padx=5, pady=5, sticky="w"
    )
    tk.Label(
        center_frame,
        text="This is the root folder, where all the playlists will be downloaded.",
        bg=PRIMARY_COLOR,
        fg="white",
        anchor="w",
    ).grid(row=ROWS["ROOT_DIR_DESC_LABEL"], column=0, columnspan=4, padx=5, pady=5, sticky="we")

    shortened_folder = shorten_path(get_config_par("music_dir"))
    music_dir_label = tk.Label(
        center_frame, text=shortened_folder, bg=PRIMARY_COLOR, fg="white", anchor="w"
    )
    music_dir_label.grid(
        row=ROWS["ROOT_DIR_SELECT"], column=0, columnspan=3, padx=5, pady=5, sticky="we"
    )

    create_hover_label(
        center_frame,
        "Select Folder",
        lambda: select_folder(music_dir_label),
        bg="black",
        fg="white",
    ).grid(
        row=ROWS["ROOT_DIR_SELECT"],
        column=3,
        columnspan=1,
        padx=5,
        pady=5,
        sticky="ew",
    )


def create_folder_ui(center_frame):
    # Create UI elements for folder
    # Add labels, entries, and descriptions
    # FOLDER NAME
    tk.Label(center_frame, text="Folder Name", bg=PRIMARY_COLOR, fg="white").grid(
        row=ROWS["FOLDER_TITLE_LABEL"], column=0, padx=5, pady=5, sticky="w"
    )
    tk.Label(
        center_frame, text="Folder Description", bg=PRIMARY_COLOR, fg="white"
    ).grid(row=ROWS["FOLDER_DESC_LABEL"], column=0, padx=5, pady=5, sticky="w")
    textentry_folder = tk.Entry(
        center_frame, bg=PRIMARY_COLOR, fg="white", insertbackground="white"
    )
    textentry_folder.grid(
        row=ROWS["FOLDER_ENTRY"], column=0, columnspan=4, padx=5, pady=5, sticky="ew"
    )

    return textentry_folder


def create_playlist_ui(center_frame):
    # Create UI elements for playlist
    # Add labels, entries, and descriptions
    # PLAYLIST NAME
    tk.Label(center_frame, text="Playlist Name", bg=PRIMARY_COLOR, fg="white").grid(
        row=ROWS["PLAYLIST_TITLE_LABEL"], column=0, padx=5, pady=5, sticky="w"
    )
    tk.Label(
        center_frame, text="Playlist Description", bg=PRIMARY_COLOR, fg="white"
    ).grid(row=ROWS["PLAYLIST_DESC_LABEL"], column=0, padx=5, pady=5, sticky="w")
    textentry_playlist = tk.Entry(
        center_frame, bg=PRIMARY_COLOR, fg="white", insertbackground="white"
    )
    textentry_playlist.grid(
        row=ROWS["PLAYLIST_ENTRY"], column=0, columnspan=4, padx=5, pady=5, sticky="ew"
    )

    return textentry_playlist


def create_url_ui(center_frame):
    # Create UI elements for URL
    # Add labels, entries, and descriptions
    # TIDAL PLAYLIST URL
    tk.Label(center_frame, text="URL", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["URL_TITLE_LABEL"], column=0, padx=5, pady=5, sticky="w"
    )
    tk.Label(center_frame, text="URL Description", bg=PRIMARY_COLOR, fg="white").grid(
        row=ROWS["URL_DESC_LABEL"], column=0, padx=5, pady=5, sticky="w"
    )
    textentry_url = tk.Entry(
        center_frame, bg=PRIMARY_COLOR, fg="white", insertbackground="white"
    )
    textentry_url.grid(
        row=ROWS["URL_ENTRY"], column=0, columnspan=4, padx=5, pady=5, sticky="ew"
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
    ).grid(
        row=ROWS["PLAYLISTS_BUTTONS"],
        column=0,
        columnspan=1,
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
        column=1,
        columnspan=1,
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
        column=2,
        columnspan=1,
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
        column=3,
        columnspan=1,
        padx=5,
        pady=5,
        sticky="ew",
    )


def create_quality_ui(center_frame):
    # Create UI elements for quality selection
    # Add labels for quality options
    # QUALITY
    tk.Label(center_frame, text="Quality", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["QUALITY_TITLE_LABEL"], column=0, padx=5, pady=5, sticky="w"
    )
    tk.Label(center_frame, text="m4a", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["QUALITY_FORMAT_LABEL"],
        column=0,
        columnspan=2,
        padx=5,
        pady=5,
        sticky="w",
    )
    tk.Label(center_frame, text="flac", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["QUALITY_FORMAT_LABEL"],
        column=2,
        columnspan=2,
        padx=5,
        pady=5,
        sticky="w",
    )

    quality_mode_label_list = []

    for text, col in quality_buttons:
        label = tk.Label(
            center_frame,
            text=text,
            bg=SECONDARY_COLOR,
            fg="white",
            padx=10,  # Padding innerhalb des Labels
            pady=5,  # Padding innerhalb des Labels
        )
        label.grid(row=ROWS["QUALITY_BUTTONS"], column=col, padx=5, pady=5, sticky="w")

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
    tk.Label(center_frame, text="Convert", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["CONVERT_TITLE_LABEL"], column=0, padx=5, pady=5, sticky="w"
    )

    convert_mode_label_list = []

    for text, col in convert_buttons:
        label = tk.Label(
            center_frame,
            text=text,
            bg=SECONDARY_COLOR,
            fg="white",
            padx=10,  # Padding innerhalb des Labels
            pady=5,  # Padding innerhalb des Labels
        )
        label.grid(row=ROWS["CONVERT_BUTTONS"], column=col, padx=5, pady=5, sticky="w")

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


def create_download_buttons_ui(center_frame, playlists_data, progress_display):
    # Create buttons for downloading selected and all items
    # BUTTONS DOWNLOAD_SELECTED, DOWNLOAD_ALL
    create_hover_label(
        center_frame,
        "Download Selected",
        lambda: download(playlists_data, progress_display),
        bg="#004499",
        fg="white",
    ).grid(
        row=ROWS["DOWNLOAD_BUTTONS"],
        column=0,
        columnspan=1,
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
        column=1,
        columnspan=1,
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
        column=2,
        columnspan=1,
        padx=5,
        pady=5,
        sticky="ew",
    )


def setup_center_frame(root, playlists_data, tree, progress_display):
    center_frame = create_center_frame(root)
    create_root_dir_ui(center_frame)
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
    create_quality_ui(center_frame)
    create_convert_ui(center_frame)
    create_download_buttons_ui(center_frame, playlists_data, progress_display)

    return textentry_folder, textentry_playlist, textentry_url
