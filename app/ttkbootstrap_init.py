# Datei: main.py
import ttkbootstrap as ttk
from modules_v2.login_window import LoginWindow

# Hauptprogramm (main)
def main():
    # Hauptfenster der Anwendung erstellen
    app = ttk.Window(themename="darkly")
    app.title("Hauptfenster mit Login")
    app.geometry("1200x800")

    # LoginWindow als komplettes Frame hinzufügen
    login_frame = LoginWindow(app, background="#00A2E8")

    # Hauptloop starten
    app.mainloop()

if __name__ == "__main__":
    main()
