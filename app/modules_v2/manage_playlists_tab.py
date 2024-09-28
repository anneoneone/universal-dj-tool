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
        """Initialisiert das linke Frame mit der Listbox für Items."""
        self._left_frame = ttk.Frame(self)
        self._left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Label und Listbox für die linke Seite
        item_list_label = ttk.Label(self._left_frame, text="Available Playlists", font=("Helvetica", 12))
        item_list_label.pack(pady=5)

        self._item_listbox = Listbox(self._left_frame)
        self._item_listbox.pack(fill="both", expand=True)

        # Playlists von Tidal anzeigen, wenn der left_frame geladen wird
        self.tidal_login.display_user_playlists(self._item_listbox)

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

        self._music_table = ttk.Treeview(self._music_table_frame, columns=("title", "artist", "length"), show="headings")
        self._music_table.heading("title", text="Titel")
        self._music_table.heading("artist", text="Interpret")
        self._music_table.heading("length", text="Länge")

        # Set column widths
        self._music_table.column("title", anchor=W, width=200)
        self._music_table.column("artist", anchor=W, width=150)
        self._music_table.column("length", anchor=CENTER, width=80)

        self._music_table.pack(fill="both", expand=True)

    # Öffentliche Methoden für die Interaktion mit der UI

    def add_item_to_list(self, item):
        """Fügt ein Item zur linken Listbox hinzu."""
        self._item_listbox.insert("end", item)

    def add_playlist_to_tree(self, playlist_name):
        """Fügt eine Playlist zur Baumstruktur hinzu."""
        self._playlist_tree.insert("", "end", text=playlist_name)

    def add_music_to_table(self, title, artist, length):
        """Fügt eine Musikzeile zur Tabelle hinzu."""
        self._music_table.insert("", "end", values=(title, artist, length))
