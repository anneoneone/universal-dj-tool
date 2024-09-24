import tkinter as tk


class HoverLabel(tk.Label):

    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.configure(
            cursor="hand2",
            compound="left",
            state="active",
            font=("Courier New", 14, "bold"),
            highlightthickness=1,  # Dünne Umrandung
            highlightbackground="pink",  # Farbe der Umrandung
            highlightcolor="pink",  # Farbe, wenn es den Fokus hat
            relief="flat",  # Stil der Umrandung
            bd=1,  # Dicke der Umrandung
        )

        self.toggle_bg = "#FF2288"
        self.is_hovering = False
        self.after_id = None
        self.default_bg = self.cget("bg")
        self.default_fg = self.cget("fg")
        # self.default_bitmap = self.cget("bitmap")
        self.default_width = self.cget("width")
        self.default_height = self.cget("height")
        self.default_bd = self.cget("bd")
        self.default_highlightbackground = self.cget("highlightbackground")
        self.default_highlightcolor = self.cget("highlightcolor")
        self.default_highlightthickness = self.cget("highlightthickness")
        self.default_activebackground = self.cget("activebackground")
        self.default_activeforeground = self.cget("activeforeground")

        self.command = command
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def toggle_state(self):
        if self.default_state == "active":
            return "disabled"
        else:
            return "active"

    def toggle_background(self):
        if self.is_hovering:
            current_bg = self.cget("bg")
            new_bg = (
                self.toggle_bg if current_bg == self.default_bg else self.default_bg
            )
            self.configure(bg=new_bg)
            self.after_id = self.after(200, self.toggle_background)

    def on_enter(self, event):
        self.is_hovering = True
        self.toggle_background()

    def on_leave(self, event):
        self.is_hovering = False
        if self.after_id:
            self.after_cancel(self.after_id)
        self.configure(bg=self.default_bg, fg=self.default_fg)

    def on_click(self, event):
        if self.command:
            # self.configure(state="disabled")
            self.command()


def create_hover_label(parent, text, command, **kwargs):
    return HoverLabel(parent, text=text, command=command, **kwargs)
