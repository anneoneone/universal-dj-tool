from tkinter import ttk


from constants import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
)


def setup_treeview(tree, playlists_data):
    for folder, urls in playlists_data.items():
        folder_id = tree.insert("", "end", text=folder)
        for url_name in urls:
            tree.insert(folder_id, "end", text=url_name)


def setup_left_frame(tree, playlists_data, on_select_tree_item, center_frame_entries):
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
        lambda event: on_select_tree_item(
            event,
            tree,
            textentry_folder,
            textentry_playlist,
            textentry_url,
            playlists_data,
        ),
    )
