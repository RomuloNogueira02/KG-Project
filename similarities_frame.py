import customtkinter as ctk
import tkinter as tk

class SimilaritiesFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, border_width=1, height=250, width=1000)
        

        title = ctk.CTkLabel(self, text="Activate", font=("Arial", 18))
        title.place(anchor="w", relx= 0.01, rely=0.1)

        self.lexical_similarity_text = ctk.CTkLabel(self, text="Lexical Similarity: ", font=("Arial", 15))
        self.lexical_similarity_text.place(anchor="w", relx=0.01, rely=0.3)

        self.lexical_similarity_options = ctk.CTkOptionMenu(self, values=["Jaccard", "Levenshtein", "Binary", "Masi", "Jaro", "Jaro-Winkler"], command=self.update_lexical_similarity)
        self.lexical_similarity_options.place(anchor="w", relx=0.15, rely=0.3)

        # ------------------

        self.llm_text = ctk.CTkLabel(self, text="LLM Model: ", font=("Arial", 15))
        self.llm_text.place(anchor="w", relx=0.01, rely=0.5)

        self.llm_options = ctk.CTkOptionMenu(self, values=["all-mpnet-base-v2", "paraphrase-MiniLM-L6-v2", "distilbert-base-nli-stsb-mean-tokens", "bert-base-uncased"], command=self.update_llm_model)
        self.llm_options.place(anchor="w", relx=0.15, rely=0.5)

        # ------------------

        self.min_threshold_text = ctk.CTkLabel(self, text="Minimum Threshold: ", font=("Arial", 15))
        self.min_threshold_text.place(anchor="w", relx=0.01, rely=0.7)

        self.min_threshold_value = tk.DoubleVar()
        self.min_threshold_value.set(0.8)

        self.min_threshold_entry = ctk.CTkEntry(self, textvariable=self.min_threshold_value)
        self.min_threshold_entry.place(anchor="w", relx=0.15, rely=0.7)

        # ------------------

        self.export_file = ctk.CTkLabel(self, text="Export format: ", font=("Arial", 15))
        self.export_file.place(anchor="w", relx=0.01, rely=.9)

        self.export_file = ctk.CTkOptionMenu(self, values=[".rdf", ".xlsx"], command=self.update_export)
        self.export_file.place(anchor="w", relx=0.15, rely=.9)
        #-----------------

        self.create_infos()

        # Infos
        self.infos_label = ctk.CTkLabel(self, text="Infos about the current alignment", font=("Arial", 15))
        self.infos_label.place(anchor="w", relx=0.7, rely=0.1)

        self.lexical_similarity_label = ctk.CTkLabel(self, textvariable= self.lexical_similarity, font=("Arial", 15))
        self.lexical_similarity_label.place(anchor="w", relx=0.7, rely=0.2)

        self.llm_model_label = ctk.CTkLabel(self, textvariable= self.llm_model, font=("Arial", 15))
        self.llm_model_label.place(anchor="w", relx=0.7, rely=0.3)

        self.ontology1_loaded_label = ctk.CTkLabel(self, textvariable= self.ontology1_loaded, font=("Arial", 15))
        self.ontology1_loaded_label.place(anchor="w", relx=0.7, rely=0.4)

        self.ontology2_loaded_label = ctk.CTkLabel(self, textvariable= self.ontology2_loaded, font=("Arial", 15))
        self.ontology2_loaded_label.place(anchor="w", relx=0.7, rely=0.5)

        self.status_label = ctk.CTkLabel(self, textvariable= self.status, font=("Arial", 15))
        self.status_label.place(anchor="w", relx=0.7, rely=0.6)
    
    def create_infos(self):
        self.lexical_similarity = tk.StringVar()
        self.lexical_similarity.set("Current Lexical Similarity: Jaccard")
        self.llm_model = tk.StringVar()
        self.llm_model.set("Current LLM Model: all-mpnet-base-v2")
        self.ontology1_loaded = tk.StringVar()
        self.ontology1_loaded.set("Ontology 1: Not loaded")
        self.ontology2_loaded = tk.StringVar()
        self.ontology2_loaded.set("Ontology 2: Not loaded")
        self.status = tk.StringVar()
        self.status.set("General State: Not ready")
        self.export_method = tk.StringVar()
    
    def update_lexical_similarity(self, value):
        self.lexical_similarity.set(f"Current Lexical Similarity: {value}")
        self.master.children["!alignmentframe"].ontology_alignment.define_lexical_function(value)

    def update_llm_model(self, value):
        self.llm_model.set(f"Current LLM Model: {value}")
        self.master.children["!alignmentframe"].ontology_alignment.define_llm_model(value)
    
    def update_export(self,value):
        self.export_method = value
        self.master.children["!alignmentframe"].export_method = value




    def get_min_threshold(self):
        return self.min_threshold_value.get()