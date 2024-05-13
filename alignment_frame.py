import customtkinter as ctk
import pickle
from ontologyAlignment import OntologyAlignment
import time
import tkinter as tk
from functions import convert_seconds

class AlignmentFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, border_width=1, height=100, width=1000, border_color="yellow")

        self.align_button = ctk.CTkButton(self, text="Align Ontologies", font=("Arial", 15), command=self.align_ontologies)
        self.align_button.place(anchor="center", relx=0.5, rely=0.5)

        self.text_time = tk.StringVar()
        self.text_time.set("Time: 0s")

        self.time = ctk.CTkLabel(self, textvariable=self.text_time, font=("Arial", 10))
        self.time.place(anchor="center", relx=0.5, rely=0.8)
        
        self.ontology_alignment = OntologyAlignment()

    def align_ontologies(self):
        
        print(self.master.children)

        start = time.time()

        self.ontology_alignment_min_threshold = self.master.children["!similaritiesframe"].get_min_threshold()

        print(self.ontology_alignment_min_threshold)

        result = self.ontology_alignment.compute_alignment(self.ontology_alignment_min_threshold)
        with open("alignment_result.pkl", "wb") as f:
            pickle.dump(result, f)
        end = time.time()
        self.text_time.set(f"Time: {convert_seconds(end-start)}s")
