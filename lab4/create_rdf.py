from rdflib import Namespace, BNode, Graph
from rdflib import URIRef, Literal
from rdflib import RDF, DC

from lxml import etree as et
import pandas as pd


def create_rdf(xml_path: str):
    dom = et.parse(xml_path)
    root = dom.getroot()

    rdf_data = form_rdf(root)
    rdf_data.serialize(destination="dou_vacancies.rdf", format="pretty-xml")
    sql_res = rdf_data.query("""
        SELECT * WHERE {
        ?vacancy dc:creator ?companyName.
        ?vacancy dc:title ?vacancyName.
        ?vacancy dc:language ?language.
        FILTER(?language='en')
        }
    """)
    df = pd.DataFrame(data=[(str(el) for el in row) for row in sql_res])
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_colwidth", None)
    print(df)

    sql_res = rdf_data.query("""
        SELECT (COUNT(*) as ?amount) WHERE {
        ?set dc:identifier ?id.
        }
    """)
    for el in sql_res:
        print(el[0])


def form_rdf(root: et.Element):
    g = Graph()
    MY = Namespace("http://description.com/my_schema/")

    for vacancy in root:
        name = vacancy[0]
        company = vacancy[1]
        cities = vacancy[2]
        info = vacancy[3]
        job_url = vacancy[4]
        vacancy_rdf = URIRef(job_url.text.strip())

        g.add((vacancy_rdf, DC.identifier, Literal(vacancy.get("id"))))
        g.add((vacancy_rdf, DC.creator, Literal(company.text.strip())))
        g.add((vacancy_rdf, DC.title, Literal(name.text.strip())))
        g.add((vacancy_rdf, DC.description,Literal(info.text.replace("\n", "").strip())))
        g.add((vacancy_rdf, DC.subject, Literal("work")))
        g.add((vacancy_rdf, DC.publisher, Literal("jobs.dou.ua")))
        g.add((vacancy_rdf, DC["format"], Literal("text/html")))

        if "а" in info.text.strip()[:50]:
            lang = "ru/ua"
        else:
            lang = "en"

        g.add((vacancy_rdf, DC.language, Literal(lang)))

        cities_bag = BNode()
        g.add((cities_bag, RDF.type, RDF.Bag))

        for city in cities:
            g.add((cities_bag, RDF.li, Literal(city.text.strip())))

        g.add((vacancy_rdf, MY.cities, cities_bag))

    g.bind("dc", DC)
    g.bind("rdf", RDF)
    g.bind("my", MY)

    return g


if __name__ == "__main__":
    XML_PATH = "dou_vacancies_1.xml"
    create_rdf(XML_PATH)
