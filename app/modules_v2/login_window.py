import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from modules_v2.tidal_login import TidalLogin
from modules_v2.utils import hide_frame

class LoginWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Referenz zum Hauptfenster
        self.on_login_success = None  # Callback für erfolgreichen Login

        # Frame auf die komplette Größe des Elternfensters ausdehnen
        self.pack(fill="both", expand=True)

        # UI-Komponenten erstellen
        self.create_widgets()

    def create_widgets(self):
        # Button in der Mitte des Fensters platzieren
        self.button = ttk.Button(self, text="Klicke mich", command=self.on_button_click, bootstyle=PRIMARY)
        self.button.place(relx=0.5, rely=0.35, anchor="center")

        # Textausgabe unter dem Button hinzufügen
        self.text_label = ttk.Label(self, text="", font=("Helvetica", 14))
        self.text_label.place(relx=0.5, rely=0.4, anchor="center")

        # Ein Entry-Widget für den Link, standardmäßig unsichtbar
        self.url_entry = ttk.Entry(self)
        self.url_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.url_entry.place_forget()  # Starten mit verstecktem Entry-Widget

    def on_button_click(self):
        # Wenn der Button geklickt wird, Textausgabe ändern
        self.text_label.configure(text="Button wurde geklickt!")
        self.tidal_login = TidalLogin(
            text_widget=self.text_label, 
            url_entry=self.url_entry,
            on_success=self._on_login_success  # Callback für erfolgreichen Login
        )
        self.tidal_login.load_token()

        # Falls kein gültiger Token geladen wurde, dann starten wir den Login
        if not self.tidal_login.session.check_login():
            self.tidal_login.login()

    def _on_login_success(self):
        # Wenn der Login erfolgreich ist, blenden wir den Hauptframe aus und rufen das Callback auf
        if self.on_login_success:
            self.on_login_success(tidal=self.tidal_login)
