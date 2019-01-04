#!/usr/bin/python3
import argparse
import json
import cbor
from xml.dom.minidom import parseString

import dicttoxml
import yaml
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

parser = argparse.ArgumentParser(description='Process PGDL documents.')
parser.add_argument('file', type=str,
                    help='a PGDL file')
parser.add_argument("-m", "--metadata", help="display PGDL metadata",
                    action="store_true")
parser.add_argument("-j", "--json", help="display PGDL in JSON",
                    action="store_true")
parser.add_argument("-pj", "--prettyjson", help="display PGDL in pretty JSON",
                    action="store_true")
parser.add_argument("-c", "--cbor", help="display PGDL in CBOR (binary JSON)",
                    action="store_true")
parser.add_argument("-x", "--xml", help="display PDGL in XML",
                    action="store_true")
parser.add_argument("-px", "--prettyxml", help="display PDGL in XML",
                    action="store_true")
parser.add_argument("-y", "--yaml", help="display PDGL in compact YAML",
                    action="store_true")
parser.add_argument("-py", "--prettyyaml", help="display PDGL in compact YAML",
                    action="store_true")
parser.add_argument("-p", "--pgdl", help="display PDGL (in YAML)",
                    action="store_true")
parser.add_argument("-s", "--shacl", help="display (PG)SHACL (in RDF)",
                    action="store_true")

args = parser.parse_args()

if args.file:
    with open(args.file, 'r') as stream:
        try:
            data = yaml.load(stream)
            with open(args.file, 'r') as s:
                raw = s.read()
        except yaml.YAMLError as exc:
            print(exc)
            exit()

    if args.metadata:
        try:
            print('PGDL domument data creation: ' + data['metadata']['created'])
        except:
            print('There are not any information about PGDL data creation')
        try:
            print('Document is created by ' + data['metadata']['creator'])
        except:
            print('There are not any information about PGDL creator')
        exit()
        print(data['shapes'][0]['targetNode'])

    if args.json:
        json = json.dumps(data)
        print(json)
    if args.cbor:
        cbor = cbor.dumps(data)
        print(cbor)
    if args.prettyjson:
        json = json.dumps(data, indent=2, sort_keys=True)
        print(json)
    if args.xml:
        xml = dicttoxml.dicttoxml(data, attr_type=False, custom_root='pgdl')
        print(xml.decode("utf-8"))
    if args.prettyxml:
        xml = dicttoxml.dicttoxml(data, attr_type=False, custom_root='pgdl')
        x = xml.decode("utf-8")
        dom = parseString(x)
        print(dom.toprettyxml())
    if args.yaml:
        print(yaml.dump(data))
    if args.pgdl:
        print(raw)
    if args.shacl:
        print('# This option is not fully supported')
        g = Graph()
        doc = BNode()
        dct = Namespace("http://purl.org/dc/terms/")
        sh = Namespace("http://www.w3.org/ns/shacl#")
        pg = Namespace("urn:pg:1.0:")
        xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
        pgsh = Namespace("http://ii.uwb.edu.pl/shpg#")
        try:
            created = data['metadata']['created']
            g.add((doc, dct.created, Literal(created, datatype=xsd.date)))
        except:
            print('# There is no information about date of creation')
        try:
            creator = data['metadata']['creator']
            g.add((doc, dct.creator, Literal(creator)))
        except:
            print('# There is no information about creator')

        for shape in data.get('shapes', []):
            tn1 = shape.get('targetNode', [])
            g.add((pg.Shape1, RDF.type, sh.NodeShape))
            g.add((pg.Shape1, sh.targetNode, URIRef("urn:pg:1.0:" + tn1)))

            for property in shape.get('properties', []):
                pn1 = property.get('name', [])
                prop = BNode()
                g.add((pg.Shape1, sh.property, prop))
                g.add((prop, sh.path, URIRef("urn:pg:1.0:" + pn1)))
                pdt1 = property.get('datatype', [])

                if pdt1 == 'string':
                    pdt1 = xsd.string
                elif pdt1 == 'int':
                    pdt1 = xsd.int
                g.add((prop, sh.datatype, pdt1))

            for edge in shape.get('edges', []):
                pp1 = edge.get('name', [])
                prop2 = BNode()
                g.add((pg.Shape1, sh.property, prop2))
                g.add((prop2, sh.path, URIRef("urn:pg:1.0:" + pp1)))
                pnd1 = edge.get('node', [])
                g.add((prop2, sh.node, URIRef("urn:pg:1.0:" + pnd1)))

                rel = BNode()
                g.add((prop2, pgsh.relation, rel))

                for relation in edge.get('relations', []):
                    nky1 = relation.get('name', [])
                    g.add((rel, pgsh.key, URIRef("urn:pg:1.0:" + nky1)))
                    rdt1 = relation.get('datatype', [])
                    if rdt1 == 'string':
                        rdt1 = xsd.string
                    elif pdt1 == 'int':
                        rdt1 = xsd.int
                    g.add((rel, sh.datatype, rdt1))

        print(g.serialize(format='turtle').decode("utf-8"))