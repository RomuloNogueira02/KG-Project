from functions import *
import time

# I think we should have a class for the ontology alignment, where executes all the pipeline.
# With this class we can personalize the pipeline, running different ways to align ontologies.

class OntologyAlignment:

    def __init__(self, path_o1, path_o2, lexical_similarity= "Jaccard", LLM=True) -> None:
        
        self.ontology1 = loadOntology(path_o1)
        self.ontology2 = loadOntology(path_o2)

        self.labels_o1 = get_labels(self.ontology1)
        self.labels_o2 = get_labels(self.ontology2)

        self.lexical_similarity = lexical_similarity

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
        
    def compute_lexical_similarity(self) -> dict:
        labels1, labels2 = normalize_labels(self.labels_o1, self.lexical_similarity), normalize_labels(self.labels_o2, self.lexical_similarity)
        func = jaccard_similarity 
        if self.lexical_similarity == "Levenshtein":
            func = levenshtein_similarity
        elif self.lexical_similarity == "Cosine":
            pass

        # print(labels1)

        scores = {}
        for l1 in labels1:
            for l2 in labels2:
                str_l1 = " ".join(l1) if self.lexical_similarity == "Jaccard" else l1
                str_l2 = " ".join(l2) if self.lexical_similarity == "Jaccard" else l2
                scores[(str_l1, str_l2)] = func(l1, l2)

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