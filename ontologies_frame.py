import customtkinter as ctk
from customtkinter import filedialog  
import tkinter as tk
import time
from functions import convert_seconds

class OntologiesFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, border_width=1, height=200, width=1000)


        self.extract_syn_label = ctk.CTkLabel(self, text="Extract Synonyms: ", font=("Arial", 15))
        self.extract_syn_label.place(anchor="w", relx=0.01, rely=0.15)

        self.extract_syn_options = ctk.CTkOptionMenu(self, values=["Yes", "No"], command=self.update_syn)
        self.extract_syn_options.place(anchor="w", relx=0.15, rely=0.15)


        self.ontology1_label = ctk.CTkLabel(self, text="Ontology 1", font=("Arial", 12))
        self.ontology1_label.place(anchor="w", relx=0.3, rely=0.4)

        self.ontology1_file = ctk.CTkButton(self, text="Select File for the first ontology", font=("Arial", 12), command=self.select_ontology1)
        self.ontology1_file.place(relx=0.24, rely=0.5)

        self.time_ontology1 = tk.StringVar()
        self.time_ontology1.set("Time: 0s")

        self.text_time_ontology1 = ctk.CTkLabel(self, textvariable=self.time_ontology1, font=("Arial", 10))
        self.text_time_ontology1.place(anchor="center", relx=0.33, rely=0.75)
        

        self.ontology2_label = ctk.CTkLabel(self, text="Ontology 2", font=("Arial", 12))
        self.ontology2_label.place(anchor="w", relx=0.6, rely=0.4)

        self.ontology2_file = ctk.CTkButton(self, text="Select File for the second ontology", font=("Arial", 12), command=self.select_ontology2)
        self.ontology2_file.place(relx=0.53, rely=0.5)

        self.time_ontology2 = tk.StringVar()
        self.time_ontology2.set("Time: 0s")

        self.text_time_ontology2 = ctk.CTkLabel(self, textvariable=self.time_ontology2, font=("Arial", 10))
        self.text_time_ontology2.place(anchor="center", relx=0.63, rely=0.75)

    def select_ontology1(self):
        filename = filedialog.askopenfilename()
        start = time.time()
        self.master.children["!alignmentframe"].ontology_alignment.load_ontology(filename)
        self.master.children["!similaritiesframe"].ontology1_loaded.set("Ontology 1: Loaded")
        end = time.time()
        self.time_ontology1.set(f"Time: {convert_seconds(end-start)}s")
    
    def select_ontology2(self):
        filename = filedialog.askopenfilename()
        start = time.time()
        self.master.children["!alignmentframe"].ontology_alignment.load_ontology(filename)
        self.master.children["!similaritiesframe"].ontology2_loaded.set("Ontology 2: Loaded")
        self.master.children["!similaritiesframe"].status.set("General State: Ready")
        end = time.time()
        self.time_ontology2.set(f"Time: {convert_seconds(end-start)}s")
        
        

    def update_syn(self, value):
        self.master.children["!alignmentframe"].ontology_alignment.define_syn_extract(value)