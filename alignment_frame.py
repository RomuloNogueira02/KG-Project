import customtkinter as ctk
import pickle
from ontologyAlignment import OntologyAlignment


class AlignmentFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, border_width=1, height=100, width=1000, border_color="yellow")

        self.align_button = ctk.CTkButton(self, text="Align Ontologies", font=("Arial", 15), command=self.align_ontologies)
        self.align_button.place(anchor="center", relx=0.5, rely=0.5)
        
        self.ontology_alignment = OntologyAlignment()

    def align_ontologies(self):
        result = self.ontology_alignment.compute_alignment()
        with open("alignment_result.pkl", "wb") as f:
            pickle.dump(result, f)