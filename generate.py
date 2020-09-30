#!/usr/bin/env python3
"""
This software is derived from [https://raw.githubusercontent.com/RDFLib/pyrdfa3/master/scripts/localRDFa.py].
Copyright © 2020 W3C® (MIT, ERCIM, Keio, Beihang). 
It generates files for all schema.org schemas instead of just one file, but the args stuff is original
"""

import sys, getopt, platform, logging, json, os
from pyRdfa                        import pyRdfa
from pyRdfa.transform.metaname     import meta_transform
from pyRdfa.transform.OpenID       import OpenID_transform
from pyRdfa.transform.DublinCore   import DC_transform
from pyRdfa.options                import Options
from time                          import sleep

###########################################

usageText="""Usage: %s -[vjxtnpzsb:g:ryle]
where:
  -x: output format RDF/XML
  -t: output format Turtle (default)
  -j: output format JSON-LD
  -n: output format N Triples
  -p: output format pretty RDF/XML
  -z: exceptions should be returned as graphs instead of exceptions raised
  -b: give the base URI; if a file name is given, this can be left empty and the file name is used
  -s: whitespace on plain literals are not preserved (default: preserved, per RDFa syntax document); this is a non-standard feture
  -l: run in RDFa 1.1 Lite mode (non-RDFa Lite generate warnings) (default: False)
  -r: report on the details of the vocabulary caching process
  -y: bypass the vocabulary cache checking, generate a new cache every time (good for debugging) (default:False)
  -v: perform vocabulary expansion (default: False)
  -g: value can be 'output', 'processor', 'output,processor' or 'processor,output'; controls which graphs are returned
  -e: embedded (in a <script> element) Turtle content or RDF/XML (in its own namespace) _not_ parsed and added to the output graph (default:True, i.e., parsed)
  -w: value is a filename, to be used instead of the default standard error for logging errors, warnings, etc.

The -g option may be unnecessary, the script tries to make a guess based on a default xmlns value for XHTML or SVG.
"""

def usage() :
    print(usageText % sys.argv[0])

fileFormat             = "turtle"
extras                 = []
value                  = ""
space_preserve         = True
base                   = ""
value                  = []
rdfOutput              = False
output_default_graph   = True
output_processor_graph = True
vocab_cache_report     = False
refresh_vocab_cache    = False
vocab_expansion        = False
vocab_cache            = True
embedded_rdf           = True
check_lite             = False
log                    = None

try :
    opts, value = getopt.getopt(sys.argv[1:],"vxetjnpzsb:g:rylw:",['graph='])
    for o,a in opts:
        if o == "-t" :
            fileFormat= "turtle"
        elif o == "-n" :
            fileFormat= "nt"
        elif o == "-j" :
            fileFormat= "json-ld"
        elif o == "-p" or o == "-x":
            fileFormat= "pretty-xml"
        elif o == "-z" :
            rdfOutput = True
        elif o == "-b" :
            base = a
        elif o == "-e" :
            embedded_rdf = False
        elif o == "-s" :
            space_preserve = False
        elif o == "-l" :
            check_lite = True
        elif o == "-r" :
            vocab_cache_report = True
        elif o == "-v" :
            vocab_expansion = True
        elif o == "-y" :
            bypass_vocab_cache = True
        elif o in ("-g", "--graph") :
            if a == "processor" :
                output_default_graph     = False
                output_processor_graph     = True
            elif a == "processor,default" or a == "default,processor" :
                output_processor_graph     = True
            elif a == "default" :
                output_default_graph     = True
                output_processor_graph     = False
        elif o == "-w" :
            log = a
        else :
            usage()
            sys.exit(1)
except :
    usage()
    sys.exit(1)

if log is not None :
    logging.basicConfig(filename=log)
else :
    logging.basicConfig()

options = Options(output_default_graph = output_default_graph,
                  output_processor_graph = output_processor_graph,
                  space_preserve=space_preserve,
                  transformers = extras,
                  embedded_rdf = embedded_rdf,
                  vocab_expansion = vocab_expansion,
                  vocab_cache = vocab_cache,
                  vocab_cache_report = vocab_cache_report,
                  refresh_vocab_cache = refresh_vocab_cache,
                  check_lite = check_lite,
                  experimental_features = True,
)

schemas = json.load(open("tree.jsonld"))
rootDir = os.getcwd() + "\\Thing_children"

def schemaProcessor(schema):
    """
    Is intended to be initially fed with the contents of tree.jsonld in dict form. Will 
    then recursively iterate through children of the root object, and their children, creating 
    a nice neat folder structure, until it runs out out of things to iterate over.
    Args:
        schema (dict): A dict containing a "name" property and possibly a "children" property
    """
    print(schema["name"])
    # Being nice and safe
    sleep(2)
    try:
        processor = pyRdfa(options, base)
        # Parse into JSON/other file and write to file
        with open(schema["name"] + ".jsonld", 'w', encoding="utf-8") as f:
            f.write(processor.rdf_from_sources(["https://schema.org/" + schema["name"]], outputFormat = fileFormat, rdfOutput = rdfOutput).decode("utf-8"))
    except Exception as e:
        print('Error while processing ' + schema["name"])
        print(e)
        exit(1)
    if schema.get("children"):
        topDir = os.getcwd()
        # Make dir to hold children of schema
        os.mkdir(schema["name"] + "_children")
        os.chdir(schema["name"] + "_children")
        # Generate files for every child
        for i in schema["children"]:
            try:
                schemaProcessor(i)
            except Exception as e:
                print('Error while processing '+ schema["name"] + " child " + i)
                exit(1)
        # Back to parent folder
        os.chdir(topDir)
schemaProcessor(schemas)
