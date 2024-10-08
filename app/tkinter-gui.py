import tkinter as tk
from tkinter import ttk
from utils import load_playlists, save_playlists, load_config
from download_playlists import download_playlists
import subprocess
import threading

WINDOW_SIZE = "1000x700"
PRIMARY_COLOR = "#8822FF"
SECONDARY_COLOR = "#FF2288"
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
│                __      \ \ \/\ \\/__/\ \     │
│              /'__`\     \ \ \ \ \  _\ \ \    │
│             /\ \L\.\_    \ \ \_\ \/\ \_\ \   │
│             \ \__/.\_\    \ \____/\ \____/   │
│              \/__/\/_/     \/___/  \/___/    │
│   ______                 ___        __       │
│  /\__  _\               /\_ \      /\ \      │
│  \/_/\ \/    ___     ___\//\ \     \ \ \     │
│     \ \ \   / __`\  / __`\\ \ \     \ \ \    │
│      \ \ \ /\ \L\ \/\ \L\ \\_\ \_    \ \_\   │
│       \ \_\\ \____/\ \____//\____\    \/\_\  │
│        \/_/ \/___/  \/___/ \/____/     \/_/  │
│                                              │
│                                              │
└──────────────────────────────────────────────┘


"""

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

# --- Helper Functions ---


def print_progress_display(progress_display, text, tag="white"):
    symbol = ""
    if tag == "white":
        symbol = "✓ "
    elif tag == "yellow":
        symbol = "⚠ "
    elif tag == "black":
        symbol = "✗ "
    progress_display.insert(tk.END, symbol + text + "\n", tag)
    progress_display.see(tk.END)


# --- Download- und Subprozess-Funktionen ---


def run_tidal_dl(link, download_dir, text_widget):
    process = subprocess.Popen(
        ["tidal-dl", "-l", link, "-o", download_dir],
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


def on_select(event, tree, textentry_folder, textentry_playlist, textentry_url, playlists_data):
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


def update_item(tree, textentry_folder, textentry_url, playlists_data):
    # Holt den aktuell ausgewählten Eintrag aus dem Treeview
    tree_selected_item = tree.selection()

    if not tree_selected_item:
        print("No item selected for update.")
        return

    # Holt den ursprünglichen Namen und die neue Werte aus den Eingabefeldern
    item_text = tree.item(tree_selected_item, "text")
    new_folder_name = textentry_folder.get()
    new_url = textentry_url.get()

    # Überprüfen, ob die neuen Eingaben gültig sind
    if not new_folder_name:
        textentry_folder.insert(0, "INSERT NAME HERE!")
        return
    if not new_url:
        textentry_url.insert(0, "INSERT URL HERE!")
        return

    # Überprüfen, ob das ausgewählte Element ein Ordner oder eine Playlist ist
    if item_text in playlists_data:
        # Es handelt sich um einen Ordner
        playlists_data[new_folder_name] = playlists_data.pop(item_text)
        # Aktualisiere den Treeview-Eintrag
        tree.item(tree_selected_item, text=new_folder_name)
    else:
        # Es handelt sich um eine Playlist, daher müssen wir den Ordner durchsuchen
        parent_item = tree.parent(tree_selected_item)
        if parent_item:  # Die Playlist befindet sich in einem Ordner
            parent_name = tree.item(parent_item, "text")
            if (
                parent_name in playlists_data
                and item_text in playlists_data[parent_name]
            ):
                playlists_data[parent_name][new_folder_name] = playlists_data[
                    parent_name
                ].pop(item_text)
        else:  # Die Playlist befindet sich auf der obersten Ebene
            playlists_data[new_folder_name] = playlists_data.pop(item_text)

        # URL aktualisieren, wenn sich diese geändert hat
        if new_url != playlists_data[new_folder_name]:
            playlists_data[new_folder_name] = new_url

        # Aktualisiere den Treeview-Eintrag
        tree.item(tree_selected_item, text=new_folder_name)

    # Speichert die aktualisierten Playlists im JSON-Objekt
    save_playlists(playlists_data)


# Funktion zum Löschen eines Eintrags
def remove_item(tree, playlists_data):
    tree_selected_item = tree.focus()
    item_text = tree.item(tree_selected_item, "text")
    parent_item = tree.parent(tree_selected_item)

    if parent_item:
        folder = tree.item(parent_item, "text")
        del playlists_data[folder][item_text]
        if not playlists_data[folder]:
            del playlists_data[folder]
    else:
        del playlists_data[item_text]

    save_playlists(playlists_data)
    tree.delete(tree_selected_item)


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
            tree_folder_id = tree_selected_item_parent_id
        else:
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
            "Select a folder or type a folder name to add a nice playlist!",
            "black",
        )
        return

    # validate playlists
    playlist_name = textentry_playlist_obj.get()
    if not playlist_name:
        print_progress_display(
            progress_display, "Set the name of your TIDAL playlist!", "black"
        )
        return

    # validate url
    playlist_url = textentry_url_obj.get()
    if not playlist_url:
        print_progress_display(
            progress_display, "Set the URL of your TIDAL playlist!", "black"
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
            progress_display, "Element " + selected_folder_name + " not found", "black"
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
            progress_display, "Give your folder a nice name!", "black"
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
            "white",
        )
        return new_folder_id
    else:
        # Wenn der Ordner bereits existiert, finde und gib seine ID zurück
        existing_folder_id = find_item_by_name(tree, folder_name)
        if existing_folder_id:
            return existing_folder_id
        else:
            return 0


def create_folder_button_fn(tree, textentry_folder, playlists_data, progress_display):
    if create_folder(tree, textentry_folder, playlists_data, progress_display) > 0:
        print_progress_display(
            progress_display, "This folder already exists. Pick another name!", "yellow"
        )


# --- Funktionen zur GUI-Erstellung ---


def setup_treeview(tree, playlists_data):
    for folder, urls in playlists_data.items():
        folder_id = tree.insert("", "end", text=folder)
        for url_name in urls:
            tree.insert(folder_id, "end", text=url_name)


def create_clickable_label(parent, text, command, bg=PRIMARY_COLOR, fg="white"):
    label = tk.Label(
        parent,
        text=text,
        font=("Comic Sans MS", 16, "bold"),
        relief=tk.RAISED,
        bg=bg,
        fg=fg,
        border=1,
        borderwidth=3,
        cursor="hand2",
    )
    label.bind("<Button-1>", lambda e: command())

    return label


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


class HoverLabel(tk.Label):

    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.configure(
            cursor="hand2",
            compound="left",
            state="active",
            font=("Comic Sans MS", 16, "bold"),
            relief=tk.RAISED,
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
            self.configure(bg=new_bg, relief=tk.SUNKEN)
            self.after_id = self.after(200, self.toggle_background)

    def on_enter(self, event):
        self.is_hovering = True
        self.toggle_background()

    def on_leave(self, event):
        self.is_hovering = False
        if self.after_id:
            self.after_cancel(self.after_id)
        self.configure(bg=self.default_bg, fg=self.default_fg, relief=tk.RAISED)

    def on_click(self, event):
        if self.command:
            # self.configure(state="disabled")
            self.command()


def create_hover_label(parent, text, command, **kwargs):
    return HoverLabel(parent, text=text, command=command, **kwargs)


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


def setup_center_frame(root, playlists_data, tree, config, progress_display):
    center_frame = tk.Frame(root, bg=PRIMARY_COLOR, width=200)
    center_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
    center_frame.grid_columnconfigure(
        0, weight=1
    )  # Adjust weight to 1 for equal width distribution
    center_frame.grid_columnconfigure(1, weight=1)
    center_frame.grid_columnconfigure(2, weight=1)
    center_frame.grid_columnconfigure(3, weight=1)

    # SELECT TARGET DIRECTORY

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
            tree, textentry_folder, textentry_playlist, textentry_url, playlists_data, progress_display
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
        lambda: update_item(tree, textentry_folder, textentry_url, playlists_data),
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

    tk.Label(center_frame, text="Normal", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["QUALITY_BUTTONS"], column=0, padx=5, pady=5, sticky="w"
    )
    tk.Label(center_frame, text="High", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["QUALITY_BUTTONS"], column=1, padx=5, pady=5, sticky="w"
    )
    tk.Label(center_frame, text="HiFi", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["QUALITY_BUTTONS"], column=2, padx=5, pady=5, sticky="w"
    )
    tk.Label(center_frame, text="Master", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["QUALITY_BUTTONS"], column=3, padx=5, pady=5, sticky="w"
    )

    # CONVERT
    tk.Label(center_frame, text="Convert", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["CONVERT_TITLE_LABEL"], column=0, padx=5, pady=5, sticky="w"
    )

    tk.Label(center_frame, text="mp3", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["CONVERT_BUTTONS"], column=0, columnspan=2, padx=5, pady=5, sticky="w"
    )
    tk.Label(center_frame, text="wav", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["CONVERT_BUTTONS"], column=2, columnspan=1, padx=5, pady=5, sticky="w"
    )
    tk.Label(center_frame, text="aiff", bg=SECONDARY_COLOR, fg="white").grid(
        row=ROWS["CONVERT_BUTTONS"], column=3, columnspan=1, padx=5, pady=5, sticky="w"
    )

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

    return textentry_folder, textentry_playlist, textentry_url


def setup_right_frame(root, progress_display):
    progress_display.grid(row=0, column=2, padx=10, pady=10, sticky="nswe")
    root.grid_columnconfigure(
        2, weight=1
    )  # Adjust weight to 1 for equal width distribution


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

    create_stripes(root, 30, "red", "green")

    progress_display = tk.Text(
        root,
        # height=15,
        width=50,
        border=0,
        borderwidth=0,
        wrap=tk.WORD,
        bg="#8822FF",
        fg="white",
        highlightthickness=0,
        # insertbackground="white",
        # relief="solid",
        # bd=2
    )
    progress_display.tag_configure("orange", foreground="orange")
    progress_display.tag_configure("black", foreground="black")
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
