# Задание 2. В приложении парсинга википедии получить первую ссылку на другую страницу и вывести все
# значимые слова из неё. Результат записать в файл в форматированном виде
#
# Задание 3. *Научить приложение определять количество ссылок в статье.
# Спарсить каждую ссылку и результаты
# записать в отдельные файлы.


import collections
import re
import requests
import csv


# Return HTML from site
def return_site_html(link):
    try:
        site_request = requests.get(link)
    except ConnectionError:
        print('Connection error to site: ru.wikipedia.org')
        exit(1)
    return site_request.text


# Return links from site
def return_links(url):
    site_html = return_site_html(url)
    links = re.findall('<li><a\s.*?href=\"([hf].+?)\".*?>', site_html)
    # Correct links if there are ampersand character - &
    for i in range(len(links)):
        links[i] = links[i].replace('amp;', '')
    return links


# Return words from site
def return_words_from_site(link):
    site_html = return_site_html(link)
    words = re.findall('[а-яА-Я]{3,}', site_html)
    # Count words
    words_counter = collections.Counter()
    for word in words:
        words_counter[word] += 1
    return words_counter.most_common(10)


# Get names from links
def get_names(links):
    links = str(links)
    spam = re.findall('\'https?://(www.)?([\w\.-]+)', links)
    names = []
    # Get only domain without 'www'
    for egg in spam:
        names.append(egg[1])
    # Replace dots and dashes in names
    for i in range(len(names)):
        names[i] = names[i].replace('.', '_')
        names[i] = names[i].replace('-', '_')
    # Add '2' if double names
    for i in range(len(names) - 1):
        for j in range(i + 1, len(names)):
            if names[j] == names[i]:
                names[j] = names[j] + '2'
    return names


# Write words to files
def file_writers(file_name, words):
    with open('parsing.git/L2_files/' + file_name + '.csv', 'w') as file:
        pen = csv.writer(file)
        pen.writerow(('Слово', 'Количество вхождений'))
        for word in words:
            pen.writerow((word[0], word[1]))


# Return words, links and write to files
def main_parsing(url):
    wiki_links = return_links(url)
    file_names = get_names(wiki_links)
    # Write to files
    for i, link in enumerate(wiki_links):
        spam = return_words_from_site(link)
        file_writers(file_names[i], spam)
    return f'Слова с {len(file_names)} сайтов записаны в файлы по адресу "parsing.git/L2_files/"'


main_url = 'https://ru.wikipedia.org/wiki/Трям!_Здравствуйте!'
print(main_parsing(main_url))
