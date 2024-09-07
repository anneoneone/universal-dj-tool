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

    # Start threads to capture both stdout and stderr
    threading.Thread(target=update_text_widget, args=(process.stdout,)).start()
    threading.Thread(target=update_text_widget, args=(process.stderr,)).start()

    process.wait()  # Wait for the process to complete
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

    # Run the download in a separate thread to avoid freezing the GUI
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


def main():
    playlists_data = load_playlists()
    config = load_config()

    root = tk.Tk()
    root.title("uDJ Tool")

    left_frame = ttk.Frame(root)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

    tk.Label(left_frame, text="Playlists").pack(anchor="nw", padx=5, pady=5)
    tree = ttk.Treeview(left_frame)
    tree.pack(fill="both", expand=True)

    setup_treeview(tree, playlists_data)

    tree.bind(
        '<<TreeviewSelect>>',
        lambda event: on_select(
            event, tree, folder_entry, url_entry, playlists_data
        )
    )

    progress_label = tk.Label(left_frame, text="Progress")
    progress_label.pack(anchor="nw", padx=5, pady=5)
    progress_text = tk.StringVar()
    progress_display = tk.Label(
        left_frame,
        textvariable=progress_text,
        height=4,
        width=40,
        relief="sunken"
    )
    progress_display.pack(anchor="nw", padx=5, pady=5)

    right_frame = ttk.Frame(root)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

    tk.Label(right_frame, text="Folder").grid(
        row=0, column=0, padx=5, pady=5, sticky="w"
    )
    folder_entry = tk.Entry(right_frame)
    folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(right_frame, text="URL").grid(
        row=0, column=2, padx=5, pady=5, sticky="w"
    )
    url_entry = tk.Entry(right_frame)
    url_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Button(right_frame, text="Add", command=lambda: add_item(
        tree, folder_entry, url_entry, playlists_data)
    ).grid(row=1, column=0, padx=5, pady=5)

    tk.Button(right_frame, text="Edit", command=lambda: edit_item(
        tree, folder_entry, url_entry, playlists_data)
    ).grid(row=1, column=1, padx=5, pady=5)

    tk.Button(right_frame, text="Remove", command=lambda: remove_item(
        tree, playlists_data)
    ).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(right_frame, text="Filter").grid(
        row=2, column=0, padx=5, pady=5, sticky="w"
    )
    filter_entry = tk.Entry(right_frame)
    filter_entry.grid(row=2,
                      column=1,
                      columnspan=3,
                      padx=5,
                      pady=5,
                      sticky="w"
                      )

    download_button = tk.Button(
        right_frame,
        text="Download",
        command=lambda: download(
            config, playlists_data, filter_entry, progress_display
        ),
    )
    download_button.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

    # Text widget to display the output of tidal-dl
    progress_display = tk.Text(left_frame, height=15, width=50, wrap=tk.WORD)
    progress_display.pack(anchor="nw", padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
