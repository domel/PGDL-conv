#!/usr/bin/python3
import argparse
import json
import cbor
from xml.dom.minidom import parseString
import qtoml

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
parser.add_argument("-px", "--prettyxml", help="display PDGL in pretty XML",
                    action="store_true")
parser.add_argument("-t", "--toml", help="display TOML",
                    action="store_true")
parser.add_argument("-y", "--yaml", help="display PDGL in compact YAML",
                    action="store_true")
# parser.add_argument("-py", "--prettyyaml", help="display PDGL in compact YAML",
#                     action="store_true")
parser.add_argument("-p", "--pgdl", help="display PDGL (in YAML)",
                    action="store_true")
parser.add_argument("-g", "--graphql", help="display GraphQL",
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
    if args.toml:
        toml = qtoml.dumps(data)
        print(toml)
    if args.yaml:
        print(yaml.dump(data))
    if args.pgdl:
        print(raw)
    if args.graphql:
        indentation = '  '

        def set_datatype(f):
            if f == 'string':
                return 'String'
            elif f == 'int':
                return 'Int'
            elif f == 'integer':
                return 'Int'
            elif f == 'boolean':
                return 'Boolean'
            elif f == 'decimal':
                return 'Float'
            elif f == 'float':
                return 'Float'
            elif f == 'double':
                return 'Float'
            elif f == 'dateTime':
                return 'String'
            elif f == 'time':
                return 'String'
            elif f == 'date':
                return 'String'


        def print_edge_details(pnd, direction):
            if edge_directed:
                print(indentation + pnd.lower() + 's: [' + pnd + '] @relation(name:\"' +
                      pp1 + '\",direction:' + direction + ')')
            else:
                print(indentation + pnd.lower() + 's: [' + pnd + '] @relation(name:\"' + pp1 + ')')


        def print_relation_details():
            print(indentation + '@property(name:' + '\"' + nky1 + '\",datatype:\"' + rdt1 + '\")')


        for shape in data.get('shapes', []):
            try:
                tn1 = shape['targetNode']
                print('type ' + tn1 + ' {')
            except:
                print('# There is no information about target node')

            for property in shape.get('properties', []):
                try:
                    pn1 = property['name']
                    pdt1 = property['datatype']
                    pdt1 = set_datatype(pdt1)
                    print(indentation + pn1 + ': ' + pdt1 + '!')
                except:
                    print(indentation + '# There is no information about property name or data type')

            try:
                for edge in shape['edges']:
                    try:
                        edge_directed = edge['directed']
                    except:
                        edge_directed = None
                        print(indentation + '# There is no information about edge direction')

                    try:
                        pp1 = edge['name']
                    except:
                        print(indentation + '# There is no information about edge name')

                    try:
                        pnd1 = edge['node']
                    except:
                        print(indentation + '# There is no information about edge node')

                    try:
                        print_edge_details(pnd1, 'OUT')
                    except:
                        print(indentation + '# Error while printing edge details')

                    for relation in edge.get('relations', []):
                        try:
                            nky1 = relation['name']
                        except:
                            print(indentation + '# There is no information about relation name')

                        try:
                            rdt1 = relation['datatype']
                            rdt1 = set_datatype(rdt1)
                            print_relation_details()
                        except:
                            print(indentation + '# There is no information about relation datatype')
            except:
                # print(indentation + '# There is no information about edge.')
                try:
                    for sh in data.get('shapes', []):
                        if sh['targetNode'] == pnd1:
                            # TODO
                            print_edge_details('Person', 'IN')
                            print_relation_details()
                except:
                    print(indentation + '# Failed to add edge & relationship information')

            print('}\n')

    if args.shacl:
        g = Graph()
        doc = BNode()
        dct = Namespace("http://purl.org/dc/terms/")
        sh = Namespace("http://www.w3.org/ns/shacl#")
        pg = Namespace("urn:pg:1.0:")
        xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
        pgsh = Namespace("http://ii.uwb.edu.pl/shpg#")


        def set_datatype(f):
            if f == 'string':
                return xsd.string
            elif f == 'int':
                return xsd.int
            elif f == 'integer':
                return xsd.integer
            elif f == 'boolean':
                return xsd.boolean
            elif f == 'decimal':
                return xsd.decimal
            elif f == 'float':
                return xsd.float
            elif f == 'double':
                return xsd.double
            elif f == 'dateTime':
                return xsd.dateTime
            elif f == 'time':
                return xsd.time
            elif f == 'date':
                return xsd.date


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
            try:
                tn1 = shape['targetNode']
                g.add((pg.Shape1, RDF.type, sh.NodeShape))
                g.add((pg.Shape1, sh.targetNode, URIRef("urn:pg:1.0:" + tn1)))
            except:
                print('# There is no information about target node')

            for property in shape.get('properties', []):
                try:
                    pn1 = property['name']
                    prop = BNode()
                    g.add((pg.Shape1, sh.property, prop))
                    g.add((prop, sh.path, URIRef("urn:pg:1.0:" + pn1)))
                except:
                    print('# There is no information about property name')

                try:
                    pdt1 = property['datatype']
                    pdt1 = set_datatype(pdt1)
                    g.add((prop, sh.datatype, pdt1))
                except:
                    print('# There is no information about property data type')

            for edge in shape.get('edges', []):
                try:
                    pp1 = edge['name']
                    prop2 = BNode()
                    g.add((pg.Shape1, sh.property, prop2))
                    g.add((prop2, sh.path, URIRef("urn:pg:1.0:" + pp1)))
                except:
                    print('# There is no information about edge name')

                try:
                    pnd1 = edge['node']
                    g.add((prop2, sh.node, URIRef("urn:pg:1.0:" + pnd1)))
                except:
                    print('# There is no information about edge node')

                rel = BNode()

                try:
                    g.add((prop2, pgsh.relation, rel))
                except:
                    print('# No relation')

                for relation in edge.get('relations', []):
                    try:
                        nky1 = relation['name']
                        g.add((rel, pgsh.key, URIRef("urn:pg:1.0:" + nky1)))
                    except:
                        print('# There is no information about relation name')

                    try:
                        rdt1 = relation['datatype']
                        rdt1 = set_datatype(rdt1)
                        g.add((rel, sh.datatype, rdt1))
                    except:
                        print('# There is no information about relation datatype')

        print(g.serialize(format='turtle').decode("utf-8"))
        
    else:
        parser.print_help()
