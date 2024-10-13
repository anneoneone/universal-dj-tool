import ttkbootstrap as ttk
from modules_v2.login_window import LoginWindow
from modules_v2.AppWindow import AppWindow
from modules_v2.utils import show_frame, hide_frame


# Hauptprogramm (main)
def main():
    # Hauptfenster der Anwendung erstellen
    app = ttk.Window(themename="solar")
    app.title("Hauptfenster mit Login")
    app.geometry("1200x800")

    # LoginWindow als komplettes Frame hinzufügen
    login_frame = LoginWindow(app)

    # Event-Handler für erfolgreichen Login und Weitergabe der Tidal-Instanz
    def on_login_success(tidal):
        hide_frame(login_frame)
        # AppWindow mit der übergebenen TidalApiClass-Instanz erzeugen
        app_frame = AppWindow(app, tidal)
        show_frame(app_frame)

    # Setzen des Callbacks für den erfolgreichen Login
    login_frame.on_login_success = on_login_success

    # Hauptloop starten
    app.mainloop()

if __name__ == "__main__":
    main()
