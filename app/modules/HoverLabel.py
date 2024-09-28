import tkinter as tk


class HoverLabel(tk.Label):

    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.toggle_bg = "#FF2288"
        self.toggle_bd = 2
        self.toggle_highlightthickness = 3
        self.is_hovering = False
        self.after_id = None
        self.default_bg = self.cget("bg")
        self.default_bd = self.cget("bd")
        self.default_highlightthickness = self.cget("highlightthickness")
        self.default_fg = self.cget("fg")
        self.default_width = self.cget("width")
        self.default_height = self.cget("height")
        self.default_bd = self.cget("bd")
        self.default_highlightbackground = self.cget("highlightbackground")
        self.default_highlightcolor = self.cget("highlightcolor")
        self.default_highlightthickness = self.cget("highlightthickness")
        self.default_activebackground = self.cget("activebackground")
        self.default_activeforeground = self.cget("activeforeground")

        self.configure(
            cursor="hand2",
            compound="left",
            state="active",
            font=("Courier New", 14, "bold"),
            highlightthickness=4,  # Dünne Umrandung
            bd=1,  # Dicke der Umrandung (Rahmen)
            highlightbackground="white",  # Farbe der Umrandung (wenn der Rahmen keinen Fokus hat)
            highlightcolor="yellow",  # Farbe der Umrandung, wenn das Widget den Fokus hat
            relief="solid",  # Stil der Umrandung
            activebackground="white",
            activeforeground="white",
        )

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

    def toggle_border(self):
        if self.is_hovering:
            current_bd = self.cget("bd")
            current_highlightthickness = self.cget("highlightthickness")
            new_bd = (
                self.toggle_bd if current_bd == self.default_bd else self.default_bd
            )
            new_highlightthickness = (
                self.toggle_highlightthickness
                if current_highlightthickness == self.default_highlightthickness
                else self.default_highlightthickness
            )
            self.configure(bd=new_bd, highlightthickness=new_highlightthickness)
            self.after_id = self.after(200, self.toggle_border)

    def on_enter(self, event):
        self.is_hovering = True
        self.toggle_background()
        self.toggle_border()

    def on_leave(self, event):
        self.is_hovering = False
        if self.after_id:
            self.after_cancel(self.after_id)
        self.configure(bg=self.default_bg, fg=self.default_fg)

    def on_click(self, event):
        if self.command:
            self.command()


def create_hover_label(parent, text, command, **kwargs):
    return HoverLabel(parent, text=text, command=command, **kwargs)
