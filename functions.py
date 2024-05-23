from owlready2 import *
import os
import re
import pandas as pd
import xml.etree.ElementTree as ET


def loadOntology(path: str) -> Ontology:
    # print(path)
    if os.path.exists(path):
        return get_ontology(path).load()
    else:
        raise FileNotFoundError("The file does not exist")
    

def calculate_entity(base, entity):
    entity = entity.split(".")[1]
    return base + entity


def get_labels(base, ontology):
    # Get labels from ontology that are not empty
    raw_labels = list(map(lambda entity: (calculate_entity(base, str(entity)), normalize_string(entity.label[0]) if len(entity.label) > 0 else ""), ontology.classes()))
    filtered_labels = list(filter(lambda label: label[1] != "", raw_labels))
    return filtered_labels

def get_syns(base, ontology):
    raw_syns = []
    for e in ontology.classes():
        entity = calculate_entity(base, str(e))
        try:
            for syn in e.hasRelatedSynonym:
                raw_syns.append((entity, normalize_string(syn.label[0])))
        except:
            pass

    filtered_syns = list(filter(lambda label: label[1] != "", raw_syns))
    return filtered_syns


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
    

def create_XML_file(alignment_df, output_path):

    # Create the root element
    rdf = ET.Element('rdf:RDF', {
        'xmlns': "http://knowledgeweb.semanticweb.org/heterogeneity/alignment",
        'xmlns:rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        'xmlns:xsd': "http://www.w3.org/2001/XMLSchema#"
    })


    # Create the Alignment element
    alignment = ET.SubElement(rdf, 'Alignment')

    # Add xml, level, and type elements
    ET.SubElement(alignment, 'xml').text = 'yes'
    ET.SubElement(alignment, 'level').text = '0'
    ET.SubElement(alignment, 'type').text = '??'


    for _, row in alignment_df.iterrows():
        map_element = ET.SubElement(alignment, 'map')
        cell = ET.SubElement(map_element, 'Cell')
        ET.SubElement(cell, 'entity1', {'rdf:resource': row['uri_o1']})
        ET.SubElement(cell, 'entity2', {'rdf:resource': row['uri_o2']})
        ET.SubElement(cell, 'measure', {'rdf:datatype': 'xsd:float'}).text = str(row['score'])
        ET.SubElement(cell, 'relation').text = '='

    # Create an ElementTree object from the root element
    tree = ET.ElementTree(rdf)

    tree.write(output_path + '/output.rdf', encoding='utf-8', xml_declaration=True)