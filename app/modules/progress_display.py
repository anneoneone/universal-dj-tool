import tkinter as tk

from modules.constants import welcome_text


def create_progress_display(root):
    progress_display = tk.Text(
        root,
        width=50,
        wrap=tk.WORD,
        bg="black",
        fg="white",
        highlightthickness=1,  # Dünne Umrandung
        highlightbackground="pink",  # Farbe der Umrandung
        highlightcolor="pink",  # Farbe, wenn es den Fokus hat
        relief="ridge",  # Stil der Umrandung
        bd=1,  # Dicke der Umrandung
    )
    progress_display.tag_configure("orange", foreground="orange")
    progress_display.tag_configure("black", foreground="black")
    progress_display.tag_configure("red", foreground="red")
    progress_display.tag_configure("green", foreground="green")
    progress_display.tag_configure("white", foreground="white")
    progress_display.tag_configure("yellow", foreground="yellow")

    progress_display.insert(1.0, welcome_text)
    return progress_display


def print_progress_display(progress_display, text, tag="white"):
    symbol = ""
    if tag == "green":
        symbol = "✓ "
    elif tag == "yellow":
        symbol = "⚠ "
    elif tag == "red":
        symbol = "✗ "
    progress_display.insert(tk.END, symbol + text + "\n", tag)
    progress_display.see(tk.END)
