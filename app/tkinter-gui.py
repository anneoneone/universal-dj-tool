import tkinter as tk
from tkinter import ttk
from utils import load_playlists, save_playlists, load_config
from download_playlists import download_playlists
import subprocess
import threading

from constants import (
    WINDOW_SIZE,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    ACTIVE_LABEL_BG,
    INACTIVE_LABEL_BG,
    quality_buttons,
    convert_buttons,
    ROWS,
    welcome_text,
)

quality_mode = None
convert_mode = None
active_quality_label = None  # Speichert das aktuell aktive Label
active_convert_label = None  # Speichert das aktuell aktive Label


# --- Funktionen zur GUI-Erstellung ---


class HoverLabel(tk.Label):

    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.configure(
            cursor="hand2",
            compound="left",
            state="active",
            font=("Courier New", 14, "bold"),
            highlightthickness=1,  # Dünne Umrandung
            highlightbackground="pink",  # Farbe der Umrandung
            highlightcolor="pink",  # Farbe, wenn es den Fokus hat
            relief="flat",  # Stil der Umrandung
            bd=1  # Dicke der Umrandung
        )

        self.toggle_bg = "#FF2288"
        self.is_hovering = False
        self.after_id = None
        self.default_bg = self.cget("bg")
        self.default_fg = self.cget("fg")
        # self.default_bitmap = self.cget("bitmap")
        self.default_width = self.cget("width")
        self.default_height = self.cget("height")
        self.default_bd = self.cget("bd")
        self.default_highlightbackground = self.cget("highlightbackground")
        self.default_highlightcolor = self.cget("highlightcolor")
        self.default_highlightthickness = self.cget("highlightthickness")
        self.default_activebackground = self.cget("activebackground")
        self.default_activeforeground = self.cget("activeforeground")

        self.command = command
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def toggle_state(self):
        if self.default_state == "active":
            return "disabled"
        else:
            return "active"

    def toggle_background(self):
        if self.is_hovering:
            current_bg = self.cget("bg")
            new_bg = (
                self.toggle_bg if current_bg == self.default_bg else self.default_bg
            )
            self.configure(bg=new_bg)
            self.after_id = self.after(200, self.toggle_background)

    def on_enter(self, event):
        self.is_hovering = True
        self.toggle_background()

    def on_leave(self, event):
        self.is_hovering = False
        if self.after_id:
            self.after_cancel(self.after_id)
        self.configure(bg=self.default_bg, fg=self.default_fg)

    def on_click(self, event):
        if self.command:
            # self.configure(state="disabled")
            self.command()


def create_hover_label(parent, text, command, **kwargs):
    return HoverLabel(parent, text=text, command=command, **kwargs)


def setup_treeview(tree, playlists_data):
    for folder, urls in playlists_data.items():
        folder_id = tree.insert("", "end", text=folder)
        for url_name in urls:
            tree.insert(folder_id, "end", text=url_name)


def print_progress_display(progress_display, text, tag="white"):

# --- Helper Functions ---


    symbol = ""
    if tag == "green":
        symbol = "✓ "
    elif tag == "yellow":
        symbol = "⚠ "
    elif tag == "red":
        symbol = "✗ "
    progress_display.insert(tk.END, symbol + text + "\n", tag)
    progress_display.see(tk.END)


def create_stripes(root, stripe_width, stripe_color_1, stripe_color_2):
    # Berechne die Anzahl der Streifen basierend auf der Fensterbreite und der Streifenbreite
    window_width = root.winfo_screenwidth()
    num_stripes = window_width // stripe_width

    for i in range(num_stripes):
        # Wähle die Farbe für den aktuellen Streifen
        color = stripe_color_1 if i % 2 == 0 else stripe_color_2

        # Erstelle ein Label als Streifen
        stripe = tk.Label(root, bg=color, width=stripe_width, height=2000)

        # Packe das Label in den Hintergrund
        stripe.place(x=i * stripe_width, y=0, width=stripe_width, relheight=1)


