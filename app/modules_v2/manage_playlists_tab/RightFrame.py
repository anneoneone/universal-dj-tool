from tkinter import W
import xml.etree.ElementTree as ET
import ttkbootstrap as ttk


class RightFrame(ttk.Frame):
    """Manages the right frame containing Rekordbox playlists."""

    def __init__(self, parent, rekordbox_xml_path):
        super().__init__(parent)
        self.parent = parent
        self.rekordbox_xml_path = rekordbox_xml_path
        self._initialize_right_frame()

    def _initialize_right_frame(self):
        """Initializes the right frame with the Rekordbox playlists Treeview."""
        # Label and Treeview for the right side
        tree_label = ttk.Label(self, text="Rekordbox Playlists", font=("Helvetica", 12))
        tree_label.pack(pady=5)

        # Treeview for Rekordbox Playlists
        self._rekordbox_treeview = ttk.Treeview(self)
        self._rekordbox_treeview.pack(fill="both", expand=True)

        self._rekordbox_treeview.heading("#0", text="Playlists/Folders", anchor=W)

        # Load Rekordbox Playlists
        self.load_rekordbox_playlists()

    def load_rekordbox_playlists(self):
        """Loads playlists from the Rekordbox XML file and displays them in the Treeview."""
        try:
            tree = ET.parse(self.rekordbox_xml_path)
            root = tree.getroot()

            # Only process the PLAYLISTS section
            playlists_root = root.find(".//PLAYLISTS")
            if playlists_root is not None:
                for node in playlists_root.findall(".//NODE"):
                    if node.attrib.get("Type") == "0" and node.attrib.get("Name") != "ROOT":
                        # Add folder nodes
                        folder_id = self._rekordbox_treeview.insert("", "end", text=node.attrib.get("Name"), open=True)
                        # Add playlists within the folder
                        for child_node in node.findall(".//NODE"):
                            if child_node.attrib.get("Type") == "1":
                                self._rekordbox_treeview.insert(folder_id, "end", text=child_node.attrib.get("Name"))
        except ET.ParseError as e:
            print(f"Error parsing Rekordbox XML: {e}")

    def get_selected_item(self):
        """Returns the currently selected item."""
        selected_item = self._rekordbox_treeview.selection()
        if selected_item:
            return selected_item[0]
        return None

    def get_item_name(self, item_id):
        """Returns the name of the item given its ID."""
        item = self._rekordbox_treeview.item(item_id)
        return item['text']

    def add_playlist_to_folder(self, folder_item_id, playlist_name):
        """Adds a playlist to a folder in the Treeview."""
        self._rekordbox_treeview.insert(folder_item_id, "end", text=playlist_name)

    def add_playlist_to_root(self, playlist_name):
        """Adds a playlist under the ROOT node in the Treeview."""
        root_item_id = self.get_root_item_id()
        if root_item_id:
            self._rekordbox_treeview.insert(root_item_id, "end", text=playlist_name)

    def get_root_item_id(self):
        """Returns the ID of the ROOT item."""
        for item_id in self._rekordbox_treeview.get_children():
            item = self._rekordbox_treeview.item(item_id)
            if item['text'] == "ROOT":
                return item_id
        return None

    def delete_item(self, item_id):
        """Deletes an item from the Treeview."""
        self._rekordbox_treeview.delete(item_id)
