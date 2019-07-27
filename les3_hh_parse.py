# 1) Необходимо собрать информацию о вакансиях на должность программиста или разработчика
# с сайта job.ru или hh.ru. (Можно с обоих сразу) Приложение должно анализировать несколько
# страниц сайта. Получившийся список должен содержать в себе:
#   * Наименование вакансии,
#   * Предлагаемую зарплату
#   * Ссылку на саму вакансию
#
# 2) Доработать приложение таким образом, чтобы можно было искать разработчиков на разные языки
# программирования (Например Python, Java, C++)
"""
This python file get the vacancies from hh.ru
"""

import requests
from lxml import html


# Get vacancy from hh.ru
def get_vacancy(url: str, params: dict, headers: dict):
    """
    For emulate real human behavior need 'headers' and run method requests.Session()
    :param url: urls
    :param params: params of get request of url
    :param headers: headers need to emulate homo sapiens
    :return: three lists - links, vacancies, salaries
    """
    session = requests.Session()
    # Try to request on site
    try:
        req = requests.get(url, params=params, headers=headers)
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
        if spam:
            links.append(spam[0])
        # Get vacancies
        spam = divs[1].xpath(f'div[{i}]//div[contains(@class, "resume-search-item__name")]/a/text()')
        if spam:
            vacancies.append(spam[0])
        # Get salaries
        spam = divs[1].xpath(f'div[{i}]//div[contains(@data-qa, "vacancy-serp__vacancy-compensation")]/text()')
        if i not in [7, 8, 15, 16]:
            salaries.append(spam[0]) if spam else salaries.append('--')
    if req.status_code == 200:
        return links, vacancies, salaries
    print('Error: status code != 200')


# Get some pages for one position
def get_some_pages(url: str, params: dict, headers: dict, count: int):
    pages = [i for i in range(count)]
    links, vacancies, salaries = [], [], []
    for i in pages:
        params['page'] = str(i)
        spam1, spam2, spam3 = get_vacancy(url, params, headers)
        links += spam1
        vacancies += spam2
        salaries += spam3
    return links, vacancies, salaries


# Get vacancy for other positions
def get_positions(url: str, params: dict, headers: dict, vacancy: list, count=3):
    links, vacancies, salaries = [], [], []
    for vac in vacancy:
        params['text'] = vac
        spam1, spam2, spam3 = get_some_pages(url, params, headers, count)
        links.append(spam1)
        vacancies.append(spam2)
        salaries.append(spam3)
    return links, vacancies, salaries


# Main function to print vacancies
def print_vacancy():
    # For emulate real human behavior need 'headers' and run method requests.Session()
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36'
                             ' (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    # Set the base url and params
    url_zero = 'https://hh.ru/search/vacancy/'
    params = {'area': '1',
              'text': 'Data science',
              'page': '0'}
    # Set positions and count of pages by parse
    vacancy = ['Data science', 'Data engineer', 'Python']
    count_pages = 3
    positions = get_positions(url=url_zero, params=params, headers=headers, vacancy=vacancy, count=count_pages)
    # Print vacancies in the console
    for i, vac in enumerate(vacancy):
        print(f'\nВакансии с {count_pages} страниц на позицию "{vac}"":\n')
        for j in range(len(positions[0][0])):
            print(f'{positions[1][i][j]:<85} {positions[2][i][j]:<25} {positions[0][i][j]}')
        print('\n\n')


print_vacancy()
