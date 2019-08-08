"""
1) Написать программу, которая собирает входящие письма из своего
или тестового почтового ящика и сложить данные о письмах в базу
данных (от кого, дата отправки, тема письма, текст письма)
"""

from time import sleep
from selenium import webdriver  # Основной элемент
from selenium.webdriver.common.keys import Keys  # Клавиши клавиатуры
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient


def parse_site_with_selenium():
    options = Options()
    options.headless = True  # add headless mode
    driver = webdriver.Chrome(options=options)
    driver.get('https://mail.ru')
    elem = driver.find_element_by_id('mailbox:login')
    elem.send_keys('test-bender@mail.ru')
    elem = driver.find_element_by_id('mailbox:password')
    elem.send_keys('youpieceofmeat')
    elem.send_keys(Keys.RETURN)
    sleep(6)  # Download page maybe so long
    letters_class_name = 'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal'
    letters = driver.find_elements_by_xpath(f'//a[contains(@class, "{letters_class_name}")]')
    letters_all = []
    letters_links = []
    for letter in letters:
        letters_links.append(letter.get_attribute('href'))
    for letter in letters_links:
        driver.get(letter)
        sleep(1)
        author = driver.find_element_by_class_name('letter__contact-item').text
        date = driver.find_element_by_class_name('letter__date').text
        topic = driver.find_element_by_class_name('thread__subject').text
        content = driver.find_element_by_class_name('letter-body').text
        letters_all.append({'author': author,
                            'date': date,
                            'topic': topic,
                            'content': content})
    driver.quit()
    return letters_all


def client_mongo(db_name: str, collection_name: str):
    client = MongoClient('mongodb://127.0.0.1:27017')
    data_base = client[db_name]  # db name
    collect_name = data_base[collection_name] # collection name
    return collect_name


def save_to_mongo(list_to_save_db: list, unique_key: str, db_name: str, collection_name: str):
    collection = client_mongo(db_name, collection_name)
    count = 0
    for item in list_to_save_db:
        spam = collection.find_one({unique_key: item[unique_key]})
        if spam is None:
            collection.insert_one(item)
            count += 1
    print(f'Added {count} records. Collection "{collection.name}" has {collection.count_documents({})} items.')


save_to_mongo(parse_site_with_selenium(), 'content', 'db_mail_letters', 'mail_letters')
