from owlready2 import *

DICT = {
    SOME: "some",
    EXACTLY: "exactly",
    MIN: "min",
    MAX: "max",
    ONLY: "only"
}
onto = get_ontology("vo-rdf.owl").load()


def check_consistency(ontology: Ontology):
    with ontology:
        sync_reasoner_hermit()
        if len(list(ontology.inconsistent_classes())) == 0:
            return True
        else:
            return False


def get_class(ontology: Ontology, name: str):
    for cl in ontology.classes():
        if cl.name == name:
            return cl


def get_property(ontology: Ontology, name: str):
    for property in ontology.properties():
        if property.name == name:
            return property


def get_individuals(ontology: Ontology, name: str):
    for indiv in ontology.individuals():
        if indiv.name == name:
            return indiv


class MarketingKnowledge(Thing):
    namespace = onto


class requireMarketingKnowledge(get_property(onto, "requireKnowledge")):
    namespace = onto
    domain = [get_class(onto, "Vacancy")]
    range = [onto.MarketingKnowledge]


class hasRating(DataProperty, FunctionalProperty):
    namespace = onto
    domain = [get_class(onto, "Company")]
    range = [float]


class hasCompiler(DataProperty, FunctionalProperty):
    namespace = onto
    domain = [get_class(onto, "Programming_Language")]
    range = [bool]


class SalesManagerVacancy(get_class(onto, "Vacancy")):
    namespace = onto
    equivalent_to = [requireMarketingKnowledge.min(1, MarketingKnowledge)]


class MiddleSalesManagerVacancy(onto.SalesManagerVacancy, get_class(onto, "Middle_Vacancy")):
    namespace = onto


if __name__ == "__main__":
    print("===========================================================================================================")
    print("All classes after adding: ")
    for cl in onto.classes():
        print("\t", cl.name)
    print("Total: ", len(list(onto.classes())))

    print("===========================================================================================================")
    print("All properties after adding: ")
    for pr in onto.properties():
        print("\t", pr.name)
    print("Total: ", len(list(onto.properties())))

    print("===========================================================================================================")
    marketing_theorem = MarketingKnowledge("marketing_theorem")

    middle_sales_manager_vacancy = MiddleSalesManagerVacancy("middle_sales_manager_vacancy")
    middle_sales_manager_vacancy.requireLanguageKnowledge = [get_individuals(onto, "Upper-Intermediate")]
    middle_sales_manager_vacancy.proposedBy = [get_individuals(onto, "GlobalLogic")]
    middle_sales_manager_vacancy.allocatedIn = [get_individuals(onto, "Kyiv")]
    middle_sales_manager_vacancy.requireMarketingKnowledge = [marketing_theorem]
    print("-----------------------------------------------------------------------------------------------------------")
    print(list(middle_sales_manager_vacancy.get_properties()))
    print("-----------------------------------------------------------------------------------------------------------")

    middle_sales_manager_vacancy_with_exp = MiddleSalesManagerVacancy("middle_sales_manager_vacancy_with_exp")
    print("All individuals after adding: ")
    for ind in onto.individuals():
        print("\t", ind.name)
    print("Total: ", len(list(onto.individuals())))

    print("===========================================================================================================")
    soft_serve = get_individuals(onto, "SoftServ")
    soft_serve.hasRating = 3.0
    print(list(soft_serve.get_properties()))

    python = get_individuals(onto, "Python")
    python.hasCompiler = True
    print(list(python.get_properties()))

    print("===========================================================================================================")
    destroy_entity(middle_sales_manager_vacancy_with_exp)
    print("All individuals after removing: ")
    for ind in onto.individuals():
        print("\t", ind.name)
    print("Total: ", len(list(onto.individuals())))

    print("===========================================================================================================")
    destroy_entity(onto.MiddleSalesManagerVacancy)
    print("All classes after deleting: ")
    for cl in onto.classes():
        print("\t", cl.name)
    print("Total: ", len(list(onto.classes())))

    print("===========================================================================================================")
    destroy_entity(onto.hasCompiler)
    print("All properties after deleting: ")
    for pr in onto.properties():
        print("\t", pr.name)
    print("Total: ", len(list(onto.properties())))

    print("===========================================================================================================")
    restr = SalesManagerVacancy.equivalent_to[0]
    print(f"{SalesManagerVacancy.name} has restriction {restr.property.name} "
          f"{DICT[restr.type]} {restr.cardinality} {restr.value.name}")

    print("===========================================================================================================")
    print("Consistency: ", check_consistency(onto))

    onto.save("res.owl")
