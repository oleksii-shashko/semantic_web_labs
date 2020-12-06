from rdflib import Namespace, BNode, Graph
from rdflib import URIRef, Literal
from rdflib import RDF

from lxml import etree as et


def create_rdf(xml_path: str):
    dom = et.parse(xml_path)
    root = dom.getroot()

    rdf_data = form_rdf(root)
    rdf_data.serialize(destination="dou_vacancies1.rdf", format="pretty-xml")


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

        g.add((vacancy_rdf, MY.identifier, Literal(vacancy.get("id"))))
        g.add((vacancy_rdf, MY.creator, Literal(company.text.strip())))
        g.add((vacancy_rdf, MY.title, Literal(name.text.strip())))
        g.add((vacancy_rdf, MY.description, Literal(info.text.replace("\n", "").strip())))
        g.add((vacancy_rdf, MY.subject, Literal("work")))
        g.add((vacancy_rdf, MY.publisher, Literal("jobs.dou.ua")))
        g.add((vacancy_rdf, MY["format"], Literal("text/html")))

        if "а" in info.text.strip()[:50]:
            lang = "ru/ua"
        else:
            lang = "en"

        g.add((vacancy_rdf, MY.language, Literal(lang)))

        cities_bag = BNode()
        g.add((cities_bag, RDF.type, RDF.Bag))

        for city in cities:
            g.add((cities_bag, RDF.li, Literal(city.text.strip())))

        g.add((vacancy_rdf, MY.cities, cities_bag))

    g.bind("rdf", RDF)
    g.bind("my", MY)

    return g


if __name__ == "__main__":
    XML_PATH = "dou_vacancies_1.xml"
    create_rdf(XML_PATH)
