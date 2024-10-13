import json
import threading
import tidalapi
from datetime import datetime
from modules_v2.utils import log_message

class TidalApiClass:
    def __init__(self, token_file='tidalapi_token.json', text_widget=None, url_entry=None, on_success=None):
        self.token_file = token_file
        self.session = tidalapi.Session()
        self.text_widget = text_widget
        self.url_entry = url_entry
        self.on_success = on_success  # Callback for successful login
        log_message("TidalApiClass initialized.")

    def login(self):
        """Starts the OAuth login process in a separate thread."""
        log_message("Starting OAuth login process for Tidal...", tag="yellow")
        thread = threading.Thread(target=self._login_thread)
        thread.daemon = True
        thread.start()

    def _login_thread(self):
        """The actual OAuth login process, to be run in a separate thread."""
        try:
            login, future = self.session.login_oauth()

            # Display the URL where the user should log in
            log_message("Please open the following URL to complete the login:")

            if self.url_entry:
                # Display the Entry widget and set the URL
                self.url_entry.place(relx=0.5, rely=0.45, anchor="center")
                self.url_entry.delete(0, 'end')  # Clear previous content
                self.url_entry.insert(0, login.verification_uri_complete)  # Insert URL
                self.url_entry.configure()

            # Wait for the user to complete the login
            future.result()

            if self.session.check_login():
                log_message("Successfully connected to Tidal!", tag="green")
                self.save_token()
                self._schedule_success_callback()  # Schedule the callback after 1 second
            else:
                log_message("Login failed.", tag="red")

        except Exception as e:
            log_message(f"An error occurred during the login process: {str(e)}", tag="red")

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
            log_message("Token saved successfully.", tag="green")
        except Exception as e:
            log_message(f"Failed to save token: {str(e)}", tag="red")

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
                self.save_token()
                log_message("Successfully connected with saved token!", tag="green")
                self._schedule_success_callback()  # Schedule the callback after 1 second

            else:
                log_message("Error loading token", tag="red")
        except FileNotFoundError:
            log_message("No saved token file found. Please log in first.", tag="red")
        except Exception as e:
            log_message(f"Error loading token: {str(e)}", tag="red")

    def _schedule_success_callback(self):
        """Schedule the on_success callback after 1 second without blocking the GUI."""
        if self.on_success and self.text_widget:
            self.text_widget.after(2000, self.on_success)  # Wait 2 seconds and execute on_success

    def display_user_playlists(self, treeview_widget):
        """Displays all playlists of the currently logged-in user in the provided Treeview widget."""
        try:
            self.playlists = self.session.user.playlists()  # Save playlists for later use
            if self.playlists:
                log_message("User's Playlists:", tag="green")
                treeview_widget.delete(*treeview_widget.get_children())  # Clear previous content
                for playlist in self.playlists:
                    # Get the last modified date
                    last_modified = playlist.last_updated.strftime("%Y-%m-%d") if playlist.last_updated else "Unknown"

                    # Insert the playlist into the Treeview
                    treeview_widget.insert("", "end", values=(playlist.name, last_modified))
                    log_message(f" - {playlist.name} (Last Modified: {last_modified})", tag="white")
            else:
                log_message("No playlists found for this user.", tag="yellow")
        except Exception as e:
            log_message(f"Failed to retrieve playlists: {str(e)}", tag="red")

    def get_playlist_tracks(self, playlist):
        """Returns all tracks in a given playlist with prepared data, including the label."""
        try:
            tracks = playlist.tracks()
            if tracks:
                log_message(f"Retrieved tracks for playlist '{playlist.name}'.", tag="blue")
                prepared_tracks = []
                for track in tracks:
                    # Convert duration from seconds to minutes:seconds
                    minutes, seconds = divmod(track.duration, 60)
                    duration_formatted = f"{minutes}:{seconds:02}"

                    # Get release year
                    if track.tidal_release_date:
                        release_year = track.tidal_release_date.strftime("%Y")
                    else:
                        release_year = "Unknown"

                    # Prepare the track data
                    track_data = {
                        'title': track.name,
                        'artist': track.artist.name,
                        'duration': duration_formatted,
                        'album': track.album.name,
                        'release_year': release_year,
                        'popularity': track.popularity,
                    }
                    prepared_tracks.append(track_data)
                    log_message(f"Added track '{track.name}' to prepared tracks.", tag="white")
                return prepared_tracks
            else:
                log_message(f"No tracks found in playlist '{playlist.name}'.", tag="yellow")
                return []
        except Exception as e:
            log_message(f"Failed to retrieve tracks for playlist '{playlist.name}': {str(e)}", tag="red")
            return []
