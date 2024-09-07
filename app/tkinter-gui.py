import tkinter as tk
from tkinter import ttk
from utils import load_playlists, save_playlists, load_config
from download_playlists import download_playlists
import subprocess
import threading


def run_tidal_dl(link, download_dir, text_widget):
    process = subprocess.Popen(
        ["tidal-dl", "-l", link, "-o", download_dir],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
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


def download(config, playlists_data, filter_entry, text_widget):
    def download_thread():
        music_directory = config['music_directory']

        for category_name, category_playlists in playlists_data.items():
            for link_name, link in category_playlists.items():
                if filter_entry.get().lower() in link_name.lower():
                    download_dir = f"{music_directory}/{category_name}/{link_name}"
                    run_tidal_dl(link, download_dir, text_widget)

    threading.Thread(target=download_thread).start()


def on_select(event, tree, folder_entry, url_entry, playlists_data):
    selected_item = tree.focus()
    item_text = tree.item(selected_item, "text")
    parent_item = tree.parent(selected_item)

    folder_entry.delete(0, tk.END)
    url_entry.delete(0, tk.END)

    if parent_item:
        url = playlists_data[tree.item(parent_item, 'text')][item_text]
        folder_entry.insert(0, item_text)
        url_entry.insert(0, url)
    else:
        folder_entry.insert(0, item_text)


def edit_item(tree, folder_entry, url_entry, playlists_data):
    selected_item = tree.focus()
    item_text = tree.item(selected_item, 'text')
    parent_item = tree.parent(selected_item)

    new_folder_name = folder_entry.get()
    new_url = url_entry.get()

    if parent_item:
        folder = tree.item(parent_item, 'text')
        playlists_data[folder][new_folder_name] = new_url

        if new_folder_name != item_text:
            del playlists_data[folder][item_text]

        save_playlists(playlists_data)
        tree.item(selected_item, text=new_folder_name)
    else:
        if new_folder_name != item_text:
            playlists_data[new_folder_name] = playlists_data.pop(item_text)
            save_playlists(playlists_data)
            tree.item(selected_item, text=new_folder_name)


def remove_item(tree, playlists_data):
    selected_item = tree.focus()
    item_text = tree.item(selected_item, 'text')
    parent_item = tree.parent(selected_item)

    if parent_item:
        folder = tree.item(parent_item, 'text')
        del playlists_data[folder][item_text]
        if not playlists_data[folder]:
            del playlists_data[folder]
    else:
        del playlists_data[item_text]

    save_playlists(playlists_data)
    tree.delete(selected_item)


def add_item(tree, folder_entry, url_entry, playlists_data):
    selected_item = tree.focus()
    new_folder_name = folder_entry.get()
    new_url = url_entry.get()

    if not selected_item:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, "Please select playlist directory")
        return

    parent_item = tree.item(selected_item, 'text')
    if tree.parent(selected_item):
        parent_item = tree.item(tree.parent(selected_item), 'text')

    if new_url:
        playlists_data[parent_item][new_folder_name] = new_url
        tree.insert(selected_item, "end", text=new_folder_name)
    else:
        playlists_data[new_folder_name] = {}
        tree.insert("", "end", text=new_folder_name)

    save_playlists(playlists_data)


def setup_treeview(tree, playlists_data):
    for folder, urls in playlists_data.items():
        folder_id = tree.insert("", "end", text=folder)
        for url_name in urls:
            tree.insert(folder_id, "end", text=url_name)


# master: Misc | None = None,
#     cnf: dict[str, Any] | None = {},
#     *,
#     activebackground: str = ...,
#     activeforeground: str = ...,
#     anchor: _Anchor = "center",
#     background: str = ...,
#     bd: _ScreenUnits = ...,
#     bg: str = ...,
#     bitmap: str = "",
#     border: _ScreenUnits = ...,
#     borderwidth: _ScreenUnits = ...,
#     compound: _Compound = "none",
#     cursor: _Cursor = "",
#     disabledforeground: str = ...,
#     fg: str = ...,
#     font: _FontDescription = "TkDefaultFont",
#     foreground: str = ...,
#     height: _ScreenUnits = 0,
#     highlightbackground: str = ...,
#     highlightcolor: str = ...,
#     highlightthickness: _ScreenUnits = 0,
#     image: _ImageSpec = "",
#     justify: Literal['left', 'center', 'right'] = "center",
#     name: str = ...,
#     padx: _ScreenUnits = 1,
#     pady: _ScreenUnits = 1,
#     relief: _Relief = "flat",
#     state: Literal['normal', 'active', 'disabled'] = "normal",
#     takefocus: _TakeFocusValue = 0,
#     text: float | str = "",
#     textvariable: Variable = ...,
#     underline: int = -1,
#     width: _ScreenUnits = 0,
#     wraplength: _ScreenUnits = 0


