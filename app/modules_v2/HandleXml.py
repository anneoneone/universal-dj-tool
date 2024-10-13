import xml.etree.ElementTree as ET

class HandleXml:
    def __init__(self, xml_path):
        """Initialisiert die XML-Verarbeitungsklasse mit dem Pfad zur XML-Datei."""
        self.xml_path = xml_path

    def load_xml(self):
        """Lädt die XML-Datei und gibt den Baum und das Wurzelelement zurück."""
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        return tree, root

    def create_playlist_node(self, playlist_name):
        """Erstellt einen neuen XML-Knoten für eine Playlist."""
        new_playlist_node = ET.Element("NODE")
        new_playlist_node.set("Name", playlist_name)
        new_playlist_node.set("Type", "1")
        return new_playlist_node

    def add_playlist_to_folder(self, parent_node, folder_name, new_playlist_node):
        """Fügt die Playlist zu einem vorhandenen Ordner hinzu."""
        target_folder_node = next((node for node in parent_node.findall(".//NODE") if node.attrib.get("Name") == folder_name and node.attrib.get("Type") == "0"), None)
        if target_folder_node:
            target_folder_node.append(new_playlist_node)
            return True
        return False

    def add_playlist_to_root(self, parent_node, new_playlist_node):
        """Fügt die Playlist zum ROOT-Knoten hinzu."""
        root_node = next((node for node in parent_node.findall(".//NODE") if node.attrib.get("Name") == "ROOT" and node.attrib.get("Type") == "0"), None)
        if root_node is not None:
            root_node.append(new_playlist_node)
            return True
        return False

    def find_and_remove_node(self, parent_node, node_name):
        """Finde und entferne den Knoten mit dem angegebenen Namen."""
        for node in list(parent_node):
            if node.attrib.get("Name") == node_name:
                parent_node.remove(node)
                return True
            removed = self.find_and_remove_node(node, node_name)
            if removed:
                return True
        return False

    def save_xml(self, tree, root):
        """Speichert die XML-Datei nach der Formatierung."""
        self.indent_xml(root)
        tree.write(self.xml_path, encoding='utf-8', xml_declaration=True)

    def indent_xml(self, elem, level=0):
        """Fügt Einrückungen und Zeilenumbrüche zum XML-Element hinzu, um die Ausgabe zu formatieren."""
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
