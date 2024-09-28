# Datei: utils.py

def show_frame(frame):
    """Zeigt den angegebenen Frame an und erstreckt ihn über den gesamten Bereich des Hauptframes."""
    frame.pack(fill="both", expand=True)

def hide_frame(frame):
    """Verbirgt den angegebenen Frame, indem es das Frame-Packing entfernt."""
    frame.pack_forget()
