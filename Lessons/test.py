
import requests
from lxml import html
import pprint

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
# Set the base url and params
url = 'https://hh.ru/search/vacancy/'
params = {'area': '1',
          'text': 'Data science',
          'page': '0'}
# Set positions and count of pages by parse
vacancy = ['Data science', 'Data engineer', 'Python']

# For emulate real human behavior need 'headers' and run method requests.Session()
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
# for i in range(1, 25):
#     # Get links
#     spam = divs[1].xpath(f'//div[{i}]div[contains(@class, "resume-search-item__name")]/a/@href')
#     if spam:
#         links.append(spam[0])
#     # Get vacancies
#     spam = divs[1].xpath(f'div[{i}]//div[contains(@class, "resume-search-item__name")]/a/text()')
#     if spam:
#         vacancies.append(spam[0])
#     # Get salaries
#     spam = divs[1].xpath(f'div[{i}]//div[contains(@data-qa, "vacancy-serp__vacancy-compensation")]/text()')
#     if i not in [7, 8, 15, 16]:
#         salaries.append(spam[0] if spam else '--')

divs2 = root.xpath('//div[@class="vacancy-serp-item__row vacancy-serp-item__row_header"]')
sal = divs2[1].xpath('.//div[@class="vacancy-serp-item__compensation"]/text()')
if req.status_code == 200:
    # print(html.tostring(sal[0]))
    # print(sal)
    for v in divs2:
        try:
            print(v.xpath('.//div[@class="vacancy-serp-item__compensation"]/text()')[0])
        except IndexError:
            print('--')
    # for i in divs2:
    #     print(html.tostring(i))
else:
    print('Error: status code != 200')


    # bestseller_wrapper = driver.find_element_by_class_name('gallery-layout sel-hits-block ')
    # bestseller_wrapper = driver.find_element_by_class_name('sel-hits-block ')
    # bestseller_wrapper = driver.find_element_by_css_selector('.gallery-layout. sel-hits-block ') # Ищет по вложенности
    # bestseller_wrapper = driver.find_element_by_css_selector('.gallery-layout.sel-hits-block ')  # Ищет по сочетанию
    # bestseller_wrapper = driver.find_element_by_class_name('gallery-layout.sel-hits-block ')