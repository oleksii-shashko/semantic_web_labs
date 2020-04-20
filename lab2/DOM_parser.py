import lxml.etree as ET


class VacancyXML:
    def __init__(self, xml_path):
        self.xml_path = xml_path
        self.dom = ET.parse(self.xml_path)
        self.root = self.dom.getroot()

    def save(self, xml_path=None):
        if xml_path:
            self.dom.write(xml_path, encoding="UTF-8", xml_declaration=True)
        else:
            self.dom.write(self.xml_path, encoding="UTF-8", xml_declaration=True)

    def clean_info(self):
        for vacancy in self.root.findall("vacancy"):
            info = vacancy.find("info")
            info.text = info.text.replace("\n", " ")

    def add_id(self, element_name: str):
        parent_name = list(self.root.iter(element_name))[0].getparent().tag
        for parent in self.root.iter(parent_name):
            for i, element_iter in enumerate(parent.getchildren()):
                element_iter.set("id", str(i))

    def add_quantity(self, element_name: str):
        for element_iter in self.root.iter(element_name):
            element_iter.set("quantity", str(len(element_iter.getchildren())))

    def add_remote_element(self):
        for vacancies in self.root.getchildren():
            cities_list = vacancies.find("cities").findall("city")
            remote = ET.SubElement(vacancies, "remote")

            for city in cities_list:
                if city.text.replace("\n", "").strip() == "remote":
                    remote.text = "True"
                    vacancies.find("cities").remove(city)
                    break
            if remote.text is None:
                remote.text = "False"


def make_html(xml: str, xslt: str):
    dom = ET.parse(xml)
    xslt_parse = ET.parse(xslt)

    transform = ET.XSLT(xslt_parse)
    new_dom = transform(dom)

    with open("dou_vacancies.html", "w", encoding="utf-8") as file:
        file.write(str(new_dom))


if __name__ == "__main__":
    dou_vacancies = VacancyXML("dou_vacancies.xml")

    dou_vacancies.add_id("city")
    dou_vacancies.add_quantity("cities")
    dou_vacancies.clean_info()
    dou_vacancies.add_remote_element()

    dou_vacancies.save("dou_vacancies_1.xml")

    make_html("dou_vacancies_1.xml", "dou_vacancies.xslt")
