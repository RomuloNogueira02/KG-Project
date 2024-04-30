import customtkinter as ctk

class HeaderFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, border_width=1, height=50, width=1000, border_color="red")
        
        title = ctk.CTkLabel(self, text="Ontology Alignment", font=("Arial", 20))
        title.place(anchor="w")