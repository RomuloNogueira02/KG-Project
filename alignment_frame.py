import customtkinter as ctk

class AlignmentFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, border_width=1, height=100, width=1000, border_color="yellow")
        