from functions import *
import time
from nltk.metrics import binary_distance, edit_distance, jaccard_distance, masi_distance
from jarowinkler import jaro_similarity, jarowinkler_similarity
from sentence_transformers import SentenceTransformer, util

# I think we should have a class for the ontology alignment, where executes all the pipeline.
# With this class we can personalize the pipeline, running different ways to align ontologies.

class OntologyAlignment:

    def __init__(self, path_o1, path_o2, lexical_similarity= "Jaccard", llm="all-mpnet-base-v2") -> None:
        
        self.ontology1 = loadOntology(path_o1)
        self.ontology2 = loadOntology(path_o2)

        self.labels_o1 = get_labels(self.ontology1)
        self.labels_o2 = get_labels(self.ontology2)

        set_labels = set(self.labels_o1).union(set(self.labels_o2))

        self.lexical_similarity = lexical_similarity

        # Ver isto melhor se é suposto ser assim
        self.llm = SentenceTransformer(llm)

        self.load_embeddings(set_labels)
        self.define_lexical_function()

    # Ontology is 1 or 2 
    def getClassesOntology(self, ontology:int) -> list:
        if ontology == 1:
            return list(self.ontology1.classes())
        elif ontology == 2:
            return list(self.ontology2.classes())
        else:
            raise ValueError("The ontology must be 1 or 2")
        
    def getLabelsOntology(self, ontology:int) -> list:
        if ontology == 1:
            return self.labels_o1
        elif ontology == 2:
            return self.labels_o2
        else:
            raise ValueError("The ontology must be 1 or 2")
        
    def getOntology(self, ontology:int) -> Ontology:
        if ontology == 1:
            return self.ontology1
        elif ontology == 2:
            return self.ontology2
        else:
            raise ValueError("The ontology must be 1 or 2")
        
    def define_lexical_function(self):
        if self.lexical_similarity == "Jaccard":
            self.func = jaccard_distance
        elif self.lexical_similarity == "Levenshtein":
            self.func = edit_distance
        elif self.lexical_similarity == "Binary":
            self.func = binary_distance
        elif self.lexical_similarity == "Masi":
            self.func = masi_distance
        elif self.lexical_similarity == "Jaro":
            self.func = jaro_similarity
        elif self.lexical_similarity == "Jaro-Winkler":
            self.func = jarowinkler_similarity
        else:
            raise ValueError("The lexical similarity must be Jaccard, Levenshtein, Binary, Masi, Jaro or Jaro-Winkler")
        
    def load_embeddings(self, set_labels: set):
        self.string_embedding = {}
        for label in set_labels:
            self.string_embedding[label] = self.llm.encode(label)
            
    def compute_embedding_similarity(self) -> dict:
        labels1 = self.labels_o1
        labels2 = self.labels_o2
        
        scores = {}
        for l1 in labels1:
            for l2 in labels2:
                embedding1 = self.string_embedding[l1]
                embedding2 = self.string_embedding[l2]
                scores[(l1, l2)] = util.cos_sim(embedding1, embedding2)[0][0].item()

        return scores
        
    def compute_lexical_similarity(self) -> dict:
        labels1 = self.labels_o1
        labels2 = self.labels_o2

        if self.lexical_similarity == "Jaccard" or self.lexical_similarity == "Masi":
            labels1 = list(map(lambda x: set(x.split()), labels1))
            labels2 = list(map(lambda x: set(x.split()), labels2))
 

        scores = {}
        for l1 in labels1:
            for l2 in labels2:
                str_l1 = " ".join(l1) if self.lexical_similarity in ["Jaccard", "Masi"] else l1
                str_l2 = " ".join(l2) if self.lexical_similarity in ["Jaccard", "Masi"] else l2
                scores[(str_l1, str_l2)] = self.func(l1, l2)

        return scores



    def startAlignment(self):
        # Here we can start the alignment process
        pass


# example
# ONTOLOGIES = os.getcwd() + "\\ontologies\\anatomy\\"
# oa = OntologyAlignmet(ONTOLOGIES + "human.owl", ONTOLOGIES + "mouse.owl")
# print(oa.getLabelsOntology(1))
# print(oa.getLabelsOntology(2))



# t1 = time.time()
# print(oa.compute_lexical_similarity("Jaccard"))
# print("Time: ", time.time() - t1)