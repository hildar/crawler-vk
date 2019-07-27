# 1) Необходимо собрать информацию о вакансиях на должность программиста или разработчика
# с сайта job.ru или hh.ru. (Можно с обоих сразу) Приложение должно анализировать несколько
# страниц сайта. Получившийся список должен содержать в себе:
#   * Наименование вакансии,
#   * Предлагаемую зарплату
#   * Ссылку на саму вакансию
#
# 2) Доработать приложение таким образом, чтобы можно было искать разработчиков на разные языки
# программирования (Например Python, Java, C++)

import requests
import pprint
from lxml import html


# Get vacancy from hh.ru
def get_vacancy(url: str, p: dict, h: dict):
    # For emulate real human behavior need 'headers' and run method requests.Session()
    session = requests.Session()
    # Try to request on site
    try:
        req = requests.get(url, params=p, headers=h)
    except requests.exceptions.ConnectionError:
        print("No connection to site")
        exit(1)
    # Get info from HTML
    root = html.fromstring(req.text)
    divs = root.xpath('//div[contains(@class, "vacancy-serp")]')
    links, vacancies, salaries = [], [], []
    for i in range(1, 25):
        # Get links
        spam = divs[1].xpath(f'div[{i}]//div[contains(@class, "resume-search-item__name")]/a/@href')
        if spam: links.append(spam[0])
        # Get vacancies
        spam = divs[1].xpath(f'div[{i}]//div[contains(@class, "resume-search-item__name")]/a/text()')
        if spam: vacancies.append(spam[0])
        # Get salaries
        spam = divs[1].xpath(f'div[{i}]//div[contains(@data-qa, "vacancy-serp__vacancy-compensation")]/text()')
        if i not in [7,8, 15, 16]:
            salaries.append(spam[0]) if spam else salaries.append('--')

    if req.status_code == 200:
        #     print(f'{v3[i]:<70} {s3[i]:<25} {l3[i]}')
        # print(links, '\n', vacancies, '\n', salaries)
        return links, vacancies, salaries
    else:
        print('Error: status code != 200')
        exit(1)


# Get some pages for one position
def get_some_pages(url: str, p: dict, h: dict, count: int):
    pages = [i for i in range(count)]
    links, vacancies, salaries = [], [], []
    for i in pages:
        p['page'] = str(i)
        spam1, spam2, spam3 = get_vacancy(url, p, h)
        links += spam1
        vacancies += spam2
        salaries += spam3
    return links, vacancies, salaries


# Get vacancy for other positions
def get_positions(url: str, p: dict, h: dict, vacancy: list, count=3):
    links, vacancies, salaries = [], [], []
    for v in vacancy:
        p['text'] = v
        spam1, spam2, spam3 = get_some_pages(url, p, h, count)
        links.append(spam1)
        vacancies.append(spam2)
        salaries.append(spam3)
    return links, vacancies, salaries


# Main function to print vacancies
def print_vacancy():
    # For emulate real human behavior need 'headers' and run method requests.Session()
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/75.0.3770.142 Safari/537.36'}
    # Set the base url and params
    url_zero = 'https://hh.ru/search/vacancy/'
    params = {'area': '1',
              'text': 'Data science',
              'page': '0'}
    # Set positions and count of pages by parse
    vac = ['Data science', 'Data engineer', 'Python']
    count_pages = 3
    positions = get_positions(url=url_zero, p=params, h=headers, vacancy=vac, count=count_pages)
    # Print vacancies in the console
    for i in range(len(vac)):
        print(f'\nВакансии с {count_pages} страниц на позицию "{vac[i]}"":\n')
        for j in range(len(positions[0][0])):
            print(f'{positions[1][i][j]:<85} {positions[2][i][j]:<25} {positions[0][i][j]}')
        print('\n\n')


print_vacancy()
