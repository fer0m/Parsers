import csv
import requests
import lxml
import math
import sys
from datetime import datetime
from bs4 import BeautifulSoup


Finally_list = []

# Получаем страницу для работы
def get_html(urls):
    r = requests.get(urls)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


# Получаем имя поста (список)
def get_name_of_post(soup):
    name_of_post_soup = soup.find_all("a", class_="post__title_link")
    name_of_posts = []
    for i in name_of_post_soup:
        i = i.text.strip()
        name_of_posts.append(i)
    # print(name_of_posts)
    # print(len(name_of_posts))
    return name_of_posts


# Получаем теги поста (список)
def get_tags(soup):
    tags_soup = soup.find_all("ul", class_="post__hubs inline-list")
    tags_list = []
    for tag in tags_soup:
        tag_1 = tag.text.strip()
        tag_final = ' '.join(tag_1.split())
        tags_list.append(tag_final)
    # print(tags_list)
    # print(len(tags_list))
    return tags_list


# Получаем имя автора (список)
def get_name_autor(soup):
    name_autor_soup = soup.find_all("span", class_="user-info__nickname user-info__nickname_small")
    names = []
    for i in name_autor_soup:
        i = i.text.strip()
        names.append(i)
    # print(names)
    # print(len(names))
    return names


# Получаем время создания поста (список)
def get_post_time(soup):
    post_time = soup.find_all("span", class_="post__time")
    all_time = []
    for time in post_time:
        time = time.text.strip()
        all_time.append(time)
    # print(all_time)
    # print(len(all_time))
    return all_time


# Получаем начальный текст поста (список)
def get_post_text(soup):
    post_text = soup.find_all("div", class_="post__text post__text-html js-mediator-article")
    all_texts_in_post = []
    for text in post_text:
        text = text.text.strip()
        text_final = ' '.join(text.split())
        all_texts_in_post.append(text_final)
    # print(all_texts_in_post)
    # print(len(all_texts_in_post))
    return all_texts_in_post


# Главная функция формирования списка с нужной нам информацией
def main(urls, post_count, count):
    soup = get_html(urls)
    post_name = get_name_of_post(soup)
    tags_post = get_tags(soup)
    text_post = get_post_text(soup)
    date_post = get_post_time(soup)
    author_post = get_name_autor(soup)

    if (post_count - count) > 20:
        for num in range(len(post_name)):
            Finally_list.append(
                [post_name[num]] + [tags_post[num]] + [text_post[num]] + [date_post[num]] + [author_post[num]])
            csv_writer(Finally_list)

    else:
        for num in range(post_count - count):
            Finally_list.append(
                [post_name[num]] + [tags_post[num]] + [text_post[num]] + [date_post[num]] + [author_post[num]])
            csv_writer(Finally_list)

# Функция расчета количества необходимых страни, получение urls, для получения количесва постов post_count.
def make_pages(post_count):
    count = -20
    pages = math.ceil(post_count / 20)
    for i in range(pages):
        elem = str(i + 1)
        urls = 'https://habr.com/ru/top/yearly/page' + elem
        count = count + 20
        main(urls, post_count, count)


# Фукнция записи в csv. файл
def csv_writer(data):
    FILENAME = "Database.csv"

    with open(FILENAME, "w+", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(data)


if __name__ == '__main__':
    count_of_posts = sys.argv[1]
    start_time = datetime.now()
    if count_of_posts == 0:
        print("В качестве агрумента необходимо ввести ненулевое значение")
    elif not count_of_posts.isdigit():
        print("В качестве аргумета необходимо ввести число")
    elif count_of_posts.isdigit():
        print("Время начала парсинга: ", start_time)
        make_pages(int(count_of_posts))

    end_time = datetime.now()
    print("Время завершения парсинга: ", end_time)
    print("Время исполнения: ", end_time-start_time)
