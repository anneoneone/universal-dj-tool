import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from modules_v2.tidal_login import TidalLogin
from modules_v2.utils import show_frame, hide_frame
import time

class LoginWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Referenz zum Hauptfenster

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
        tidal = TidalLogin(
            text_widget=self.text_label, 
            url_entry=self.url_entry,
            on_success=self.on_login_success  # Callback für erfolgreichen Login
        )
        tidal.load_token()

        # Falls kein gültiger Token geladen wurde, dann starten wir den Login
        if not tidal.session.check_login():
            tidal.login()

    def on_login_success(self):
        # Wenn der Login erfolgreich ist, blenden wir den Hauptframe aus und den zweiten Frame ein
        hide_frame(self)
