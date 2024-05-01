import customtkinter as ctk
from customtkinter import filedialog  

class OntologiesFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, border_width=1, height=200, width=1000, border_color="green")

        self.ontology1_label = ctk.CTkLabel(self, text="Ontology 1", font=("Arial", 12))
        self.ontology1_label.place(anchor="w", relx=0.3, rely=0.3)

        self.ontology1_file = ctk.CTkButton(self, text="Select File for the first ontology", font=("Arial", 12), command=self.select_ontology1)
        self.ontology1_file.place(relx=0.24, rely=0.4)

        self.ontology2_label = ctk.CTkLabel(self, text="Ontology 2", font=("Arial", 12))
        self.ontology2_label.place(anchor="w", relx=0.6, rely=0.3)

        self.ontology2_file = ctk.CTkButton(self, text="Select File for the second ontology", font=("Arial", 12), command=self.select_ontology2)
        self.ontology2_file.place(relx=0.53, rely=0.4)

    def select_ontology1(self):
        filename = filedialog.askopenfilename()
        print(filename)
        # Load ontology... 

        return filename
    
    def select_ontology2(self):
        filename = filedialog.askopenfilename()
        print(filename)
        # Load ontology... 

        return filename
        

    