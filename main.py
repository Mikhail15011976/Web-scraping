import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import json
from unicodedata import normalize

KEYWORDS = ["Django", "Flask"]
#Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.

HOST ='https://spb.hh.ru/search/vacancy?area=1&area=2&enable_snippets=true&excluded_text=&no_magic=' \
      'true&ored_clusters=true&search_field=name&search_field=description&search_period=' \
      '7&text=Python%2C+django%2C+Flask&order_by=publication_time'

def get_headers():
    headers = Headers(browser='firefox', os='win')
    return headers.generate()

response = requests.get(HOST, headers=get_headers())
hh_main = response.text
#pprint(hh_main)

soup = BeautifulSoup(hh_main, features='lxml')
vacancies = soup.find_all('div', class_ ='serp-item')
#pprint(vacancies)

parsed = []

for vacancy in vacancies:

    h3_link = vacancy.find('h3')
    a_link = h3_link.find('a')
    href_link = a_link['href']
    link_abs = f'https://spb.hh.ru{href_link}'
    #print(link_abs)

    salary = vacancy.find('span', "bloko-header-section-3")
    if salary == None:
        salary_num = ' '
    else:
        salary_num = salary.text
    #print(salary_num)

    company = vacancy.find('a', class_="bloko-link bloko-link_kind-tertiary")
    company_text = company.text
    #print(company_text)

    city = vacancy.find('div', {'data-qa': "vacancy-serp__vacancy-address"})
    city_text = city.text
    #print(city_text)

    parsed.append(
        {'link': link_abs,
         'salary': normalize('NFKD', salary_num),
         'company': normalize('NFKD', company_text),
         'city': normalize('NFKD', city_text)

        }
    )

pprint(parsed)

with open('hh_vacs', 'w', encoding='utf-8') as file:
    json.dump(parsed, file, indent=4, ensure_ascii=False, separators=(',', ': '))




