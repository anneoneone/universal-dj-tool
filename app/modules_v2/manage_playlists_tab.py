import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Listbox
from modules_v2.tidal_login import TidalLogin

class ManagePlaylistsTab(ttk.Frame):
    def __init__(self, parent, tidal_login):
        super().__init__(parent)
        self.parent = parent
        self.tidal_login = tidal_login  # Instanz von TidalLogin übergeben

        # Initialisiere die GUI-Komponenten
        self._initialize_main_layout()
        self._initialize_left_frame()
        self._initialize_button_frame()
        self._initialize_right_frame()
        self._initialize_music_table()

        # Sicherstellen, dass das Frame gepackt wird
        self.pack(fill="both", expand=True)
        self.update()

    def _initialize_main_layout(self):
        """Initialisiert das Hauptlayout mit einem Grid-System für linkes, mittleres und rechtes Frame."""
        self.columnconfigure(0, weight=1)  # Linke Spalte (linkes Frame)
        self.columnconfigure(1, weight=0)  # Mittlere Spalte (Buttons)
        self.columnconfigure(2, weight=1)  # Rechte Spalte (rechtes Frame)

        self.rowconfigure(0, weight=1)     # Obere Zeile für Frames
        self.rowconfigure(1, weight=1)     # Untere Zeile für die Musik-Tabelle

    def _initialize_left_frame(self):
        """Initialisiert das linke Frame mit einem Treeview für Playlists und deren letzte Bearbeitung."""
        self._left_frame = ttk.Frame(self)
        self._left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Label und Treeview für die linke Seite
        item_list_label = ttk.Label(self._left_frame, text="TIDAL Playlists", font=("Helvetica", 12))
        item_list_label.pack(pady=5)

        # Treeview mit zwei Spalten: Name und letzte Bearbeitung
        self._playlist_treeview = ttk.Treeview(self._left_frame, columns=("name", "last_modified"), show="headings")
        self._playlist_treeview.heading(
            "name",
            text="TIDAL Playlist",
            anchor="w",
            command=lambda: self.sort_treeview_column(
                self._playlist_treeview, "name", False
            ),
        )
        self._playlist_treeview.heading(
            "last_modified",
            text="Last Modified",
            anchor="w",
            command=lambda: self.sort_treeview_column(
                self._playlist_treeview, "last_modified", False
            ),
        )

        # Setze die Spaltenausrichtung und Breite
        self._playlist_treeview.column("name", anchor=W, width=150)
        self._playlist_treeview.column("last_modified", anchor=W, width=50)

        # Packe das Treeview in das Frame
        self._playlist_treeview.pack(fill="both", expand=True)

        # Playlists von Tidal anzeigen, wenn der left_frame geladen wird
        self.tidal_login.display_user_playlists(self._playlist_treeview)

        # Event-Handler hinzufügen für Treeview-Auswahl
        self._playlist_treeview.bind("<<TreeviewSelect>>", self.on_playlist_select)

    def _initialize_button_frame(self):
        """Initialisiert das mittlere Frame mit den vertikal angeordneten Buttons."""
        self._button_frame = ttk.Frame(self)
        self._button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Konfiguration des mittleren Frames in 9 gleich große Zeilen
        for i in range(9):
            self._button_frame.rowconfigure(i, weight=1)

        # Buttons in den Zeilen 4, 5 und 6 anordnen
        self._add_button = ttk.Button(self._button_frame, text="Add to Rekordbox Playlists", bootstyle="success")
        self._add_button.grid(row=3, column=0, pady=5, sticky="ew")

        self._remove_button = ttk.Button(self._button_frame, text="Remove from Rekordbox Playlist", bootstyle="danger")
        self._remove_button.grid(row=4, column=0, pady=5, sticky="ew")

        self._create_folder_button = ttk.Button(self._button_frame, text="Create Folder", bootstyle="info")
        self._create_folder_button.grid(row=5, column=0, pady=5, sticky="ew")

    def _initialize_right_frame(self):
        """Initialisiert das rechte Frame mit der Baumstruktur für Playlists."""
        self._right_frame = ttk.Frame(self)
        self._right_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # Label und Treeview für die rechte Seite
        tree_label = ttk.Label(self._right_frame, text="Rekordbox Playlists", font=("Helvetica", 12))
        tree_label.pack(pady=5)

        self._playlist_tree = ttk.Treeview(self._right_frame)
        self._playlist_tree.pack(fill="both", expand=True)

        self._playlist_tree.heading("#0", text="Playlists/Folders", anchor=W)

    def _initialize_music_table(self):
        """Initialisiert die untere Tabelle zur Darstellung der Musikdateien."""
        self._music_table_frame = ttk.Frame(self)
        self._music_table_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Erweiterte Spalten für detaillierte Track-Informationen
        self._music_table = ttk.Treeview(
            self._music_table_frame,
            columns=("title", "artist", "length", "album", "release_year", "popularity", "version"),
            show="headings"
        )

        # Stil für die Header linksbündig setzen
        style = ttk.Style()
        style.configure("Treeview.Heading", anchor="w")  # 'w' steht für 'west' (links)

        # Definiere die Spaltenüberschriften und stelle sicher, dass der Text linksbündig ist
        self._music_table.heading(
            "title",
            text="Title",
            anchor="w",
            command=lambda: self.sort_treeview_column(self._music_table, "title", False),
        )
        self._music_table.heading(
            "artist",
            text="Artist",
            anchor="w",
            command=lambda: self.sort_treeview_column(self._music_table, "artist", False),
        )
        self._music_table.heading(
            "length",
            text="Duration",
            anchor="w",
            command=lambda: self.sort_treeview_column(self._music_table, "length", False),
        )
        self._music_table.heading(
            "album",
            text="Album",
            anchor="w",
            command=lambda: self.sort_treeview_column(self._music_table, "album", False),
        )
        self._music_table.heading(
            "release_year",
            text="Release",
            anchor="w",
            command=lambda: self.sort_treeview_column(
                self._music_table, "release_year", False
            ),
        )
        self._music_table.heading(
            "popularity",
            text="Popularity",
            anchor="w",
            command=lambda: self.sort_treeview_column(
                self._music_table, "popularity", False
            ),
        )
        self._music_table.heading(
            "version",
            text="Version",
            anchor="w",
            command=lambda: self.sort_treeview_column(
                self._music_table, "version", False
            ),
        )

        # Setze die Ausrichtung der Spalten auf links
        self._music_table.column("title", anchor=W, width=220)
        self._music_table.column("artist", anchor=W, width=150)
        self._music_table.column("length", anchor=W, width=80)
        self._music_table.column("album", anchor=W, width=150)
        self._music_table.column("release_year", anchor=W, width=50)
        self._music_table.column("popularity", anchor=W, width=70)
        self._music_table.column("version", anchor=W, width=100)

        # Packe das Treeview in das Frame
        self._music_table.pack(fill="both", expand=True)

    def sort_treeview_column(self, treeview, col, reverse):
        """Sortiert die Spalten des Treeview, unter Berücksichtigung des Datentyps."""
        # Extrahiere die Daten aus der Spalte
        data = []
        for k in treeview.get_children(''):
            value = treeview.set(k, col)

            # Versuche den Wert in einen Integer oder Float zu konvertieren, falls es numerisch ist
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass  # Wert bleibt ein String, wenn er nicht numerisch ist

            data.append((value, k))

        # Sortiere die Daten
        data.sort(reverse=reverse)

        # Neu anordnen im Treeview
        for index, (_, k) in enumerate(data):
            treeview.move(k, '', index)

        # Sortierrichtung umkehren für die nächste Sortierung
        treeview.heading(col, command=lambda: self.sort_treeview_column(treeview, col, not reverse))

    def on_playlist_select(self, event):
        """Event-Handler, der ausgeführt wird, wenn eine Playlist im Treeview ausgewählt wird."""
        try:
            # Aktuelle Auswahl abrufen
            selected_item = self._playlist_treeview.selection()
            if selected_item:
                # Abrufen der Werte der ausgewählten Playlist
                item = self._playlist_treeview.item(selected_item)
                playlist_name = item['values'][0]  # Der Name der Playlist befindet sich in der ersten Spalte

                # Suche die entsprechende Playlist anhand des Namens
                selected_playlist = next((pl for pl in self.tidal_login.playlists if pl.name == playlist_name), None)

                if selected_playlist:
                    # Playlist-Tracks im music_table anzeigen
                    self.tidal_login.display_playlist_tracks(selected_playlist, self._music_table)
        except IndexError:
            pass  # Falls die Auswahl ungültig ist, wird nichts gemacht

    def add_item_to_list(self, item):
        """Fügt ein Item zur linken Listbox hinzu."""
        self._item_listbox.insert("end", item)

    def add_playlist_to_tree(self, playlist_name):
        """Fügt eine Playlist zur Baumstruktur hinzu."""
        self._playlist_tree.insert("", "end", text=playlist_name)

    def add_music_to_table(self, title, artist, length):
        """Fügt eine Musikzeile zur Tabelle hinzu."""
        self._music_table.insert("", "end", values=(title, artist, length))
