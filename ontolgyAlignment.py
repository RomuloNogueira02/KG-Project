from functions import *



# I think we should have a class for the ontology alignment, where executes all the pipeline.
# With this class we can personalize the pipeline, running different ways to align ontologies.

class OntologyAlignmet:

    def __init__(self, path_o1, path_o2, lexical_similarity= "Jaccard", LLM=True) -> None:
        
        self.ontology1 = loadOntology(path_o1)
        self.ontology2 = loadOntology(path_o2)

        self.labels_o1 = get_labels(self.ontology1)
        self.labels_o2 = get_labels(self.ontology2)

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


    def startAlignment(self):
        # Here we can start the alignment process
        pass


# example
# ONTOLOGIES = os.getcwd() + "\\ontologies\\anatomy\\"
# oa = OntologyAlignmet(ONTOLOGIES + "human.owl", ONTOLOGIES + "mouse.owl")
# print(oa.getLabelsOntology(1))