import tkinter as tk
from tkinter import ttk
from utils import load_playlists, save_playlists, load_config
from download_playlists import download_playlists


# Funktion, die ausgeführt wird, wenn ein Treeview-Item ausgewählt wird
def on_select(event):
    selected_item = tree.focus()  # Gibt den selektierten Item-Schlüssel zurück
    item_text = tree.item(selected_item, "text")  # Holt den Text des ausgewählten Items

    parent_item = tree.parent(selected_item)  # Holt den Parent-Item-Schlüssel (Kategorie)

    if parent_item:  # Wenn es einen Parent gibt, ist es ein Sub-Item
        url = playlists_data[tree.item(parent_item, 'text')][item_text]

        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, item_text)  # Füge den Namen des Sub-Items ein

        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)
    else:  # Wenn es keinen Parent gibt, ist es eine Kategorie
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, item_text)  # Füge den Namen der Kategorie ein

        url_entry.delete(0, tk.END)


# Bearbeiten der Playlists
def edit_item():
    selected_item = tree.focus()  # Das aktuell ausgewählte Element im Treeview
    item_text = tree.item(selected_item, 'text')  # Der Text des ausgewählten Elements

    parent_item = tree.parent(selected_item)  # Der Parent des ausgewählten Elements (falls vorhanden)

    new_folder_name = folder_entry.get()
    new_url = url_entry.get()

    if parent_item:  # Es ist ein Sub-Item
        folder = tree.item(parent_item, 'text')

        # Aktualisiere die Werte im JSON
        playlists_data[folder][new_folder_name] = new_url

        # Entferne das alte Sub-Item
        if new_folder_name != item_text:
            del playlists_data[folder][item_text]

        # Speichere die aktualisierte JSON-Datei
        save_playlists(playlists_data)

        # Aktualisiere den Treeview
        tree.item(selected_item, text=new_folder_name)

    else:  # Es ist eine Kategorie
        # Aktualisiere die Kategorie im JSON
        if new_folder_name != item_text:
            playlists_data[new_folder_name] = playlists_data.pop(item_text)

            # Speichere die aktualisierte JSON-Datei
            save_playlists(playlists_data)

            # Aktualisiere den Treeview
            tree.item(selected_item, text=new_folder_name)


# Entfernen der Playlists
def remove_item():
    selected_item = tree.focus()  # Das aktuell ausgewählte Element im Treeview
    item_text = tree.item(selected_item, 'text')  # Der Text des ausgewählten Elements

    parent_item = tree.parent(selected_item)  # Der Parent des ausgewählten Elements (falls vorhanden)

    if parent_item:  # Es ist ein Sub-Item
        folder = tree.item(parent_item, 'text')
        
        # Entferne das Sub-Item aus dem JSON
        del playlists_data[folder][item_text]
        
        # Falls der Ordner jetzt leer ist, entferne ihn auch
        if not playlists_data[folder]:
            del playlists_data[folder]

        # Speichere die aktualisierte JSON-Datei
        save_playlists(playlists_data)

        # Entferne das Sub-Item aus dem Treeview
        tree.delete(selected_item)

    else:  # Es ist eine Kategorie
        # Entferne die Kategorie aus dem JSON
        del playlists_data[item_text]

        # Speichere die aktualisierte JSON-Datei
        save_playlists(playlists_data)

        # Entferne die Kategorie aus dem Treeview
        tree.delete(selected_item)


# Hinzufügen einer neuen Playlist oder Kategorie
def add_item():
    selected_item = tree.focus()  # Das aktuell ausgewählte Element im Treeview

    new_folder_name = folder_entry.get()
    new_url = url_entry.get()

    if not selected_item:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, "Please select playlist directory")
        return

    if new_url:  # Ein Sub-Item wird hinzugefügt
        parent_item = tree.item(selected_item, 'text')

        # Prüfen, ob das ausgewählte Element eine Kategorie ist
        if tree.parent(selected_item):
            parent_item = tree.item(tree.parent(selected_item), 'text')

        # Sub-Item zur Kategorie hinzufügen
        playlists_data[parent_item][new_folder_name] = new_url

        # Speichere die aktualisierte JSON-Datei
        save_playlists(playlists_data)

        # Füge das neue Sub-Item zum Treeview hinzu
        tree.insert(selected_item, "end", text=new_folder_name)

    else:  # Eine neue Kategorie wird hinzugefügt
        # Kategorie zum JSON hinzufügen
        playlists_data[new_folder_name] = {}

        # Speichere die aktualisierte JSON-Datei
        save_playlists(playlists_data)

        # Füge die neue Kategorie zum Treeview hinzu
        tree.insert("", "end", text=new_folder_name)


def download(config, playlists_data, filter_entry):
    print(config)
    music_directory = config['music_directory']
    download_format = config['download_format']

    for category_name, category_playlists in playlists_data.items():
        download_playlists(
            music_directory,
            download_format,
            category_name,
            category_playlists,
            filter_entry.get()
        )


# Lade die Playlists-Daten
playlists_data = load_playlists()
config = load_config()

# Hauptfenster erstellen
root = tk.Tk()
root.title("uDJ Tool")

# Linker Bereich
left_frame = ttk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

# Playlists-Anzeige
playlists_label = tk.Label(left_frame, text="Playlists")
playlists_label.pack(anchor="nw", padx=5, pady=5)

# Erstelle das Treeview für Playlists
tree = ttk.Treeview(left_frame)
tree.pack(fill="both", expand=True)

# Füge die Kategorien und Playlists zum Treeview hinzu
for folder, urls in playlists_data.items():
    folder_id = tree.insert("", "end", text=folder)  # Fügt die Kategorie als Ordner hinzu
    for url_name, url_link in urls.items():
        tree.insert(folder_id, "end", text=url_name)  # Fügt die Playlists zur Kategorie hinzu

# Binde die Auswahl-Callback-Funktion an das Treeview
tree.bind('<<TreeviewSelect>>', on_select)

# Progress-Anzeige
progress_label = tk.Label(left_frame, text="Progress")
progress_label.pack(anchor="nw", padx=5, pady=5)

progress_text = tk.StringVar()
progress_display = tk.Label(left_frame, textvariable=progress_text, height=4, width=40, relief="sunken")
progress_display.pack(anchor="nw", padx=5, pady=5)

# Rechter Bereich
right_frame = ttk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

# Ordner und URL Eingabefelder
folder_label = tk.Label(right_frame, text="Ordner")
folder_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
folder_entry = tk.Entry(right_frame)
folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

url_label = tk.Label(right_frame, text="URL")
url_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
url_entry = tk.Entry(right_frame)
url_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

# Buttons Add, Edit, Remove
add_button = tk.Button(right_frame, text="Add", command=add_item)
add_button.grid(row=1, column=0, padx=5, pady=5)

edit_button = tk.Button(right_frame, text="Edit", command=edit_item)
edit_button.grid(row=1, column=1, padx=5, pady=5)

remove_button = tk.Button(right_frame, text="Remove", command=remove_item)
remove_button.grid(row=1, column=2, padx=5, pady=5)

# Filter-Eingabefeld und Download-Button
filter_label = tk.Label(right_frame, text="Filter")
filter_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
filter_entry = tk.Entry(right_frame)
filter_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")

download_button = tk.Button(
    right_frame,
    text="Download",
    command=lambda: download(config, playlists_data, filter_entry),
)
download_button.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()
