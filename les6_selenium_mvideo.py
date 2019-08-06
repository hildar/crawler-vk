"""
* 2) Написать программу, которая собирает «Хиты продаж» с сайтов
техники mvideo, onlinetrade и складывает данные в БД. Магазины можно
выбрать свои. Главный критерий выбора: динамически загружаемые товары
"""


import time
from selenium import webdriver  # Основной элемент
from selenium.webdriver.common.keys import Keys  # Клавиши клавиатуры
from pymongo import MongoClient


def parse_site_with_selenium():
    driver = webdriver.Chrome()
    driver.get('https://www.mvideo.ru')
    time.sleep(5)
    print(driver.page_source)

    bestseller_wrapper = driver.find_element_by_class_name('gallery-layout sel-hits-block ')
    bestseller = bestseller_wrapper.find_elements_by_class_name('gallery-list-item')
    # bestseller = driver.find_elements_by_class_name('gallery-list-item')
    # bestseller = driver.find_elements_by_tag_name('h4')

    print(f'length list of bestseller: {len(bestseller)}')
    print(bestseller)
    products = []
    count = 0
    for item in bestseller:
        print(f'count = {count}')
        count += 1
        # print(driver.page_source)
        # spam = item.find_element_by_class_name('sel-product-tile-title')
        # spam = item.find_element_by_css_selector('a.sel-product-tile-title')
        # spam = item.find_element_by_xpath('/a[@class="sel-product-tile-title"]')
        spam = item.find_element_by_tag_name('a')
        title = spam.text
        url = spam.get_attribute('href')
        products.append({'title': title,
                         'url': url})

    for prod in products:
        print(prod)

    driver.quit()
    return products


parse_site_with_selenium()


def client_mongo():
    client = MongoClient('mongodb://127.0.0.1:27017')
    data_base = client['db_mail_letters']  # db name
    mail_letters = data_base.mail_letters  # collection name
    return mail_letters


def save_to_mongo(letters: list):
    mail_letters = client_mongo()
    count = 0
    for letter in letters:
        spam = mail_letters.find_one({'content': letter['content']})
        if spam is None:
            mail_letters.insert_one(letter)
            count += 1
    print(f'Added {count} records. Collection "{mail_letters.name}" has {mail_letters.count_documents({})} letters')


# save_to_mongo(parse_site_with_selenium())

