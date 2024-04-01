import rdflib
from rdflib.namespace import RDF, Namespace
import yaml
import argparse

# Define namespaces
SH = Namespace("http://www.w3.org/ns/shacl#")
SHPG = Namespace("http://ii.uwb.edu.pl/shpg#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

def get_last_segment(uri):
    """
    Extracts the last segment from a URI.
    """
    return uri.split('/')[-1].split('#')[-1].split(':')[-1]

def parse_shacl(graph):
    metadata = {}
    shapes = []

    # Extract metadata
    for term in ['title', 'creator', 'subject', 'description', 'publisher', 'contributor', 'date', 'type', 'format', 'identifier', 'source', 'language', 'relation', 'coverage', 'rights']:
        for s, p, o in graph.triples((None, DCTERMS[term], None)):
            if term not in metadata:
                metadata[term] = []
            metadata[term].append(str(o))

    for date_term in ['created', 'issued', 'modified']:
        for s, p, o in graph.triples((None, DCTERMS[date_term], None)):
            if date_term not in metadata:
                metadata[date_term] = []
            metadata[date_term].append(str(o))

    for term in ['label', 'comment', 'seeAlso', 'isDefinedBy']:
        for s, p, o in graph.triples((None, RDFS[term], None)):
            if term not in metadata:
                metadata[term] = []
            metadata[term].append(str(o))

    for term in ['versionInfo', 'priorVersion', 'backwardCompatibleWith', 'incompatibleWith']:
        for s, p, o in graph.triples((None, OWL[term], None)):
            if term not in metadata:
                metadata[term] = []
            metadata[term].append(str(o))

    for term in ['altLabel', 'changeNote', 'definition', 'editorialNote', 'example', 'hiddenLabel', 'historyNote', 'note', 'prefLabel', 'scopeNote']:
        for s, p, o in graph.triples((None, SKOS[term], None)):
            if term not in metadata:
                metadata[term] = []
            metadata[term].append(str(o))

    for term, values in metadata.items():
        if len(values) == 1:
            metadata[term] = values[0]

    # Extract shapes
    for shape in graph.subjects(RDF.type, SH.NodeShape):
        shape_dict = {'targetClass': get_last_segment(str(graph.value(shape, SH.targetClass)))}
        properties = []
        edges = []

        for prop in graph.objects(shape, SH.property):
            prop_dict = {}
            path = graph.value(prop, SH.path)
            if path:
                prop_dict['name'] = get_last_segment(str(path))
                datatype = graph.value(prop, SH.datatype)
                if datatype:
                    prop_dict['datatype'] = get_last_segment(str(datatype))
                properties.append(prop_dict)

            relation = graph.value(prop, SHPG.relation)
            if relation:
                edge_dict = {'name': get_last_segment(str(path)), 'node': get_last_segment(str(graph.value(prop, SH.node)))}
                key = graph.value(relation, SHPG.key)
                if key:
                    edge_dict['relations'] = [{'name': get_last_segment(str(key)), 'datatype': get_last_segment(str(graph.value(relation, SH.datatype)))}]
                edges.append(edge_dict)

        if properties:
            shape_dict['properties'] = properties
        if edges:
            shape_dict['edges'] = edges
        shapes.append(shape_dict)

    return {'metadata': metadata, 'shapes': shapes}

def shacl_to_yaml(input_shacl_file):
    g = rdflib.Graph()
    with open(input_shacl_file, 'r') as file:
        g.parse(file, format="turtle")

    parsed_data = parse_shacl(g)
    return yaml.dump(parsed_data, sort_keys=False, allow_unicode=True)

def main():
    parser = argparse.ArgumentParser(description="Convert SHACL to YAML.")
    parser.add_argument('input_shacl_file', type=str, help="Path to the input SHACL file.")
    
    args = parser.parse_args()

    yaml_output = shacl_to_yaml(args.input_shacl_file)
    print(yaml_output)

if __name__ == "__main__":
    main()

