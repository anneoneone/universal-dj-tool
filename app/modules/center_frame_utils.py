import tkinter as tk
import subprocess
import threading
import os
import signal

from modules.progress_display import print_progress_display
from modules.utils import save_playlists, get_config_par, set_config_par, save_config
from modules.constants import (
    ACTIVE_LABEL_BG,
    INACTIVE_LABEL_BG,
)

current_process = None
is_downloading = False

quality_mode = None
convert_mode = None
active_quality_label = None  # Speichert das aktuell aktive Label
active_convert_label = None  # Speichert das aktuell aktive Label


def set_quality_mode(event=None, label=None, quality=None):
    global active_quality_label, quality_mode

    # Setze die Hintergrundfarbe des vorherigen Labels zurück
    if active_quality_label:
        active_quality_label.config(bg=INACTIVE_LABEL_BG)

    # Setze das neue Label als aktiv
    label.config(bg=ACTIVE_LABEL_BG)
    active_quality_label = label

    # Aktualisiere den ausgewählten Qualitätsmodus
    quality_mode = quality

    set_config_par('quality_mode', quality_mode)
    save_config()
    print(f"Selected quality: {quality_mode}")


def set_convert_mode(event=None, label=None, convert=None):
    global active_convert_label, convert_mode

    # Setze die Hintergrundfarbe des vorherigen Labels zurück
    if active_convert_label:
        active_convert_label.config(bg=INACTIVE_LABEL_BG)

    # Setze das neue Label als aktiv
    label.config(bg=ACTIVE_LABEL_BG)
    active_convert_label = label

    # Aktualisiere den ausgewählten Qualitätsmodus
    convert_mode = convert

    set_config_par('convert_mode', convert_mode)
    save_config()
    print(f"Selected convert: {convert_mode}")


# download functions
def run_tidal_dl(link, download_dir, text_widget):
    global current_process, quality_mode, is_downloading
    print("quality_mode: " + quality_mode)

    if is_downloading:
        current_process = subprocess.Popen(
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
            preexec_fn=os.setsid  # Setzt den Prozess in eine eigene Prozessgruppe
        )

        def update_text_widget(stream):
            for line in iter(stream.readline, ""):
                text_widget.insert(tk.END, line)
                text_widget.see(tk.END)  # Scroll to the end of the Text widget
            stream.close()

        threading.Thread(target=update_text_widget, args=(current_process.stdout,)).start()
        threading.Thread(target=update_text_widget, args=(current_process.stderr,)).start()

        current_process.wait()
        text_widget.insert(tk.END, "\nDownload completed.\n")
        text_widget.see(tk.END)
        is_downloading = False


def download(playlists_data, text_widget):
    def download_thread():
        global is_downloading
        is_downloading = True

        music_directory = get_config_par("music_directory")

        for category_name, category_playlists in playlists_data.items():
            for link_name, link in category_playlists.items():
                download_dir = f"{music_directory}/{category_name}/{link_name}"
                run_tidal_dl(link, download_dir, text_widget)

    threading.Thread(target=download_thread).start()


def stop_tidal_dl(text_widget):
    global current_process, is_downloading
    if current_process is not None:
        # Beende die gesamte Prozessgruppe
        os.killpg(os.getpgid(current_process.pid), signal.SIGTERM)
        current_process = None
        is_downloading = False
        text_widget.insert(tk.END, "\nDownload aborted.\n")
        text_widget.see(tk.END)

# tree functions
def tree_find_item_by_name(tree, name):
    # Diese Funktion durchsucht den Treeview nach einem Element mit dem gegebenen Namen.
    for item in tree.get_children():
        if tree.item(item, "text") == name:
            return item
    return None


def tree_create_folder(tree, textentry_folder, playlists_data, progress_display):
    folder_name = textentry_folder.get()

    if not folder_name:
        print_progress_display(progress_display, "Give your folder a nice name!", "red")
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
        existing_folder_id = tree_find_item_by_name(tree, folder_name)
        if existing_folder_id:
            return existing_folder_id
        else:
            return 0


def tree_create_playlist(
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
        selected_folder_id = tree_create_folder(
            tree, textentry_folder_obj, playlists_data, progress_display
        )
    elif tree_has_item and not textentry_folder_has_item:
        selected_folder_name = tree_folder_name
        selected_folder_id = tree_folder_id
    elif tree_has_item and textentry_folder_has_item:
        selected_folder_name = textentry_folder_name
        selected_folder_id = tree_create_folder(
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
                    progress_display,
                    "Playlists already present in this folder",
                    "yellow",
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


def tree_update_folder(tree, textentry_folder, playlists_data, progress_display):
    # Holen des ausgewählten Elements im Treeview
    selected_item = tree.focus()  # Holt die ID des ausgewählten Elements

    if not selected_item:
        print_progress_display(
            progress_display, "Please select a folder to update!", "red"
        )
        return

    # Holt den aktuellen Namen des ausgewählten Elements (Ordners)
    current_folder_name = tree.item(selected_item, "text")

    # Den neuen Ordnernamen vom Eingabefeld bekommen
    new_folder_name = textentry_folder.get()

    if not new_folder_name:
        print_progress_display(
            progress_display, "Please enter a new folder name!", "red"
        )
        return

    # Überprüfen, ob der aktuelle Name des Ordners in den playlists_data existiert
    if current_folder_name in playlists_data:
        # Prüfen, ob der neue Name bereits in playlists_data existiert
        if new_folder_name in playlists_data:
            print_progress_display(
                progress_display, "Folder name already exists!", "red"
            )
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
        print_progress_display(
            progress_display, "Selected item is not a folder!", "red"
        )


def tree_update_playlist(
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
        print_progress_display(
            progress_display, "Please select a playlist to update!", "red"
        )
        return

    # Holt den aktuellen Namen und URL der ausgewählten Playlist
    current_playlist_name = tree.item(selected_item, "text")

    # Den neuen Ordnernamen, Playlistnamen und die neue URL aus den Eingabefeldern holen
    new_folder_name = textentry_folder.get()
    new_playlist_name = textentry_playlist.get()
    new_playlist_url = textentry_url.get()

    if not new_playlist_name:
        print_progress_display(
            progress_display, "Please enter a new playlist name!", "red"
        )
        return
    if not new_playlist_url:
        print_progress_display(
            progress_display, "Please enter a new playlist URL!", "red"
        )
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
            playlists_data[new_folder_name][new_playlist_name] = playlists_data[
                current_folder_name
            ].pop(current_playlist_name)
            save_playlists(playlists_data)

            tree.delete(selected_item)
            new_item_id = tree.insert(new_folder_id, "end", text=new_playlist_name)
            print_progress_display(
                progress_display,
                f'Playlist "{current_playlist_name}" moved to folder "{new_folder_name}".',
                "green",
            )

        else:
            print_progress_display(
                progress_display, "New folder does not exist!", "red"
            )
            return
    else:
        # Ordner bleibt gleich, nur Name oder URL werden geändert
        if (
            current_folder_name
            and current_playlist_name in playlists_data[current_folder_name]
        ):
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


def tree_update_item(
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
        print_progress_display(progress_display, "No item is selected!", "red")
        return

    if not tree.parent(tree_selected_item_id):
        tree_update_folder(tree, textentry_folder, playlists_data, progress_display)
    else:
        tree_update_playlist(
            tree,
            textentry_folder,
            textentry_playlist,
            textentry_url,
            playlists_data,
            progress_display,
        )

    return


def tree_remove_item(tree, playlists_data):
    # TODO: Add error handling if nothing is selected

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