def setup_left_frame(tree, playlists_data, on_select, center_frame_entries):
    # TREEVIEW
    style = ttk.Style()
    style.configure(
        "Treeview.Heading",
        font=("Comic Sans MS", 16, "bold"),
        background=SECONDARY_COLOR,
        fieldbackground=SECONDARY_COLOR,
        fg=SECONDARY_COLOR,
    )
    style.configure(
        "Treeview",
        background=PRIMARY_COLOR,
        fieldbackground=PRIMARY_COLOR,
        foreground="white",
        font=("Courier New", 14),
        rowheight=18,
    )

    tree.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")
    setup_treeview(tree, playlists_data)
    tree.heading("#0", text="Playlists", anchor="w")
    textentry_folder, textentry_playlist, textentry_url = center_frame_entries
    tree.bind(
        "<<TreeviewSelect>>",
        lambda event: on_select(
            event, tree, textentry_folder, textentry_playlist, textentry_url, playlists_data
        ),
    )


def select_quality(event, label, quality):
    global active_quality_label, quality_mode
    # Setze die Hintergrundfarbe des vorherigen Labels zurück
    if active_quality_label:
        active_quality_label.config(bg=INACTIVE_LABEL_BG)
    
    # Setze das neue Label als aktiv
    label.config(bg=ACTIVE_LABEL_BG)
    active_quality_label = label
    
    # Aktualisiere den ausgewählten Qualitätsmodus
    quality_mode = quality
    print(f"Selected quality: {quality_mode}")

def select_convert(event, label, convert):
    global active_convert_label, convert_mode
    # Setze die Hintergrundfarbe des vorherigen Labels zurück
    if active_convert_label:
        active_convert_label.config(bg=INACTIVE_LABEL_BG)
    
    # Setze das neue Label als aktiv
    label.config(bg=ACTIVE_LABEL_BG)
    active_convert_label = label
    
    # Aktualisiere den ausgewählten Qualitätsmodus
    convert_mode = convert
    print(f"Selected convert: {convert_mode}")


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
            pady=5    # Padding innerhalb des Labels
        )
        label.grid(row=ROWS["QUALITY_BUTTONS"], column=col, padx=5, pady=5, sticky="w")

        # Füge ein Bind-Event hinzu, um die Label-Funktion beim Klicken aufzurufen
        label.bind("<Button-1>", lambda event, l=label, t=text: select_quality(event, l, t))

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
            pady=5    # Padding innerhalb des Labels
        )
        label.grid(row=ROWS["CONVERT_BUTTONS"], column=col, padx=5, pady=5, sticky="w")
        
        # Füge ein Bind-Event hinzu, um die Label-Funktion beim Klicken aufzurufen
        label.bind("<Button-1>", lambda event, l=label, t=text: select_convert(event, l, t))


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


def setup_right_frame(root, progress_display):
    progress_display.grid(row=0, column=2, padx=10, pady=10, sticky="nswe")
    root.grid_columnconfigure(
        2, weight=1
    )  # Adjust weight to 1 for equal width distribution


# --- Download- und Subprozess-Funktionen ---


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


# --- Funktionen zum Bearbeiten der Playlist-Daten ---


def on_select(
    event, tree, textentry_folder, textentry_playlist, textentry_url, playlists_data
):
    tree_selected_item = tree.focus()
    item_text = tree.item(tree_selected_item, "text")
    parent_item = tree.parent(tree_selected_item)

    textentry_folder.delete(0, tk.END)
    textentry_playlist.delete(0, tk.END)
    textentry_url.delete(0, tk.END)

    if parent_item:
        url = playlists_data[tree.item(parent_item, "text")][item_text]
        folder_name = tree.item(parent_item, "text")
        textentry_folder.insert(0, folder_name)
        textentry_playlist.insert(0, item_text)
        textentry_url.insert(0, url)
    else:
        textentry_folder.insert(0, item_text)


def find_item_by_name(tree, name):
    # Diese Funktion durchsucht den Treeview nach einem Element mit dem gegebenen Namen.
    for item in tree.get_children():
        if tree.item(item, "text") == name:
            return item
    return None


