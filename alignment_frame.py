import customtkinter as ctk

class AlignmentFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, border_width=1, height=100, width=1000, border_color="yellow")

        self.align_button = ctk.CTkButton(self, text="Align Ontologies", font=("Arial", 15))
        self.align_button.place(anchor="center", relx=0.5, rely=0.5)
        
        