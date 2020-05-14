from lxml.etree import parse, tostring


def query(tree_, query_str):
    return tree_.xpath(query_str)


def get_elements_by_quantity(tree_):
    return [node for node in query(tree_, "//*[@quantity]")]


def get_element_by_id(tree_):
    return query(tree_, "/vacancy-list/vacancy[@id=1]/name/text()")[0]


def get_number_of_complex_name(tree_):
    return query(tree_, "//vacancy[name[contains(.,' ')]]/@id")


def n_complex(tree_, n: int):
    return query(tree_, f"/vacancy-list/vacancy[1]/child::*[{n}]/text()")[0]


def quantity_and_name(tree_):
    return query(tree_, "/vacancy-list/*[cities/@quantity > 1 and cities/@quantity < 4 and "
                        "starts-with(name, '\n   Senior')]/company/text()")


def fifth_el(tree_):
    return query(tree_, "//vacancy[@id mod 5 = 0]/name/text() | //vacancy[@id mod 5 = 0]/remote/text()")


def second_plus(tree_):
    return query(tree_, "//vacancy[@id mod 2 = 0]/@id | //vacancy[@id mod 2 = 0]/cities/@quantity")


def kharkov_companies(tree_):
    return query(tree_, "/vacancy-list/*[starts-with(cities/*/text(), '\n    Kharkov')]/company/text()")


def engineers(tree_):
    return query(tree_, "//vacancy[contains(name/text(), 'Engineer') and cities/@quantity < 3 and @id mod 3 = 0]"
                        "/name/text()")


if __name__ == "__main__":
    tree = parse("dou_vacancies.xml")

    # task 1
    print("======================Task 1======================\n")
    print(query(tree, "count(/vacancy-list/vacancy)"))
    print("\n")

    # task 2
    print("======================Task 2======================\n")
    for el in get_elements_by_quantity(tree):
        print(tostring(el).decode().replace("\n", "").strip())
    print("\n")

    # task 3
    print("======================Task 3======================\n")
    print(get_element_by_id(tree))
    print("\n")

    # task 4
    print("======================Task 4======================\n")
    print(get_number_of_complex_name(tree))
    print("\n")

    # task 5
    print("======================Task 5======================\n")
    print(n_complex(tree, 1))
    print("\n")

    # task 6
    print("======================Task 6======================\n")
    print(quantity_and_name(tree))
    print("\n")

    # task 7
    print("======================Task 7======================\n")
    for el in fifth_el(tree):
        print(el.replace("\n", "").strip())
    print("\n")

    # task 8
    print("======================Task 8======================\n")
    locker = False
    for el in second_plus(tree):
        if not locker:
            temp = el
            locker = True
            continue
        print("Element ", temp, ": ", el)
        locker = False
    print("\n")

    # task 9
    print("======================Task 9======================\n")
    for el in kharkov_companies(tree):
        print(el.replace("\n", "").strip())
    print("\n")

    # task 10
    print("======================Task 10======================\n")
    for el in engineers(tree):
        print(el.replace("\n", "").strip())
    print("\n")
