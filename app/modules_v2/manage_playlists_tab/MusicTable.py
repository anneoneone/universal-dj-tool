import ttkbootstrap as ttk
from ttkbootstrap.constants import W
from modules_v2.utils import log_message


class MusicTable(ttk.Frame):
    """Manages the bottom table displaying music files."""

    def __init__(self, parent, tidal_api):
        super().__init__(parent)
        self.parent = parent
        self.tidal_api = tidal_api
        self._initialize_music_table()

    def _initialize_music_table(self):
        """Initializes the bottom table to display music files."""
        # Extended columns for detailed track information
        self._music_table = ttk.Treeview(
            self,
            columns=(
                "title",
                "artist",
                "length",
                "album",
                "release_year",
                "popularity",
            ),
            show="headings",
        )

        # Style headers to align to the left
        style = ttk.Style()
        style.configure("Treeview.Heading", anchor="w")

        # Define column headings and ensure left alignment
        self._music_table.heading(
            "title",
            text="Title",
            anchor="w",
            command=lambda: self.parent.sort_treeview_column(
                self._music_table, "title", False
            ),
        )
        self._music_table.heading(
            "artist",
            text="Artist",
            anchor="w",
            command=lambda: self.parent.sort_treeview_column(
                self._music_table, "artist", False
            ),
        )
        self._music_table.heading(
            "length",
            text="Duration",
            anchor="w",
            command=lambda: self.parent.sort_treeview_column(
                self._music_table, "length", False
            ),
        )
        self._music_table.heading(
            "album",
            text="Album",
            anchor="w",
            command=lambda: self.parent.sort_treeview_column(
                self._music_table, "album", False
            ),
        )
        self._music_table.heading(
            "release_year",
            text="Release",
            anchor="w",
            command=lambda: self.parent.sort_treeview_column(
                self._music_table, "release_year", False
            ),
        )
        self._music_table.heading(
            "popularity",
            text="Popularity",
            anchor="w",
            command=lambda: self.parent.sort_treeview_column(
                self._music_table, "popularity", False
            ),
        )

        # Set column alignment
        self._music_table.column("title", anchor=W, width=220)
        self._music_table.column("artist", anchor=W, width=150)
        self._music_table.column("length", anchor=W, width=80)
        self._music_table.column("album", anchor=W, width=150)
        self._music_table.column("release_year", anchor=W, width=50)
        self._music_table.column("popularity", anchor=W, width=70)

        # Pack the Treeview
        self._music_table.pack(fill="both", expand=True)

    def display_tracks(self, selected_playlist):
        """Displays the tracks from the selected playlist in the table."""
        # Clear existing entries
        for item in self._music_table.get_children():
            self._music_table.delete(item)

        # Fetch tracks with prepared data
        prepared_tracks = self.tidal_api.get_playlist_tracks(selected_playlist)
        if prepared_tracks:
            for track_data in prepared_tracks:
                # Add track to the music table
                self._music_table.insert(
                    "",
                    "end",
                    values=(
                        track_data["title"],
                        track_data["artist"],
                        track_data["duration"],
                        track_data["album"],
                        track_data["release_year"],
                        track_data["popularity"],
                    ),
                )
        else:
            log_message(
                f"No tracks to display for playlist '{selected_playlist.name}'.",
                tag="yellow",
            )
