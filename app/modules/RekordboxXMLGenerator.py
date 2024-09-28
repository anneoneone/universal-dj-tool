# rekordbox_xml_generator.py

import xml.etree.ElementTree as ET


class RekordboxXMLGenerator:
    def __init__(self):
        pass

    def generate_xml(self, playlists, output_file="rekordbox_playlists.xml"):
        """Generates Rekordbox-compatible XML from given playlists."""
        try:
            root = ET.Element("DJ_PLAYLISTS")
            root.set("Version", "1.0.0")

            # COLLECTION part
            collection = ET.SubElement(root, "COLLECTION")
            track_ids = {}  # To keep track of all added track IDs

            # PLAYLISTS part
            playlists_element = ET.SubElement(root, "PLAYLISTS")

            for playlist in playlists:
                playlist_element = ET.SubElement(playlists_element, "NODE", Name=playlist.name, Type="1")

                tracks = playlist.tracks()
                if tracks:
                    for index, track in enumerate(tracks, start=1):
                        track_id = str(track.id)
                        if track_id not in track_ids:
                            track_element = ET.SubElement(collection, "TRACK",
                                TrackID=track_id,
                                Name=track.name,
                                Artist=track.artist.name,
                                Album=track.album.name,
                                Genre="",  # Optional: Genre
                                TotalTime=str(track.duration // 1000),
                                Location="",
                                TrackNumber=str(index)
                            )
                            track_ids[track_id] = track_element

                        ET.SubElement(playlist_element, "TRACK", Key=track_id)

            # Write to an XML file
            tree = ET.ElementTree(root)
            tree.write(output_file, encoding="utf-8", xml_declaration=True)

        except Exception as e:
            raise Exception(f"Error while generating Rekordbox XML: {str(e)}")

    def generate_m3u(self, playlists):
        """Generates M3U files for each playlist."""
        try:
            for playlist in playlists:
                filename = f"{playlist.name}.m3u"
                with open(filename, "w", encoding="utf-8") as m3u_file:
                    m3u_file.write("#EXTM3U\n")
                    tracks = playlist.tracks()
                    if tracks:
                        for track in tracks:
                            # Writing track details
                            m3u_file.write(f"#EXTINF:{track.duration // 1000},{track.artist.name} - {track.name}\n")
                            m3u_file.write(f"{track.name}\n")
                
                print(f"Generated M3U playlist: {filename}")

        except Exception as e:
            raise Exception(f"Error while generating M3U files: {str(e)}")
