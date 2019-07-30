# 1) С помощью BeautifulSoup спарсить новости с https://news.yandex.ru по своему региону.
#  * Заголовок
#  * Краткое описание
#  * Ссылка на новость
# 2) * Разбить новости по категориям
# * Расположить в хронологическом порядке

"""
This file parse the news from  news.yandex.ru by Amur region
"""


import requests
from bs4 import BeautifulSoup
import re


def request_to_site():
    """
    Request to site and response HTML page
    :return: response from site
    """
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    aria = 'Blagoveshchensk'
    try:
        response = requests.get(f'https://news.yandex.ru/{aria}/index.html', headers=headers)
        return response
    except requests.exceptions.ConnectionError:
        print('ConnectionError')
        exit(1)


def get_soup():
    """
    Get BeautifulSoup object
    :return: soup
    """
    html_news = request_to_site().text
    soup = BeautifulSoup(html_news, 'html.parser')
    return soup


def get_news(soup: BeautifulSoup, story_type: str):
    """
    Get list of news by type of stories
    :param soup: BeautifulSoup object
    :param story_type: type of stories
    :return: list news by story type - [category, title, overview, tuple(hour time, minute time)]
    """
    news = soup.findAll('div', attrs={'class': story_type})
    # different types have different tags - <div> or <td>
    if not news:
        news = soup.findAll('td', attrs={'class': story_type})
    news_story_type = []
    for new in news:
        spam = []
        spam.append(new.find('a').text)
        spam.append(new.find('h2', attrs={'class': 'story__title'}).text)
        try:
            spam.append(new.find('div', attrs={'class': 'story__text'}).text)
        except AttributeError:
            spam.append('-' * 5 + ' Нет описания ' + '-' * 5)
        spam.append('https://news.yandex.ru' + new.find('a', attrs={'class': 'link link_theme_black i-bem'})['href'])
        spam.append(re.findall('(\d+):(\d+)', new.find('div', attrs={'class': 'story__date'}).text))
        news_story_type.append(spam)
    return news_story_type


# Get soup and set the story types
bs_soup = get_soup()
story_types = ['stories-set__main-item',
               'story story_view_normal story_noimage',
               'stories-set__item',
               'story story_view_with-left-image']

# Get all news in list news_all
news_all = []
for story in story_types:
    news_all += get_news(bs_soup, story)

# Get categories of news and convert string time to integer
categories = []
for i, news in enumerate(news_all):
    categories.append(news[0])
    news_all[i][4] = int(news[4][0][0] + news[4][0][1])
categories = list(set(categories))

# Sort by time
news_all = sorted(news_all, key=lambda news: news[4], reverse=True)

# Print news
print(f'\nВсего в новостях по Амурской области {len(categories)} категории: {categories}')
for category in categories:
    print(f'\n{" " * 50}----- {category} -----\n')
    for news in news_all:
        if news[0] == category:
            for new in news[1:]:
                if type(new) != int:
                    # Print title, overview and link
                    print(new)
                else:
                    # Print time
                    eggs = new % 100
                    print(f'{new // 100}:{"0" + str(eggs) if eggs <= 9 else eggs}')
            print('\n')
    print('*' * 50 + '\n')

