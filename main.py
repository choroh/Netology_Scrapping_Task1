"""
Netology. Скрапинг.
Необходимо парсить страницу со свежими статьями
https://habr.com/ru/all/
и выбирать те статьи, в которых встречается хотя бы одно
из ключевых слов (эти слова определяем в начале скрипта). Поиск вести по всей доступной preview-информации
(это информация, доступная непосредственно с текущей страницы). Вывести в консоль список подходящих статей
в формате: <дата> - <заголовок> - <ссылка>.
12.12.21
"""

import requests
import bs4

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

#  Будем искать статьи с этими ключевыми словами

url = 'https://habr.com/ru/all'
domain = "https://habr.com"

responce = requests.get(url)
responce.raise_for_status()

soup = bs4.BeautifulSoup(responce.text, features='html.parser')
#  передаем текст, который нужно разобрать text, правило, по которому разбирать features='html.parser'
#  Получаем всю страницу
articles = soup.find_all('article')
#  Получаем блок всех статей
print(f'Статьи с сайта {url}, в которых присутствуют ключевые слова {KEYWORDS}')
print(f'Дата - Заголовок - Ссылка')


for article in articles:
    #  Перебираем блок по статьям
    preview = article.find("div", class_="tm-article-body tm-article-snippet__lead").text.strip()
    #  Получаем превью статей
    if KEYWORDS[0] in preview or KEYWORDS[1] in preview or KEYWORDS[2] in preview or KEYWORDS[3] in preview:
        title = article.find('h2').text.strip()
        href = article.find(class_= 'tm-article-snippet__title-link').attrs['href']
        link = domain + href
        #  Получили заголовок и ссылку
        #  data = article.find(class_="tm-article-snippet__datetime-published").text
        #  вывод даты в виде "сегодня в 15:00"
        data = article.find("span", class_="tm-article-snippet__datetime-published").find("time").get("title")
        #  Находим запись даты, выделяем тег time и получаем от туда дату и время из title
        print(f'{data} - {title} - {link}')


