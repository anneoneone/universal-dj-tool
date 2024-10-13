import ttkbootstrap as ttk
from ttkbootstrap.constants import W


class LeftFrame(ttk.Frame):
    """Manages the left frame containing TIDAL playlists."""

    def __init__(self, parent, tidal_api, on_playlist_select_callback):
        super().__init__(parent)
        self.parent = parent
        self.tidal_api = tidal_api
        self.on_playlist_select_callback = on_playlist_select_callback
        self._initialize_left_frame()

    def _initialize_left_frame(self):
        """Initializes the left frame with a Treeview for """
        """playlists and last modified date."""
        # Label and Treeview for the left side
        item_list_label = ttk.Label(
            self, text="TIDAL Playlists", font=("Helvetica", 12)
        )
        item_list_label.pack(pady=5)

        # Treeview with two columns: Name and Last Modified
        self._playlist_treeview = ttk.Treeview(
            self, columns=("name", "last_modified"), show="headings"
        )
        self._playlist_treeview.heading(
            "name",
            text="TIDAL Playlist",
            anchor="w",
            command=lambda: self.parent.sort_treeview_column(
                self._playlist_treeview, "name", False
            ),
        )
        self._playlist_treeview.heading(
            "last_modified",
            text="Last Modified",
            anchor="w",
            command=lambda: self.parent.sort_treeview_column(
                self._playlist_treeview, "last_modified", False
            ),
        )

        # Set column alignment and width
        self._playlist_treeview.column("name", anchor=W, width=150)  # type: ignore
        self._playlist_treeview.column("last_modified", anchor=W, width=50)

        # Pack the Treeview
        self._playlist_treeview.pack(fill="both", expand=True)

        # Display TIDAL playlists
        self.tidal_api.display_user_playlists(self._playlist_treeview)

        # Add event handler for selection
        self._playlist_treeview.bind("<<TreeviewSelect>>", self.on_playlist_select)

    def on_playlist_select(self, event):
        """Handles the selection of a playlist in the Treeview."""
        selected_item = self._playlist_treeview.selection()
        if selected_item:
            item = self._playlist_treeview.item(selected_item)
            playlist_name = item["values"][0]
            selected_playlist = next(
                (pl for pl in self.tidal_api.playlists if pl.name == playlist_name),
                None,
            )
            if selected_playlist:
                self.on_playlist_select_callback(selected_playlist)

    def get_selected_playlist(self):
        """Returns the currently selected playlist."""
        selected_item = self._playlist_treeview.selection()
        if selected_item:
            item = self._playlist_treeview.item(selected_item)
            playlist_name = item["values"][0]
            selected_playlist = next(
                (pl for pl in self.tidal_api.playlists if pl.name == playlist_name),
                None,
            )
            return selected_playlist
        return None