def create_clickable_label(parent, text, command, bg="black", fg="white"):
    label = tk.Label(parent, 
                     text=text, 
                     font=("Comic Sans MS", 16, "bold"),
                     relief=tk.RAISED,
                     bg=bg, fg=fg, border=1, borderwidth=3, cursor="hand2")
    label.bind("<Button-1>", lambda e: command())

    return label

class HoverLabel(tk.Label):
    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.default_bg = self.cget("bg")
        self.default_fg = self.cget("fg")
        self.command = command
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        self.configure(bg=self.default_fg, fg=self.default_bg)

    def on_leave(self, event):
        self.configure(bg=self.default_bg, fg=self.default_fg)

    def on_click(self, event):
        if self.command:
            self.command()

def create_hover_label(parent, text, command, **kwargs):
    return HoverLabel(parent, text=text, command=command, **kwargs)


def main():
    playlists_data = load_playlists()
    config = load_config()

    root = tk.Tk()
    root.title("uDJ Tool")
    root.configure(bg="black")

    # Left Frame
    left_frame = tk.Frame(root, bg="black")
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

    tk.Label(left_frame, text="Playlists", bg="black", fg="white").grid(
        row=0, column=0, padx=5, pady=5, sticky="nw"
    )
    tree = ttk.Treeview(left_frame)
    tree.grid(row=1, column=0, padx=5, pady=5, sticky="nswe")

    setup_treeview(tree, playlists_data)

    tree.bind(
        '<<TreeviewSelect>>',
        lambda event: on_select(
            event, tree, folder_entry, url_entry, playlists_data
        )
    )

    # Progress Label
    tk.Label(left_frame, text="Progress", bg="black", fg="white").grid(
        row=2, column=0, padx=5, pady=5, sticky="nw"
    )
    progress_display = tk.Text(
        left_frame,
        height=15,
        width=50,
        wrap=tk.WORD,
        bg="black",
        fg="white",
        insertbackground="white",
        relief="solid",
        bd=2
    )
    progress_display.grid(row=3, column=0, padx=5, pady=5)
    progress_display.configure(highlightbackground="blue", highlightcolor="blue")

    # Right Frame
    right_frame = tk.Frame(root, bg="black")
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

    tk.Label(right_frame, text="Folder", bg="black", fg="white").grid(
        row=0, column=0, padx=5, pady=5, sticky="w"
    )
    folder_entry = tk.Entry(right_frame, bg="black", fg="white", insertbackground="white")
    folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(right_frame, text="URL", bg="black", fg="white").grid(
        row=0, column=2, padx=5, pady=5, sticky="w"
    )
    url_entry = tk.Entry(right_frame, bg="black", fg="white", insertbackground="white")
    url_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    # Replace buttons with clickable labels
    create_clickable_label(
        right_frame, "Add", lambda: add_item(tree, folder_entry, url_entry, playlists_data),
        bg="black", fg="white"
    ).grid(row=1, column=0, padx=5, pady=5)
    
    create_clickable_label(
        right_frame, "Edit", lambda: edit_item(tree, folder_entry, url_entry, playlists_data),
        bg="black", fg="white"
    ).grid(row=1, column=1, padx=5, pady=5)

    create_clickable_label(
        right_frame, "Remove", lambda: remove_item(tree, playlists_data),
        bg="black", fg="white"
    ).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(right_frame, text="Filter", bg="black", fg="white").grid(
        row=2, column=0, padx=5, pady=5, sticky="w"
    )
    filter_entry = tk.Entry(right_frame, bg="black", fg="white", insertbackground="white")
    filter_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")

    create_hover_label(
        right_frame, "Download", lambda: download(
            config, playlists_data, filter_entry, progress_display),
        bg="black", fg="white", font=("Comic Sans MS", 12)
    ).grid(row=3, column=0, columnspan=4, padx=5, pady=5)

    # create_clickable_label(
    #     right_frame, "Download", lambda: download(
    #         config, playlists_data, filter_entry, progress_display),
    #     bg="#3300FF", fg="white"
    # ).grid(row=3, column=0, columnspan=1, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
