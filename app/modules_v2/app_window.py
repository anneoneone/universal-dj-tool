
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from modules_v2.manage_playlists_tab import ManagePlaylistsTab
from modules_v2.run_dj_tool_tab import RunDJToolTab

class AppWindow(ttk.Frame):
    def __init__(self, parent, tidal_login):
        super().__init__(parent)
        self.parent = parent
        self.tidal_login = tidal_login  # Referenz zur TidalLogin-Instanz

        self.pack(fill="both", expand=True)

        # Notebook erstellen
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # "Manage Playlists" Tab erstellen und hinzufügen
        self.manage_playlists_tab = ManagePlaylistsTab(self.notebook, tidal_login)
        self.notebook.add(self.manage_playlists_tab, text="Manage Playlists")

        # "Run DJ Tool" Tab erstellen und hinzufügen
        self.run_dj_tool_tab = RunDJToolTab(self.notebook)
        self.notebook.add(self.run_dj_tool_tab, text="Run DJ Tool")
