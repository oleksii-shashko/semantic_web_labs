from rdflib import Graph


def total_amount(graph: Graph):
    sparql_res = graph.query("""
        SELECT (COUNT(*) as ?amount) WHERE {
        ?set dc:identifier ?id.
        }
    """)
    return list(sparql_res)[0][0]


def one_title(graph: Graph):
    sparql_res = graph.query("""
        SELECT ?vacancyTitle WHERE {
        ?vacancy dc:title ?vacancyTitle.
        } LIMIT 1
    """)
    return list(sparql_res)[0][0]


def all_complex_elements(graph: Graph):
    sparql_res = graph.query("""
        PREFIX my:<http://description.com/my_schema/>
        PREFIX type-v:<file:///D:/KNURE/Labs/SemanticWeb/lab5/>
        SELECT * WHERE {
        ?resource rdf:type type-v:MLEngineer.
        ?resource my:title ?title.
        }
    """)
    return sparql_res


def all_creators(graph: Graph):
    sparql_res = graph.query("""
        PREFIX my:<http://description.com/my_schema/>
        SELECT ?creator WHERE {
        ?vacancy my:creator ?creator.
        }
    """)
    return list(sparql_res)


def all_subclasses(graph: Graph):
    sparql_res = graph.query("""
        PREFIX my:<http://description.com/my_schema/>
        PREFIX type-c:<file:///D:/KNURE/Labs/SemanticWeb/lab5/dou_vacancies.rdf#>
        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?class WHERE {
        ?class rdfs:subClassOf type-c:VacancyList.
        }
    """)
    return list(sparql_res)


def amount_of_backends(graph: Graph):
    sparql_res = graph.query("""
        PREFIX my:<http://description.com/my_schema/>
        PREFIX type-v:<file:///D:/KNURE/Labs/SemanticWeb/lab5/>
        SELECT (COUNT(*) as ?amount) WHERE {
        ?vacancy rdf:type type-v:BackendEngineer.
        }
    """)
    return list(sparql_res)[0][0]


def ML_info(graph: Graph):
    sparql_res = graph.query("""
            PREFIX my:<http://description.com/my_schema/>
            PREFIX type-v:<file:///D:/KNURE/Labs/SemanticWeb/lab5/>
            SELECT ?title ?creator ?description WHERE {
            ?vacancy rdf:type type-v:MLEngineer.
            ?vacancy my:title ?title.
            ?vacancy my:creator ?creator.
            ?vacancy my:description ?description.
            }
        """)
    return list(sparql_res)


if __name__ == "__main__":
    graph1 = Graph()
    graph1.parse(source="D:\\KNURE\\Labs\\SemanticWeb\\lab4\\dou_vacancies.rdf", format='xml')
    graph2 = Graph()
    graph2.parse(source="D:\\KNURE\\Labs\\SemanticWeb\\lab5\\dou_vacancies.rdf", format='xml')

    print("====================================Task 1====================================")
    print(total_amount(graph1))

    print("====================================Task 2====================================")
    print(one_title(graph1))

    print("====================================Task 3====================================")
    for el in all_complex_elements(graph2):
        print(el[0])

    print("====================================Task 4====================================")
    for el in all_creators(graph2):
        print(el[0])

    print("====================================Task 5====================================")
    for el in all_subclasses(graph2):
        print(el[0])

    print("====================================Task 6====================================")
    print(amount_of_backends(graph2))

    print("====================================Task 7====================================")
    for el in ML_info(graph2):
        print("{}\n{}\n{}".format(el[0], el[1], el[2]))
        print("------------------------------------------------------------------------------")
