from owlready2 import *
import os
import re
import Levenshtein

def loadOntology(path: str) -> Ontology:
    # print(path)
    if os.path.exists(path):
        return get_ontology(path).load()
    else:
        raise FileNotFoundError("The file does not exist")
    

def get_labels(ontology):
    # Get labels from ontology that are not empty
    raw_labels = list(map(lambda entity: entity.label[0] if len(entity.label) > 0 else "", ontology.classes()))
    filtered_labels = list(filter(lambda label: label != "", raw_labels))
    return filtered_labels

def normalize_labels(label: list, method) -> list:
    if method == "Jaccard":
        return list(map(lambda l: set(normalize_string(l).split()), label))
    elif method == "Levenshtein":
        return list(map(lambda l: normalize_string(l), label))
    elif method == "Cosine":
        # Not implmented yet
        return []

def normalize_string(s):
    # Convert to lowercase
    s = s.lower()
    # Remove non-alphanumeric characters and spaces
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    # Remove extra spaces
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0.0

def levenshtein_similarity(labels1, labels2):
    return Levenshtein.distance(labels1, labels2)