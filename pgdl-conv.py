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

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-m", "--metadata", help="display PGDL metadata",
                    action="store_true")
group.add_argument("-j", "--json", help="display PGDL in JSON",
                    action="store_true")
group.add_argument("-pj", "--prettyjson", help="display PGDL in pretty JSON",
                    action="store_true")
group.add_argument("-c", "--cbor", help="display PGDL in CBOR (binary JSON)",
                    action="store_true")
group.add_argument("-x", "--xml", help="display PDGL in XML",
                    action="store_true")
group.add_argument("-px", "--prettyxml", help="display PDGL in pretty XML",
                    action="store_true")
group.add_argument("-t", "--toml", help="display TOML",
                    action="store_true")
group.add_argument("-y", "--yaml", help="display PDGL in compact YAML",
                    action="store_true")
# parser.add_argument("-py", "--prettyyaml", help="display PDGL in compact YAML",
#                     action="store_true")
group.add_argument("-p", "--pgdl", help="display PDGL (in YAML)",
                    action="store_true")
group.add_argument("-g", "--graphql", help="display GraphQL",
                    action="store_true")
group.add_argument("-s", "--shacl", help="display (PG)SHACL (in RDF)",
                    action="store_true")

args = parser.parse_args()

if args.file:
    with open(args.file, 'r') as stream:
        try:
            data = yaml.load(stream, Loader=yaml.SafeLoader)
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
        g.bind("shpg", pgsh)

        def set_datatype(f):
            return {
                'string': xsd.string,
                'int': xsd.int,
                'integer': xsd.integer,
                'boolean': xsd.boolean,
                'decimal': xsd.decimal,
                'float': xsd.float,
                'double': xsd.double,
                'dateTime': xsd.dateTime,
                'time': xsd.time,
                'date': xsd.date,
            }.get(f)

        try:
            created = data['metadata']['created']
            g.add((doc, dct.created, Literal(created, datatype=xsd.date)))
        except KeyError:
            print('# There is no information about date of creation')

        try:
            creator = data['metadata']['creator']
            g.add((doc, dct.creator, Literal(creator)))
        except KeyError:
            print('# There is no information about creator')

        shape_counter = 1
        for shape in data.get('shapes', []):
            shape_id = f"Shape{shape_counter}"
            shape_counter += 1
            try:
                tn1 = shape['targetNode']
                shape_ref = URIRef(f"urn:pg:1.0:{shape_id}")
                g.add((shape_ref, RDF.type, sh.NodeShape))
                g.add((shape_ref, sh.targetNode, URIRef("urn:pg:1.0:" + tn1)))
            except KeyError:
                print('# There is no information about target node')

            for property in shape.get('properties', []):
                prop = BNode()
                try:
                    pn1 = property['name']
                    g.add((shape_ref, sh.property, prop))
                    g.add((prop, sh.path, URIRef("urn:pg:1.0:" + pn1)))
                    pdt1 = set_datatype(property.get('datatype'))
                    if pdt1:
                        g.add((prop, sh.datatype, pdt1))
                except KeyError as e:
                    print(f'# There is no information about property: {e}')

            for edge in shape.get('edges', []):
                prop2 = BNode()
                try:
                    pp1 = edge['name']
                    g.add((shape_ref, sh.property, prop2))
                    g.add((prop2, sh.path, URIRef("urn:pg:1.0:" + pp1)))
                    pnd1 = edge['node']
                    g.add((prop2, sh.node, URIRef("urn:pg:1.0:" + pnd1)))

                    rel = BNode()
                    g.add((prop2, pgsh.relation, rel))

                    for relation in edge.get('relations', []):
                        nky1 = relation['name']
                        g.add((rel, pgsh.key, URIRef("urn:pg:1.0:" + nky1)))
                        rdt1 = set_datatype(relation.get('datatype'))
                        if rdt1:
                            g.add((rel, sh.datatype, rdt1))
                except KeyError as e:
                    print(f'# There is no information about edge or relation: {e}')

        print(g.serialize(format='turtle'))
        
else:
    parser.print_help()
