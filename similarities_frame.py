import customtkinter as ctk


class SimilaritiesFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, border_width=1, height=250, width=1000, border_color="blue")
        

        title = ctk.CTkLabel(self, text="Activate", font=("Arial", 18))
        title.place(anchor="w", relx= 0.01, rely=0.1)

        self.lexical_similarity_check = ctk.CTkCheckBox(self, text="Lexical Similarity", font=("Arial", 15))
        self.lexical_similarity_check.place(anchor="w", relx=0.01, rely=0.3)
        self.lexical_similarity_check.select()
        self.lexical_similarity_check_info = True

        self.lexical_similarity_options = ctk.CTkOptionMenu(self, values=["Jaccard", "Cosine", "Levenshtein"])
        self.lexical_similarity_options.place(anchor="w", relx=0.18, rely=0.3)

        self.llm_check = ctk.CTkCheckBox(self, text="LLM", font=("Arial", 15))
        self.llm_check.place(anchor="w", relx=0.01, rely=0.5)
        self.llm_check.select()
        self.llm_info = True

        # Infos
        self.infos_label = ctk.CTkLabel(self, text="Infos about the current alignment", font=("Arial", 15))
        self.infos_label.place(anchor="w", relx=0.7, rely=0.1)



        
    
