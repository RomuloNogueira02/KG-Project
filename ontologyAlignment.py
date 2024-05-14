from functions import *
import time
from nltk.metrics import binary_distance, edit_distance, jaccard_distance, masi_distance
from jarowinkler import jaro_similarity, jarowinkler_similarity
from sentence_transformers import SentenceTransformer, util
from transformers import AutoModel, AutoTokenizer, pipeline
import pandas as pd


class OntologyAlignment:

    def __init__(self, lexical_similarity= "Jaccard", llm="all-mpnet-base-v2") -> None:
        self.lexical_similarity = lexical_similarity
 
        
        self.define_llm_model(llm)
        self.define_lexical_function(lexical_similarity)

        self.ontology1_loaded = False
        self.ontology2_loaded = False

        self.final_alignment = {}
        self.remaining = {}


    def load_ontology(self, path):
        
        ontology = loadOntology(path)
        labels = get_labels(ontology) 
        
        if self.ontology1_loaded == False:
            self.ontology1 = ontology
            self.labels_o1 = labels
            self.ontology1_loaded = True
        else:
            self.ontology2 = ontology
            self.labels_o2 = labels
            self.ontology2_loaded = True

            # self.load_embeddings(list(set(self.labels_o1).union(set(self.labels_o2))))


    def load_embeddings(self, set_labels: set):
        self.string_embedding = {}
        for label in set_labels:
            self.string_embedding[label] = self.llm.encode(label)
    
    def define_llm_model(self, llm="all-mpnet-base-v2"):
        if llm in ["all-mpnet-base-v2", "paraphrase-MiniLM-L6-v2", "distilbert-base-nli-stsb-mean-tokens"]:
            self.llm = SentenceTransformer(llm)
        else: #! bert-base-uncased
            self.tokenizer = AutoTokenizer.from_pretrained(llm)
            self.model = AutoModel.from_pretrained(llm)
            self.llm_pipeline = pipeline('feature-extraction', model=self.model, tokenizer=self.tokenizer)

    def define_lexical_function(self, lexical_similarity ="Jaccard"):
        if lexical_similarity == "Jaccard":
            self.func = jaccard_distance
        elif lexical_similarity == "Levenshtein":
            self.func = edit_distance
        elif lexical_similarity == "Binary":
            self.func = binary_distance
        elif lexical_similarity == "Masi":
            self.func = masi_distance
        elif lexical_similarity == "Jaro":
            self.func = jaro_similarity
        elif lexical_similarity == "Jaro-Winkler":
            self.func = jarowinkler_similarity
        else:
            raise ValueError("The lexical similarity must be Jaccard, Levenshtein, Binary, Masi, Jaro or Jaro-Winkler")
        

    def compute_lexical_similarity(self, MIN_THRESHOLD=0.85):
        scores_lexical_similarity = {}
        for l1 in self.labels_o1:
            for l2 in self.labels_o2:
                if self.lexical_similarity == "Jaccard" or self.lexical_similarity == "Masi":
                    set_l1 = set(l1.split())
                    set_l2 = set(l2.split())
                    scores_lexical_similarity[(l1, l2)] = 1 - self.func(set_l1, set_l2)
                elif self.lexical_similarity == "Levenshtein":
                    scores_lexical_similarity[(l1, l2)] = 1 - (self.func(l1, l2) / max(len(l1), len(l2)))
                elif self.lexical_similarity == "Binary":
                    scores_lexical_similarity[(l1, l2)] = 1 - self.func(l1, l2)
                elif self.lexical_similarity == "Jaro":
                    scores_lexical_similarity[(l1, l2)] = self.func(l1, l2)
                elif self.lexical_similarity == "Jaro-Winkler":
                    scores_lexical_similarity[(l1, l2)] = self.func(l1, l2)
                else:
                    scores_lexical_similarity[(l1, l2)] = self.func(l1, l2)

                # if self.lexical_similarity == "Jaccard":
                #     set_l1 = set(l1.split())
                #     set_l2 = set(l2.split())

                #     scores_lexical_similarity[(l1, l2)] = 1 - self.func(set_l1, set_l2)
                # else:
                #     scores_lexical_similarity[(l1, l2)] = self.func(l1, l2)

        self.final_alignment = {key: value for key, value in scores_lexical_similarity.items() if value >= MIN_THRESHOLD}
        palavras_unicas = {palavra for tupla in self.final_alignment.keys() for palavra in tupla}
        self.remaining = {key: value for key, value in scores_lexical_similarity.items() if (value < MIN_THRESHOLD and not any(palavra in palavras_unicas for palavra in key))}

    def compute_cosine_similarity(self):

        print("Loading embeddings...")
        words = {palavra for tupla in self.remaining.keys() for palavra in tupla}
        self.load_embeddings(words)

        print("Embeddings loaded")


        lexical_cosine_similarity = {}
        # progress = 0
        for t in self.remaining.items():
            embedding1 = self.string_embedding[t[0][0]]
            embedding2 = self.string_embedding[t[0][1]]
            lexical_cosine_similarity[t[0]] = max(t[1], util.cos_sim(embedding1, embedding2)[0][0].item())
            # progress += 1

            # percent = calculate_progress(progress, len(self.remaining))
            # if percent in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
            #     print(f"{percent}% completed")


        self.final_alignment.update(lexical_cosine_similarity)
        self.remaining.clear()
    
    def compute_alignment(self, MIN_THRESHOLD=0.80):

        self.compute_lexical_similarity()
        print("Lexical similarity computed")

        self.compute_cosine_similarity()
        print("Cosine similarity computed")
        
        # Antes de retornar filtrar por este MIN_THRESHOLD
        self.final_alignment = {key: value for key, value in self.final_alignment.items() if value >= MIN_THRESHOLD}
        
        return self.final_alignment

    def one_to_one_alignment(self):
        
        print("One to one alignment")

        triplos = [(key[0], key[1], value) for key, value in self.final_alignment.items()]

        df = pd.DataFrame(triplos, columns=['ontology 1', 'ontology 2', 'score'])
        # Clean the left side 
        toDrop = set()
        for index, row in df.iterrows():
            duplicates = df[df["ontology 1"] == row['ontology 1']]
            if len(duplicates) > 1:
                indexes = set(duplicates[duplicates["score"] < max(duplicates["score"])].index.values.tolist())
                toDrop |= indexes

        droped_left = df.drop(toDrop)

        # Clean the right side
        toDrop2 = set()
        for index, row in droped_left.iterrows():
            duplicates = droped_left[droped_left["ontology 2"] == row['ontology 2']]

            if len(duplicates) > 1:
                indexes = set(duplicates[duplicates["score"] < max(duplicates["score"])].index.values.tolist())
                toDrop2 |= indexes

        self.final_alignment = droped_left.drop(toDrop2)
        print("One to one alignment: Finished!")
        return self.final_alignment.sort_values(by='score', ascending=False)