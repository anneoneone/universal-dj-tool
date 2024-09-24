import tkinter as tk

from modules.HoverLabel import create_hover_label
from modules.center_frame_utils import (
    create_folder,
    create_playlist,
    update_item,
    remove_item,
    select_quality,
    select_convert,
    download,
)
from modules.constants import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    quality_buttons,
    convert_buttons,
    ROWS,
)


def create_center_frame(root):
    center_frame = tk.Frame(root, bg="black", width=200)
    center_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
    for i in range(4):
        center_frame.grid_columnconfigure(i, weight=1)
    return center_frame


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
    # BUTTONS: CREATE_FOLDER, ADD_PLAYLIST, UPDATE, REMOVE
    create_hover_label(
        center_frame,
        "Create Folder",
        lambda: create_folder(tree, textentry_folder, playlists_data, progress_display),
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
        lambda: create_playlist(
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
        lambda: update_item(
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
        lambda: remove_item(tree, playlists_data),
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

        # Füge ein Bind-Event hinzu, um die Label-Funktion beim Klicken aufzurufen
        label.bind(
            "<Button-1>",
            lambda event, label=label, text=text: select_quality(event, label, text),
        )


def create_convert_ui(center_frame):
    # Create UI elements for conversion options
    # Add labels for conversion options
    # CONVERT
    tk.Label(center_frame, text="Convert", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["CONVERT_TITLE_LABEL"], column=0, padx=5, pady=5, sticky="w"
    )

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

        # Füge ein Bind-Event hinzu, um die Label-Funktion beim Klicken aufzurufen
        label.bind(
            "<Button-1>",
            lambda event, label=label, t=text: select_convert(event, label, text),
        )


def create_download_buttons_ui(center_frame, config, playlists_data, progress_display):
    # Create buttons for downloading selected and all items
    # BUTTONS DOWNLOAD_SELECTED, DOWNLOAD_ALL
    create_hover_label(
        center_frame,
        "Download Selected",
        lambda: download(config, playlists_data, progress_display),
        bg="#004499",
        fg="white",
    ).grid(
        row=ROWS["DOWNLOAD_BUTTONS"],
        column=0,
        columnspan=2,
        padx=5,
        pady=5,
        sticky="ew",
    )

    create_hover_label(
        center_frame,
        "Download All",
        lambda: download(config, playlists_data, progress_display),
        bg="#009944",
        fg="white",
    ).grid(
        row=ROWS["DOWNLOAD_BUTTONS"],
        column=2,
        columnspan=2,
        padx=5,
        pady=5,
        sticky="ew",
    )


def setup_center_frame(root, playlists_data, tree, config, progress_display):
    center_frame = create_center_frame(root)
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
    create_download_buttons_ui(center_frame, config, playlists_data, progress_display)

    return textentry_folder, textentry_playlist, textentry_url