def create_folder(tree, textentry_folder, playlists_data, progress_display):
    folder_name = textentry_folder.get()

    if not folder_name:
        print_progress_display(
            progress_display, "Give your folder a nice name!", "red"
        )
        return

    # Überprüfen, ob der Ordnername bereits existiert
    if folder_name not in playlists_data:
        playlists_data[folder_name] = {}
        save_playlists(playlists_data)  # init folder empty
        new_folder_id = tree.insert("", "end", text=folder_name)
        print_progress_display(
            progress_display,
            'Created folder "' + folder_name + '". Such a cool name!',
            "green",
        )
        return new_folder_id
    else:
        # Wenn der Ordner bereits existiert, finde und gib seine ID zurück
        existing_folder_id = find_item_by_name(tree, folder_name)
        if existing_folder_id:
            return existing_folder_id
        else:
            return 0


def create_playlist(
    tree,
    textentry_folder_obj,
    textentry_playlist_obj,
    textentry_url_obj,
    playlists_data,
    progress_display,
):
    tree_selected_item_id = tree.focus()
    tree_has_item = False
    textentry_folder_has_item = False
    selected_folder_name = ""
    selected_folder_id = 0
    textentry_folder_name = textentry_folder_obj.get()

    if tree_selected_item_id:
        tree_has_item = True
    if textentry_folder_name:
        textentry_folder_has_item = True

    if tree_has_item:
        # get tree id and name
        tree_selected_item_parent_id = tree.parent(tree_selected_item_id)
        if tree_selected_item_parent_id:
            # item is folder
            tree_folder_id = tree_selected_item_parent_id
        else:
            # item is playlist
            tree_folder_id = tree_selected_item_id
        tree_folder_name = tree.item(tree_folder_id, "text")

    if not tree_has_item and textentry_folder_has_item:
        selected_folder_name = textentry_folder_name
        selected_folder_id = create_folder(
            tree, textentry_folder_obj, playlists_data, progress_display
        )
    elif tree_has_item and not textentry_folder_has_item:
        selected_folder_name = tree_folder_name
        selected_folder_id = tree_folder_id
    elif tree_has_item and textentry_folder_has_item:
        selected_folder_name = textentry_folder_name
        selected_folder_id = create_folder(
            tree, textentry_folder_obj, playlists_data, progress_display
        )
    elif not tree_has_item and not textentry_folder_has_item:
        print_progress_display(
            progress_display,
            "Select a folder to add a nice playlist!",
            "red",
        )
        return

    # validate playlists
    playlist_name = textentry_playlist_obj.get()
    if not playlist_name:
        print_progress_display(
            progress_display, "Set the name of your TIDAL playlist!", "red"
        )
        return

    # validate url
    playlist_url = textentry_url_obj.get()
    if not playlist_url:
        print_progress_display(
            progress_display, "Set the URL of your TIDAL playlist!", "red"
        )
        return

    # check if folder exists in playlists_data
    if selected_folder_name in playlists_data:
        # Kinder des Elements abrufen
        children = playlists_data[selected_folder_name]

        # get all childs
        print(f"Children of '{selected_folder_name}':")
        for child_name, child_url in children.items():
            print(f"Name: {child_name}, URL: {child_url}")
            if child_name == playlist_name:
                print_progress_display(
                    progress_display, "Playlists already present in this folder", "yellow"
                )
                return
            if child_url == playlist_url:
                print_progress_display(
                    progress_display, "URL is already used in this folder", "yellow"
                )
                return
    else:
        print_progress_display(
            progress_display, "Element " + selected_folder_name + " not found", "red"
        )

    # add to json and tree
    playlists_data[selected_folder_name][playlist_name] = playlist_url
    tree.insert(selected_folder_id, "end", text=playlist_name)
    print_progress_display(
        progress_display,
        "Playlist "
        + playlist_name
        + " added to folder "
        + selected_folder_name
        + ". Cool!",
        "green",
    )

    return


