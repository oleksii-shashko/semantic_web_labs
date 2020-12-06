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


def quantity_of_classes(ontology: Ontology):
    return len(list(ontology.classes()))


def quantity_of_individuals(ontology: Ontology):
    return len(list(ontology.individuals()))


def get_property(ontology: Ontology, name: str):
    for property in ontology.properties():
        if property.name == name:
            return property


def get_classes_with_property(ontology: Ontology, property_name: str):
    results = []
    property = get_property(ontology, property_name)

    for cl in ontology.classes():
        if property in cl.INDIRECT_get_class_properties():
            results.append(cl)

    return results, property


def restriction_analysis(ontology: Ontology):
    res = {}
    for cl in ontology.classes():
        if len(list(cl.get_indirect_equivalent_to())) != 0:
            for et in list(cl.get_indirect_equivalent_to()):
                if type(et) == And:
                    continue
                try:
                    et.name
                except:
                    res[et] = clear(cl.descendants())
    return res


def get_data_about_ind(_class: ThingClass, ontology: Ontology):
    indv = list(ontology.individuals())
    curr_indv = []

    for ind in indv:
        if _class in ind.is_instance_of:
            curr_indv.append(ind)
    if len(curr_indv) != 1:
        return None

    return curr_indv[0]


def show_analysis(ontology: Ontology):
    res = restriction_analysis(ontology)
    for k in list(res):
        try:
            print(f"Restriction {k.property.name} {DICT[k.type]} {k.cardinality} {k.value}:")
            for el in res[k]:
                ind = get_data_about_ind(el, ontology)
                if ind is None:
                    print("\t", el.name)
                else:
                    print("\t", el.name, "\t\t\t", getattr(ind, k.property.name))
        except Exception:
            print(f"Restriction {k}:")
            for el in res[k]:
                print("\t", el.name)
        print(f"Total: {len(res[k])}\n")


if __name__ == "__main__":
    print("===========================================================================================================")
    print("Consistency: ", check_consistency(onto))

    print("===========================================================================================================")
    print("Quantity of classes: ", quantity_of_classes(onto))

    print("===========================================================================================================")
    print("Quantity of individuals: ", quantity_of_individuals(onto))

    print("===========================================================================================================")
    list_of_classes, prop = get_classes_with_property(onto, "allocatedIn")
    print(f"List of classes with property {prop.name}: ")
    for cl in list_of_classes:
        print("\t", cl.name)

    print("===========================================================================================================")
    show_analysis(onto)
