from owlready2 import *
import os

def loadOntology(path: str) -> Ontology:
    print(path)
    if os.path.exists(path):
        return get_ontology(path).load()
    else:
        raise FileNotFoundError("The file does not exist")
    

def get_labels(ontology):
    # Get labels from ontology that are not empty
    raw_labels = list(map(lambda entity: entity.label[0] if len(entity.label) > 0 else "", ontology.classes()))
    filtered_labels = list(filter(lambda label: label != "", raw_labels))
    return filtered_labels