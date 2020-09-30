# Overview
JSON versions of schema.org schemas. Contains every single schema (except for primitive types) in JSON form in a neat folder structure following the schema structure. Also includes a python script which can be used to regenerate this in other formats. The base script is derived from [https://raw.githubusercontent.com/RDFLib/pyrdfa3/master/scripts/localRDFa.py]. Copyright © 2020 W3C® (MIT, ERCIM, Keio, Beihang). The JSON files are generated directly from the webpages of the schema.org site 

See LICENSE for the license each of these are licensed under.

The script needs to be run under python3 and needs pyRdfa3 (pip install pyRdfa3) If generating in JSON rdflib-jsonld (pip install rdflib-jsonld) is also needed.

I'm not affiliated with schema.org in any way, I just wanted this data, and it simply isn't available in bulk in this format elsewhere (at least I couldn't find it). FYI, despite the amount of files, it is only 47MB 