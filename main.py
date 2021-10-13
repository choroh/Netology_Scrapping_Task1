"""
Netology. Скрапинг.
Необходимо парсить страницу со свежими статьями
https://habr.com/ru/all/
и выбирать те статьи, в которых встречается хотя бы одно
из ключевых слов (эти слова определяем в начале скрипта). Поиск вести по всей доступной preview-информации
(это информация, доступная непосредственно с текущей страницы). Вывести в консоль список подходящих статей
в формате: <дата> - <заголовок> - <ссылка>.

Дополнительное задание:
Улучшить скрипт так, чтобы он анализировал не только preview-информацию статьи, но и весь текст статьи целиком.
Для этого потребуется получать страницы статей и искать по тексту внутри этой страницы.
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


def find_article(current_article, article_scrap):
    """
    Функция проверяет, есть ли ключевые слова KEYWORDS [ ] в полученном тексте.
    Если есть - выдает дату - заголовок - ссылку и ключевое слово, по которому данная статья найдена.
    :param current_article:
    :param article_scrap:
    """
    for key in KEYWORDS:
        #  Вариант поиска различных ключевых слов из любого списка
        if key.title() in article_scrap or key.lower() in article_scrap or key.upper() in article_scrap:
            #if KEYWORDS[0] in preview or KEYWORDS[1] in preview or KEYWORDS[2] in preview or KEYWORDS[3] in preview:
            #  Вариант поиска фиксированных ключевых слов из задания
            title = current_article.find('h2').text.strip()
            href = current_article.find(class_='tm-article-snippet__title-link').attrs['href']
            current_clink = domain + href
            #  Получили заголовок и ссылку
            #  data = article.find(class_="tm-article-snippet__datetime-published").text
            #  вывод даты в виде "сегодня в 15:00"
            data = current_article.find("span", class_="tm-article-snippet__datetime-published").find("time").get("title")
            #  Находим запись даты, выделяем тег time и получаем от туда дату и время из title
            print(f'{data} - {title} - {current_clink}. ключевое слово: {key}')
            break


print('Поиск по превью')
for article in articles:
    #  Перебираем блок по статьям
    preview = article.find("div", class_="tm-article-body tm-article-snippet__lead").text.strip()
    #  Получаем превью статей и отправляем в функцию на обработку
    find_article(article, preview)

print()
#  Поиск по статье целиком
print('Поиск по статье целиком')
for article in articles:
    current_article_href = (article.find("div", class_="tm-article-body tm-article-snippet__lead").
                            find("a", class_="tm-article-snippet__readmore").get("href"))
    #  Получили ссылку на полную статью
    link1 = domain + current_article_href
    responce1 = requests.get(link1)
    responce1.raise_for_status()

    soup1 = (bs4.BeautifulSoup(responce1.text, features='html.parser').
             find("div", class_="tm-article-presenter__body").text.strip())
    #  Передаем текст страницы целиком и отправляем в функцияю на обработку
    find_article(article, soup1)



