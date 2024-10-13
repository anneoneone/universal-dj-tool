import xml.etree.ElementTree as ET
import ttkbootstrap as ttk
from modules_v2.constants import rekordbox_xml_path
from modules_v2.utils import log_message

from modules_v2.manage_playlists_tab.LeftFrame import LeftFrame
from modules_v2.manage_playlists_tab.RightFrame import RightFrame
from modules_v2.manage_playlists_tab.ButtonFrame import ButtonFrame
from modules_v2.manage_playlists_tab.MusicTable import MusicTable


class ManagePlaylistsTab(ttk.Frame):
    """Main class that orchestrates all components."""

    def __init__(self, parent, tidal_api):
        super().__init__(parent)
        self.parent = parent
        self.tidal_api = tidal_api
        self.rekordbox_xml_path = rekordbox_xml_path

        # Initialize main layout
        self._initialize_main_layout()

        # Create frames
        self.left_frame = LeftFrame(self, tidal_api, self.on_playlist_selected)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.right_frame = RightFrame(self, self.rekordbox_xml_path)
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        self.button_frame = ButtonFrame(
            self,
            self._add_to_rekordbox,
            self._remove_from_rekordbox,
            self._create_folder,
        )
        self.button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.music_table = MusicTable(self, self.tidal_api)
        self.music_table.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10
        )

        # Ensure the frame is packed
        self.pack(fill="both", expand=True)
        self.update()

    def _initialize_main_layout(self):
        """Initializes the main layout with a grid system for frames."""
        self.columnconfigure(0, weight=1)  # Left column (left frame)
        self.columnconfigure(1, weight=0)  # Middle column (buttons)
        self.columnconfigure(2, weight=1)  # Right column (right frame)

        self.rowconfigure(0, weight=1)  # Top row for frames
        self.rowconfigure(1, weight=1)  # Bottom row for the music table

    def on_playlist_selected(self, selected_playlist):
        """Handles the event when a playlist is selected."""
        self.music_table.display_tracks(selected_playlist)

    def _add_to_rekordbox(self):
        """Adds the selected playlist from the left frame to the Rekordbox XML."""
        try:
            # Get the selected playlist from the left frame
            selected_playlist = self.left_frame.get_selected_playlist()
            if not selected_playlist:
                log_message("No playlist selected in left frame.", tag="red")
                return

            # Get the selected item from the right frame
            selected_right_item = self.right_frame.get_selected_item()

            # Load the Rekordbox XML
            tree = ET.parse(self.rekordbox_xml_path)
            root = tree.getroot()

            # Find the PLAYLISTS section
            playlists_root = root.find(".//PLAYLISTS")
            if playlists_root is None:
                log_message("PLAYLISTS section not found in Rekordbox XML.", tag="red")
                return

            # Create new XML node for the playlist
            new_playlist_node = ET.Element("NODE")
            new_playlist_node.set("Name", selected_playlist.name)
            new_playlist_node.set("Type", "1")  # Type=1 means a normal playlist

            # If a target folder is selected in the right frame
            if selected_right_item:
                folder_name = self.right_frame.get_item_name(selected_right_item)

                # Find the folder node in the XML
                target_folder_node = next(
                    (
                        node
                        for node in playlists_root.findall(".//NODE")
                        if node.attrib.get("Name") == folder_name
                        and node.attrib.get("Type") == "0"
                    ),
                    None,
                )
                if target_folder_node:
                    # Add the playlist as a child of the selected folder
                    target_folder_node.append(new_playlist_node)
                else:
                    log_message(
                        "Selected folder not found in Rekordbox XML.", tag="red"
                    )
                    return
            else:
                # If no folder selected, find the ROOT node
                root_node = next(
                    (
                        node
                        for node in playlists_root.findall(".//NODE")
                        if node.attrib.get("Name") == "ROOT"
                        and node.attrib.get("Type") == "0"
                    ),
                    None,
                )
                if root_node is not None:
                    # Add the playlist as a child of the ROOT node
                    root_node.append(new_playlist_node)
                else:
                    log_message("ROOT node not found in Rekordbox XML.", tag="red")
                    return

            # Format the XML
            self.indent_xml(root)

            # Write the updated XML file
            tree.write(self.rekordbox_xml_path, encoding="utf-8", xml_declaration=True)
            log_message(
                f"Playlist '{selected_playlist.name}' added to Rekordbox XML.",
                tag="green",
            )

            # Update the right frame Treeview
            if selected_right_item:
                self.right_frame.add_playlist_to_folder(
                    selected_right_item, selected_playlist.name
                )
            else:
                self.right_frame.add_playlist_to_root(selected_playlist.name)

        except ET.ParseError as e:
            log_message(f"Error parsing Rekordbox XML: {str(e)}", tag="red")
        except Exception as e:
            log_message(f"An unexpected error occurred: {str(e)}", tag="red")

    def _remove_from_rekordbox(self):
        """Removes the selected item from the right frame """
        """from the Rekordbox XML and Treeview."""
        try:
            # Get the selected item from the right frame
            selected_right_item = self.right_frame.get_selected_item()
            if not selected_right_item:
                log_message("No item selected in right frame.", tag="red")
                return

            # Get the item name
            item_name = self.right_frame.get_item_name(selected_right_item)

            # Load the Rekordbox XML
            tree = ET.parse(self.rekordbox_xml_path)
            root = tree.getroot()

            # Find the PLAYLISTS section
            playlists_root = root.find(".//PLAYLISTS")
            if playlists_root is None:
                log_message("PLAYLISTS section not found in Rekordbox XML.", tag="red")
                return

            # Function to find and remove the node
            def find_and_remove_node(parent_node, node_name):
                for node in list(parent_node):
                    if node.attrib.get("Name") == node_name:
                        parent_node.remove(node)
                        return True
                    # Recursively search in child nodes
                    removed = find_and_remove_node(node, node_name)
                    if removed:
                        return True
                return False

            # Attempt to find and remove the node
            removed = find_and_remove_node(playlists_root, item_name)
            if not removed:
                log_message(
                    f"Item '{item_name}' not found in Rekordbox XML.", tag="red"
                )
                return

            # Write the updated XML
            self.indent_xml(root)
            tree.write(self.rekordbox_xml_path, encoding="utf-8", xml_declaration=True)
            log_message(f"Item '{item_name}' removed from Rekordbox XML.", tag="green")

            # Remove the item from the right frame Treeview
            self.right_frame.delete_item(selected_right_item)

        except ET.ParseError as e:
            log_message(f"Error parsing Rekordbox XML: {str(e)}", tag="red")
        except Exception as e:
            log_message(f"An unexpected error occurred: {str(e)}", tag="red")

    def _create_folder(self):
        """Handles the creation of a new folder in the Rekordbox XML and Treeview."""
        # Implement the logic to create a new folder
        pass

    def indent_xml(self, elem, level=0):
        """Adds indentation and line breaks to the XML element to format the output."""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for child in elem:
                self.indent_xml(child, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def sort_treeview_column(self, treeview, col, reverse):
        """Sorts the columns of the Treeview, taking data types into account."""
        # Extract data from the column
        data = []
        for k in treeview.get_children(""):
            value = treeview.set(k, col)

            # Try to convert the value to an integer or float if it's numeric
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass  # Value remains a string if not numeric

            data.append((value, k))

        # Sort the data
        data.sort(reverse=reverse)

        # Reorder in the Treeview
        for index, (_, k) in enumerate(data):
            treeview.move(k, "", index)

        # Reverse sort direction for next sort
        treeview.heading(
            col, command=lambda: self.sort_treeview_column(treeview, col, not reverse)
        )
