# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1njLGFxvdGgWkkJhXyPx2J58GP4sp1B0O

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

namespace = Namespace("http://somewhere#")
living_thing_class = namespace.LivingThing

query = f"""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?subclass
WHERE {{
    ?subclass rdfs:subClassOf <{living_thing_class}> .
}}
"""
print("Subclasses of LivingThing:")
for r in g.query(query):
    print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

namespace = Namespace("http://somewhere#")
person_class = namespace.Person

query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?individual
WHERE {{
    {{
        ?individual a <{person_class}> .
    }}
    UNION
    {{
        ?individual a ?subclass .
        ?subclass rdfs:subClassOf <{person_class}> .
    }}
}}
"""
print("Individuals of Person:")
for r in g.query(query):
    print(r.individual)

"""**TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**

"""

animal_class = namespace.Animal

query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?individual
WHERE {{
    {{
        ?individual a <{person_class}> .
    }}
    UNION
    {{
        ?individual a <{animal_class}> .
    }}
}}
"""
print("Individuals of Person or Animal:")
for r in g.query(query):
    print(r.individual)

"""**TASK 7.4 :  List the name of the persons who know Rocky (in SPARQL only)**"""

rocky = namespace.Rocky
query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://somewhere#>

SELECT ?personName
WHERE {{
    ?person a ns:Person .
    ?person ns:knows ns:Rocky .
    ?person ns:name ?personName .
}}
"""
print("Persons who know Rocky:")
results = g.query(query)

if results:
    for r in results:
        print(r.personName)
else:
    print("No results found.")

"""**Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**"""

query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://somewhere#>

SELECT ?animalName
WHERE {{
    ?animal a ns:Animal .
    ?animal ns:knows ?otherAnimal .
    ?otherAnimal a ns:Animal .
    ?animal ns:name ?animalName .
}}
"""

print("Animals who know at least another animal:")
results = g.query(query)

# Check if there are results
if results:
    for r in results:
        print(r.animalName)  # Accessing the 'animalName' directly
else:
    print("No results found.")

"""**Task 7.6: List the age of all living things in descending order (in SPARQL only)**"""

query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://somewhere#>

SELECT ?livingThing ?age
WHERE {
    ?livingThing a ns:LivingThing .
    ?livingThing ns:age ?age .
}
ORDER BY DESC(?age)
"""
print("Ages of all living things in descending order:")
results = g.query(query)


if results:
    for r in results:
        print(f"{r.livingThing}: {r.age}")
else:
    print("No results found.")