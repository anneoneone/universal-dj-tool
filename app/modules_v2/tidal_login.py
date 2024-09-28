import json
import threading
import time
import tidalapi
from datetime import datetime

class TidalLogin:
    def __init__(self, token_file='tidalapi_token.json', text_widget=None, url_entry=None, on_success=None):
        self.token_file = token_file
        self.session = tidalapi.Session()
        self.text_widget = text_widget
        self.url_entry = url_entry
        self.on_success = on_success  # Callback für erfolgreichen Login
        self.log_message("TidalLogin initialisiert.")

    def log_message(self, message, tag="white"):
        """Helper function to print messages in text_widget."""
        if self.text_widget:
            self.text_widget.configure(text=message)
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
            self.log_message("Please open the following URL to complete the login:")

            if self.url_entry:
                # Entry-Widget anzeigen und URL setzen
                self.url_entry.place(relx=0.5, rely=0.45, anchor="center")
                self.url_entry.delete(0, 'end')  # Vorherigen Inhalt löschen
                self.url_entry.insert(0, login.verification_uri_complete)  # URL einfügen
                self.url_entry.configure()

            # Wait for the user to complete the login
            future.result()

            if self.session.check_login():
                self.log_message("Successfully connected to Tidal!", tag="green")
                self.save_token()
                self._schedule_success_callback()  # Planen des Callback-Aufrufs nach 1 Sekunde
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
                self.save_token()
                self.log_message("Successfully connected with saved token!", tag="green")
                self._schedule_success_callback()  # Planen des Callback-Aufrufs nach 1 Sekunde

            else:
                self.log_message("Error loading token", tag="red")
        except FileNotFoundError:
            self.log_message("No saved token file found. Please log in first.", tag="red")
        except Exception as e:
            self.log_message(f"Error loading token: {str(e)}", tag="red")

    def _schedule_success_callback(self):
        """Schedule the on_success callback after 1 second without blocking the GUI."""
        if self.on_success:
            self.text_widget.after(2000, self.on_success)  # Warte 1 Sekunde (1000 ms) und führe on_success aus

    def display_user_playlists(self, listbox_widget):
        """Displays all playlists of the currently logged-in user in the provided Listbox widget."""
        try:
            playlists = self.session.user.playlists()
            if playlists:
                self.log_message("User's Playlists:", tag="green")
                listbox_widget.delete(0, "end")  # Vorherige Inhalte löschen
                for playlist in playlists:
                    listbox_widget.insert("end", playlist.name)
                    self.log_message(f" - {playlist.name} (ID: {playlist.id})", tag="white")
            else:
                self.log_message("No playlists found for this user.", tag="yellow")
        except Exception as e:
            self.log_message(f"Failed to retrieve playlists: {str(e)}", tag="red")
