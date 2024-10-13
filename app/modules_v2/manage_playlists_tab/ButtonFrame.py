import ttkbootstrap as ttk


class ButtonFrame(ttk.Frame):
    """Manages the middle frame containing action buttons."""

    def __init__(self, parent, add_callback, remove_callback, create_folder_callback):
        super().__init__(parent)
        self.parent = parent
        self.add_callback = add_callback
        self.remove_callback = remove_callback
        self.create_folder_callback = create_folder_callback
        self._initialize_button_frame()

    def _initialize_button_frame(self):
        """Initializes the middle frame with vertically arranged buttons."""
        # Configure the frame with 9 equally sized rows
        for i in range(9):
            self.rowconfigure(i, weight=1)

        # Arrange buttons in rows 4, 5, and 6
        self._add_button = ttk.Button(
            self,
            text="Add to Rekordbox Playlists",
            bootstyle="success",
            command=self.add_callback,
        )
        self._add_button.grid(row=3, column=0, pady=5, sticky="ew")

        self._remove_button = ttk.Button(
            self,
            text="Remove from Rekordbox Playlist",
            bootstyle="danger",
            command=self.remove_callback,
        )
        self._remove_button.grid(row=4, column=0, pady=5, sticky="ew")

        self._create_folder_button = ttk.Button(
            self,
            text="Create Folder",
            bootstyle="info",
            command=self.create_folder_callback,
        )
        self._create_folder_button.grid(row=5, column=0, pady=5, sticky="ew")