def update_folder(tree, textentry_folder, playlists_data, progress_display):
    # Holen des ausgewählten Elements im Treeview
    selected_item = tree.focus()  # Holt die ID des ausgewählten Elements

    if not selected_item:
        print_progress_display(progress_display, "Please select a folder to update!", "red")
        return

    # Holt den aktuellen Namen des ausgewählten Elements (Ordners)
    current_folder_name = tree.item(selected_item, "text")

    # Den neuen Ordnernamen vom Eingabefeld bekommen
    new_folder_name = textentry_folder.get()

    if not new_folder_name:
        print_progress_display(progress_display, "Please enter a new folder name!", "red")
        return

    # Überprüfen, ob der aktuelle Name des Ordners in den playlists_data existiert
    if current_folder_name in playlists_data:
        # Prüfen, ob der neue Name bereits in playlists_data existiert
        if new_folder_name in playlists_data:
            print_progress_display(progress_display, "Folder name already exists!", "red")
            return

        # Aktualisiere den Treeview mit dem neuen Ordnernamen
        tree.item(selected_item, text=new_folder_name)

        # Aktualisiere die JSON-Datenstruktur (Ordnernamen ändern)
        playlists_data[new_folder_name] = playlists_data.pop(current_folder_name)

        # Änderungen speichern
        save_playlists(playlists_data)

        # Zeige eine Erfolgsmeldung an
        print_progress_display(
            progress_display,
            f'Folder "{current_folder_name}" updated to "{new_folder_name}".',
            "green",
        )
    else:
        print_progress_display(progress_display, "Selected item is not a folder!", "red")


def update_playlist(
    tree,
    textentry_folder,
    textentry_playlist,
    textentry_url,
    playlists_data,
    progress_display,
):
    # Holt die ausgewählte Playlist
    selected_item = tree.focus()  # ID der ausgewählten Playlist

    if not selected_item:
        print_progress_display(progress_display, "Please select a playlist to update!", "red")
        return

    # Holt den aktuellen Namen und URL der ausgewählten Playlist
    current_playlist_name = tree.item(selected_item, "text")

    # Den neuen Ordnernamen, Playlistnamen und die neue URL aus den Eingabefeldern holen
    new_folder_name = textentry_folder.get()
    new_playlist_name = textentry_playlist.get()
    new_playlist_url = textentry_url.get()

    if not new_playlist_name:
        print_progress_display(progress_display, "Please enter a new playlist name!", "red")
        return
    if not new_playlist_url:
        print_progress_display(progress_display, "Please enter a new playlist URL!", "red")
        return

    # Sucht das aktuelle Parent-Element (Ordner), in dem die Playlist liegt
    parent_item = tree.parent(selected_item)
    current_folder_name = tree.item(parent_item, "text") if parent_item else None

    # Prüfen, ob ein neuer Ordnername eingegeben wurde
    if new_folder_name and current_folder_name != new_folder_name:
        # Prüfen, ob der neue Ordner existiert
        new_folder_id = None
        for item_id in tree.get_children():
            if tree.item(item_id, "text") == new_folder_name:
                new_folder_id = item_id
                break

        if new_folder_id:
            # Verschiebe die Playlist in den neuen Ordner
            playlists_data[new_folder_name][new_playlist_name] = playlists_data[current_folder_name].pop(current_playlist_name)
            save_playlists(playlists_data)

            # Update den Tree: Entferne die Playlist aus dem alten Ordner und füge sie dem neuen hinzu
            tree.delete(selected_item)
            new_item_id = tree.insert(new_folder_id, "end", text=new_playlist_name)
            print_progress_display(progress_display, f'Playlist "{current_playlist_name}" moved to folder "{new_folder_name}".', "green")

        else:
            print_progress_display(progress_display, "New folder does not exist!", "red")
            return
    else:
        # Ordner bleibt gleich, nur Name oder URL werden geändert
        if current_folder_name and current_playlist_name in playlists_data[current_folder_name]:
            # Aktualisiere den Namen und die URL der Playlist im JSON-Daten
            playlists_data[current_folder_name].pop(current_playlist_name)
            playlists_data[current_folder_name][new_playlist_name] = new_playlist_url
            save_playlists(playlists_data)

            # Aktualisiere den Tree mit dem neuen Playlistnamen
            tree.item(selected_item, text=new_playlist_name)
            print_progress_display(
                progress_display,
                f'Playlist "{current_playlist_name}" updated successfully.',
                "green",
            )
        else:
            print_progress_display(
                progress_display, "Selected item is not a valid playlist!", "red"
            )


