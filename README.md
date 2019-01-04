# PGDL-conv

Property Graph Definition Language converter for many other formats including [JSON](https://www.json.org/), [CBOR](http://cbor.io/) (binary JSON), [XML](https://www.w3.org/XML/), [YAML](https://yaml.org/) and (PG)[SHACL](https://www.w3.org/TR/shacl/). Written in [Python](https://www.python.org/) 3. Works from CLI.

## Usage

```shell
pgdl-conv.py [-h] [-m] [-j] [-pj] [-c] [-x] [-px] [-y] [-p] [-s] file
```

### Positional arguments

```shell
  file               a PGDL file
```

### Optional arguments

```shell
  -h, --help         show this help message and exit
  -m, --metadata     display PGDL metadata
  -j, --json         display PGDL in JSON
  -pj, --prettyjson  display PGDL in pretty JSON
  -c, --cbor         display PGDL in CBOR (binary JSON)
  -x, --xml          display PDGL in XML
  -px, --prettyxml   display PDGL in pretty XML
  -y, --yaml         display PDGL in compact YAML
  -p, --pgdl         display PDGL (in YAML)
  -s, --shacl        display (PG)SHACL (in RDF)
```

Available options may vary depending on the version. To display all available options with their descriptions use ``pgdl-conv.py -h``.

## Contribution

Would you like to improve this project? Great! We are waiting for your help and suggestions. If you are new in open source contributions, read [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/).

## License

Distributed under [MIT license](https://github.com/domel/PGDL-conv/blob/master/LICENSE).