# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге
# MongoDB и реализовать функцию, записывающую собранные объявления
# с avito.ru в созданную БД (xpath/BS для парсинга на выбор)
#
# 2) Написать функцию, которая производит поиск и выводит на экран
# объявления с ценой меньше введенной суммы
#
# *Написать функцию, которая будет добавлять в вашу базу данных
# только новые объявления


import pprint
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup


def request_to_site():
    param = input('Type kind or color the cat to add in data base (e.g.: рыжий):  ')
    params = {'q': param}
    try:
        response = requests.get('https://www.avito.ru/amurskaya_oblast_blagoveschensk/koshki', params=params)
        return response
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def get_ads():
    response = request_to_site().text
    soup = BeautifulSoup(response, 'html.parser')
    adverts = soup.find_all('div', {'class': 'description item_table-description'})
    ads = []
    spam = dict
    for advert in adverts:
        spam = {
            'title': advert.find('h3').text[2:-2],  # A slice is need for remove excess characters
            'price': int(advert.find('span', {'class': 'price'})['content']),
            'link': 'https://www.avito.ru/' + advert.find('a')['href']
        }
        ads.append(spam)
    return ads


def client_mongo():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['db_ads']  # db name
    ads_db = db.ads  # collection name
    return ads_db


def save_to_mongo(adventures: list):
    ads_db = client_mongo()
    count = 0
    for adventure in adventures:
        spam = ads_db.find_one({'link': adventure['link']})
        if spam is None:
            ads_db.insert_one(adventure)
            count += 1
    print(f'Added {count} records. Collection "{ads_db.name}" has {ads_db.count_documents({})} adventures')


def search_by_price():
    try:
        price = int(input('\nEnter a number to search for ads with a price less than the entered amount: '))
    except ValueError:
        print('Please, inter the number, not characters')
        exit(1)
    ads_db = client_mongo()
    ads_cursor = ads_db.find({'price': {'$lt': price}})
    for ads in ads_cursor:
        pprint.pprint(ads)


save_to_mongo(get_ads())
search_by_price()