def update_item(
    tree,
    textentry_folder,
    textentry_playlist,
    textentry_url,
    playlists_data,
    progress_display,
):
    # Holt den aktuell ausgewählten Eintrag aus dem Treeview
    tree_selected_item_id = tree.focus()

    if not tree_selected_item_id:
        print("no item selected in tree")
        print_progress_display(
            progress_display, "No item is selected!", "red"
        )
        return

    if not tree.parent(tree_selected_item_id):
        update_folder(tree, textentry_folder, playlists_data, progress_display)
    else:
        update_playlist(
            tree,
            textentry_folder,
            textentry_playlist,
            textentry_url,
            playlists_data,
            progress_display,
        )

    return


def remove_item(tree, playlists_data):
    # Aktuell ausgewähltes Element im Treeview
    tree_selected_item = tree.focus()
    item_text = tree.item(tree_selected_item, "text")
    parent_item = tree.parent(tree_selected_item)

    if parent_item:  # Wenn das ausgewählte Item eine Playlist ist
        # Der Ordner, in dem die Playlist liegt
        folder = tree.item(parent_item, "text")

        # Lösche die Playlist aus dem entsprechenden Ordner im JSON
        if item_text in playlists_data[folder]:
            del playlists_data[folder][item_text]

        # Lösche nur die Playlist aus dem Treeview
        tree.delete(tree_selected_item)

    else:  # Wenn das ausgewählte Item ein Ordner ist
        # Lösche den Ordner direkt
        if item_text in playlists_data:
            del playlists_data[item_text]
        
        # Lösche den Ordner aus dem Treeview
        tree.delete(tree_selected_item)

    # Speichere die aktualisierte JSON-Struktur
    save_playlists(playlists_data)


# --- Main-Funktion ---


def main():
    playlists_data = load_playlists()
    config = load_config()

    root = tk.Tk()
    root.title("uDJ Tool")
    root.configure(bg="black")
    root.geometry(WINDOW_SIZE)
    root.resizable(False, False)

    # tk.Label(root, bg="#FF2288", height=100, width=3).grid(
    #     row=0, column=0, columnspan=10, rowspan=10, padx=5, pady=5, sticky="nw"
    # )

    # create_stripes(root, 30, PRIMARY_COLOR, SECONDARY_COLOR)

    progress_display = tk.Text(
        root,
        width=50,
        wrap=tk.WORD,
        bg="black",
        fg="white",
        highlightthickness=1,  # Dünne Umrandung
        highlightbackground="pink",  # Farbe der Umrandung
        highlightcolor="pink",  # Farbe, wenn es den Fokus hat
        relief="ridge",  # Stil der Umrandung
        bd=1  # Dicke der Umrandung
    )
    progress_display.tag_configure("orange", foreground="orange")
    progress_display.tag_configure("black", foreground="black")
    progress_display.tag_configure("red", foreground="red")
    progress_display.tag_configure("green", foreground="green")
    progress_display.tag_configure("white", foreground="white")
    progress_display.tag_configure("yellow", foreground="yellow")

    progress_display.insert(1.0, welcome_text)

    left_frame = tk.Frame(root, bg=PRIMARY_COLOR, width=200)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
    left_frame.grid_propagate(False)
    left_frame.grid_columnconfigure(0, weight=1)
    left_frame.grid_rowconfigure(0, weight=1)
    tree = ttk.Treeview(left_frame)

    center_frame_entries = setup_center_frame(
        root, playlists_data, tree, config=config, progress_display=progress_display
    )
    setup_left_frame(tree, playlists_data, on_select, center_frame_entries)
    setup_right_frame(root, progress_display)

    # Konfiguriere die Spalten des root Fensters
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()
