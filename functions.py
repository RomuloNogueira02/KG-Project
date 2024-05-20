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
    raw_labels = list(map(lambda entity: (entity, normalize_string(entity.label[0]) if len(entity.label) > 0 else ""), ontology.classes()))
    filtered_labels = list(filter(lambda label: label[1] != "", raw_labels))
    return filtered_labels


def normalize_string(s):
    # Convert to lowercase
    s = s.lower()
    # Remove non-alphanumeric characters and spaces
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    # Remove extra spaces
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def convert_seconds(sec):
    sec = int(sec)
    minu = sec // 60
    sec_remaining = sec % 60
    return f"{minu:02d}:{sec_remaining:02d}"


def calculate_progress(current, total):
    if total == 0:
        return 100.0 if current == 0 else float('inf')
    else:
        return (current / total) * 100