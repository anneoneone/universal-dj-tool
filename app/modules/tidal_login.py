import json
import threading
from modules.RekordboxXMLGenerator import RekordboxXMLGenerator
import tidalapi
from datetime import datetime


class TidalLogin:
    def __init__(self, token_file='tidal_token.json', progress_display=None):
        self.token_file = token_file
        self.session = tidalapi.Session()
        self.progress_display = progress_display
        self.log_message("hello test")

    def log_message(self, message, tag="white"):
        """Helper function to print messages in progress_display."""
        if self.progress_display:
            self.progress_display.insert("end", f"{message}\n", tag)
            self.progress_display.see("end")
        else:
            print(message)

    def login(self):
        """Starts the OAuth login process in a separate thread."""
        self.log_message("Starting OAuth login process for Tidal...", tag="yellow")
        thread = threading.Thread(target=self._login_thread)
        thread.daemon = True
        thread.start()

    def _login_thread(self):
        """The actual OAuth login process, to be run in a separate thread."""
        try:
            login, future = self.session.login_oauth()

            # Display the URL where the user should log in
            self.log_message(f"Please open the following URL to complete the login: {login.verification_uri_complete}", tag="blue")

            # Wait for the user to complete the login
            future.result()

            if self.session.check_login():
                self.log_message("Successfully connected to Tidal!", tag="green")
                self.save_token()
            else:
                self.log_message("Login failed.", tag="red")

        except Exception as e:
            self.log_message(f"An error occurred during the login process: {str(e)}", tag="red")

    def save_token(self):
        """Saves the current token data to a file."""
        token_data = {
            "access_token": self.session.access_token,
            "refresh_token": self.session.refresh_token,
            "token_type": self.session.token_type,
            "expiry_time": self.session.expiry_time.isoformat() if self.session.expiry_time else None,
        }

        try:
            with open(self.token_file, 'w') as token_file:
                json.dump(token_data, token_file)
            self.log_message("Token saved successfully.", tag="green")
        except Exception as e:
            self.log_message(f"Failed to save token: {str(e)}", tag="red")

    def load_token(self):
        """Loads the saved token from the file."""
        try:
            with open(self.token_file, 'r') as token_file:
                token_data = json.load(token_file)

            # Load token data into the session
            self.session.access_token = token_data["access_token"]
            self.session.refresh_token = token_data["refresh_token"]
            self.session.token_type = token_data["token_type"]
            self.session.expiry_time = datetime.fromisoformat(token_data["expiry_time"]) if token_data["expiry_time"] else None

            if self.session.load_oauth_session(
                self.session.token_type,
                self.session.access_token,
                self.session.refresh_token,
                self.session.expiry_time,
            ):
                # if self.session.check_login():
                self.log_message("Successfully connected with saved token!", tag="green")
            else:
                self.log_message("Error loading token", tag="red")
        except FileNotFoundError:
            self.log_message("No saved token file found. Please log in first.", tag="red")
        except Exception as e:
            self.log_message(f"Error loading token: {str(e)}", tag="red")

    def get_user_id(self):
        user = self.session.user
        user_id = user.id
        return user_id
    
    def display_user_playlists(self):
        """Displays all playlists of the currently logged-in user."""
        try:
            playlists = self.session.user.playlists()
            if playlists:
                self.log_message("User's Playlists:", tag="green")
                for playlist in playlists:
                    self.log_message(f" - {playlist.name} (ID: {playlist.id})", tag="white")
            else:
                self.log_message("No playlists found for this user.", tag="yellow")
        except Exception as e:
            self.log_message(f"Failed to retrieve playlists: {str(e)}", tag="red")

    def display_playlist_tracks(self, playlist):
        """Displays all tracks in a given playlist."""
        try:
            tracks = playlist.tracks()
            if tracks:
                self.log_message(f"Tracks in playlist '{playlist.name}':", tag="blue")
                for track in tracks:
                    self.log_message(f"   - {track.name} by {track.artist.name}", tag="white")
            else:
                self.log_message(f"No tracks found in playlist '{playlist.name}'.", tag="yellow")
        except Exception as e:
            self.log_message(f"Failed to retrieve tracks for playlist '{playlist.name}': {str(e)}", tag="red")

    def display_user_playlists_and_tracks(self):
        """Displays all playlists of the currently logged-in user and all their tracks."""
        try:
            playlists = self.session.user.playlists()
            if playlists:
                self.log_message("User's Playlists:", tag="green")
                for playlist in playlists:
                    self.log_message(f" - {playlist.name} (ID: {playlist.id})", tag="white")
                    self.display_playlist_tracks(playlist)  # Display tracks of each playlist
            else:
                self.log_message("No playlists found for this user.", tag="yellow")
        except Exception as e:
            self.log_message(f"Failed to retrieve playlists: {str(e)}", tag="red")

    def generate_rekordbox_files(self):
        """Generates Rekordbox-compatible XML file with playlists and tracks."""
        try:
            playlists = self.session.user.playlists()
            if not playlists:
                self.log_message("No playlists available to generate XML.", tag="red")
                return

            # Creating an instance of the RekordboxXMLGenerator class
            xml_generator = RekordboxXMLGenerator()
            
            # Calling the generate_xml() method of RekordboxXMLGenerator
            xml_generator.generate_xml(playlists)

            # Creating m3u playlist files
            xml_generator.generate_m3u(playlists)
            self.log_message("M3U files generated successfully for each playlist.", tag="green")
            
            self.log_message("Rekordbox XML generated successfully: rekordbox_playlists.xml", tag="green")

        except Exception as e:
            self.log_message(f"Failed to generate Rekordbox XML: {str(e)}", tag="red")


    # def refresh_token(self):
    #     """Refreshes the token if the saved one has expired."""
    #     if self.session.refresh_oauth_session():
    #         self.log_message("Token successfully refreshed.", tag="green")
    #         self.save_token()
    #     else:
    #         self.log_message("Token refresh failed. Please log in again.", tag="red")
