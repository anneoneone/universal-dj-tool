import tkinter as tk
from tkinter import ttk
from utils import load_playlists, load_config

from left_frame import setup_left_frame
from center_frame import setup_center_frame
from progress_display import create_progress_display
from constants import (
    WINDOW_SIZE,
    PRIMARY_COLOR,
)


# --- Funktionen zur GUI-Erstellung ---


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


def setup_right_frame(root, progress_display):
    progress_display.grid(row=0, column=2, padx=10, pady=10, sticky="nswe")
    root.grid_columnconfigure(
        2, weight=1
    )  # Adjust weight to 1 for equal width distribution


# --- Download- und Subprozess-Funktionen ---


# --- Funktionen zum Bearbeiten der Playlist-Daten ---


def on_select_tree_item(
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

    progress_display = create_progress_display(root)

    left_frame = tk.Frame(root, bg=PRIMARY_COLOR, width=200)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
    left_frame.grid_propagate(False)
    left_frame.grid_columnconfigure(0, weight=1)
    left_frame.grid_rowconfigure(0, weight=1)
    tree = ttk.Treeview(left_frame)

    center_frame_entries = setup_center_frame(
        root, playlists_data, tree, config=config, progress_display=progress_display
    )
    setup_left_frame(tree, playlists_data, on_select_tree_item, center_frame_entries)
    setup_right_frame(root, progress_display)

    # Konfiguriere die Spalten des root Fensters
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()
