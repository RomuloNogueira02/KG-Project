from functions import *
import time
from nltk.metrics import binary_distance, edit_distance, jaccard_distance, masi_distance
from jarowinkler import jaro_similarity, jarowinkler_similarity
from sentence_transformers import SentenceTransformer, util


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

            self.load_embeddings(list(set(self.labels_o1).union(set(self.labels_o2))))


    def load_embeddings(self, set_labels: set):
        self.string_embedding = {}
        for label in set_labels:
            self.string_embedding[label] = self.llm.encode(label)
    
    def define_llm_model(self, llm="all-mpnet-base-v2"):
        self.llm = SentenceTransformer(llm)
        

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
        

    def compute_lexical_similarity(self, MIN_THRESHOLD=0.8):
        scores_lexical_similarity = {}
        for l1 in self.labels_o1:
            for l2 in self.labels_o2:
                if (l1, l2) not in scores_lexical_similarity and (l2, l1) not in scores_lexical_similarity:
                    if self.lexical_similarity == "Jaccard":
                        set_l1 = set(l1.split())
                        set_l2 = set(l2.split())

                        scores_lexical_similarity[(l1, l2)] = 1 - self.func(set_l1, set_l2)
                    else:
                        scores_lexical_similarity[(l1, l2)] = self.func(l1, l2)

        self.final_alignment = {key: value for key, value in scores_lexical_similarity.items() if value >= MIN_THRESHOLD}
        self.remaining = {key: value for key, value in scores_lexical_similarity.items() if value < MIN_THRESHOLD}

    def compute_cosine_similarity(self):
        lexical_cosine_similarity = {}
        for t in self.remaining.items():
            embedding1 = self.string_embedding[t[0][0]]
            embedding2 = self.string_embedding[t[0][1]]
            lexical_cosine_similarity[t[0]] = (t[1], util.cos_sim(embedding1, embedding2)[0][0].item())

        self.final_alignment.update(lexical_cosine_similarity)
        self.remaining.clear()
    
    def compute_alignment(self, MIN_THRESHOLD=0.8):

        self.compute_lexical_similarity(MIN_THRESHOLD)
        self.compute_cosine_similarity()
        
        return self.final_alignment

