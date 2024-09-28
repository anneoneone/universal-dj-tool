import ttkbootstrap as ttk

class RunDJToolTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Beispielinhalt für den "Run DJ Tool" Tab
        self.label = ttk.Label(self, text="DJ Tool Ausführen", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Sicherstellen, dass das Frame gepackt wird
        self.pack(fill="both", expand=True)
        self.update()
