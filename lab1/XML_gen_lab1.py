from bs4 import BeautifulSoup
import lxml.etree as ET
import requests


TRANSLATER = {
    "удаленно": "remote",
    "Киев": "Kiev",
    "Львов": "Lviv",
    "Одесса": "Odessa",
    "New York City": "New York City",
    "Харьков": "Kharkov",
    "за рубежом": "abroad",
    "Днепр": "Dnepr"
}


def make_xml(names: list, company: list, cities: list, info: list):
    soup = BeautifulSoup(features="xml")
    vacancy_list = soup.new_tag("vacancy-list", attrs={"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                                       "xsi:noNamespaceSchemaLocation": ".\\vacancies.xsd"})

    for i in range(len(names)):
        vacancy = soup.new_tag("vacancy", attrs={"id": i})

        name = soup.new_tag("name")
        name.string = names[i]
        vacancy.append(name)

        company_tag = soup.new_tag("company")
        company_tag.string = company[i]
        vacancy.append(company_tag)

        cities_tag = soup.new_tag("cities")
        for city_item in cities[i]:
            city = soup.new_tag("city")
            city.string = TRANSLATER[city_item]

            cities_tag.append(city)
        vacancy.append(cities_tag)

        info_tag = soup.new_tag("info")
        info_tag.string = info[i]
        vacancy.append(info_tag)

        vacancy_list.append(vacancy)

    soup.append(vacancy_list)
    return soup


def generate_xml(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

    website_page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(website_page, "lxml")
    list_of_vacancies = soup.find("ul", {"class": "lt"})

    vacancies = list_of_vacancies.find_all_next("li", {"class": "l-vacancy"})
    names = []
    company = []
    cities = []
    info = []

    for item in vacancies:
        names.append(item.find("a", {"class": "vt"}).text)
        company.append(item.find("a", {"class": "company"}).text)
        cities.append(item.find("span", {"class": "cities"}).text.split(", "))
        info.append(item.find("div", {"class": "sh-info"}).text)

    xml_data = make_xml(names, company, cities, info)
    temp = ET.fromstring(xml_data.prettify("utf-8"))

    xml_data_str = ET.tostring(temp, encoding="utf-8", xml_declaration=True).decode("utf-8").replace("\u2028", "-")

    with open("dou_vacancies.xml", "w") as file:
        file.write(xml_data_str)


if __name__ == "__main__":
    URL_DOU = "https://jobs.dou.ua/vacancies/?category=Python"

    generate_xml(URL_DOU)
