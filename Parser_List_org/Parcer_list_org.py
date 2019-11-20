import selenium
import time
import re
import csv
from selenium import webdriver
import sys

# Создаем словарь с xpath, для удобного поиска в случае изменений на сайте.
xpath_dict = {
    'f_name': "//p[1]/a[@class='upper']",
    'l_name': "//tr[1]/td[2]/a[@class='upper']",
    'date_1': "//div[@class='c2m'][1]/table[@class='tt']/tbody/tr[6]/td[2]",
    'date_2': "//div[@class='c2m'][1]/table[@class='tt']/tbody/tr[5]/td[2]",
    'date_3': "//div[@class='c2m'][1]/table[@class='tt']/tbody/tr[4]/td[2]",
    'stat_0': "//td[@class='status_0']",
    'stat_1': "//td[@class='status_1']",
    'INN': "//div[@class='content']/div[@class='c2m'][3]/p[1]",
    'KPP': "//div[@class='content']/div[@class='c2m'][3]/p[2]",
    'OGRN': "//div[@class='content']/div[@class='c2m'][3]/p[4]"
}


# Объявляем драйвер
def init_driver():
    path = "C:\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=path)
    driver.get(web_site)
    return driver


# Функция для определения формата, в соотв. с форматом даты на сайте дд.мм.гггг
def is_time(s):
    re_time = '..[.]..[.]....'
    if re.match(re_time, s) is not None:
        return True
    else:
        return False

# Поиск и получение информации по xpath
# Все запросы сделаны через try/except, для безостановочной работы парсера
def get_info():
    global register_date

    # Поиск полного названия компании
    try:
        full_name = driver.find_element_by_xpath(xpath_dict.get('f_name')).text
    except:
        full_name = "Не найдено"

    # Поиск имени собственника и форматирование
    try:
        leader_temp_1 = driver.find_element_by_xpath(xpath_dict.get('l_name')).text
        leader_temp_2 = leader_temp_1.split()
        leader = ' '.join(leader_temp_2[-3::])
    except:
        leader = "Не найдено"

    # Поиск даты создания. Лютый костыль из-за того, что "Дата" периодически находится
    # в различных тегах
    try:
        try:
            register_temp = driver.find_element_by_xpath(xpath_dict.get('date_1')).text
            if is_time(register_temp) == True:
                register_date = register_temp
        except:
            pass

        try:
            register_temp = driver.find_element_by_xpath(xpath_dict.get('date_2')).text
            if is_time(register_temp) == True:
                register_date = register_temp
        except:
            print("Я вылетел 2")
            pass

        try:
            register_temp = driver.find_element_by_xpath(xpath_dict.get('date_3')).text
            if is_time(register_temp) == True:
                register_date = register_temp
        except:
            pass
    except:
        register_date = "Не найдено"

    # Поиск "Состояния" фирмы. Два xpath.
    try:
        status = driver.find_element_by_xpath(xpath_dict.get('stat_0')).text
    except:
        status = driver.find_element_by_xpath(xpath_dict.get('stat_1')).text

    # Поиск ИНН и форматирование.
    try:
        INN_temp = driver.find_element_by_xpath(xpath_dict.get('INN')).text
        INN = re.findall(r'\b\d+\b', INN_temp)[0]
    except:
        INN = "Не найдено"

    # Поиск КПП и форматрование
    try:
        KPP_temp = driver.find_element_by_xpath(xpath_dict.get('KPP')).text
        KPP = re.findall(r'\b\d+\b', KPP_temp)[0]
    except:
        KPP = "Не найдено"

    # Поиск ОГРН и форматирование
    try:
        OGRN_temp = driver.find_element_by_xpath(xpath_dict.get('OGRN')).text
        OGRN = re.findall(r'\b\d+\b', OGRN_temp)[0]
    except:
        OGRN = "Не найдено"

    # Вывод результата как списка (для возможности последующего расширения функционала)
    total_result = []
    total_result.append([full_name] + [leader] + [register_date] + [status] + [INN] + [KPP] + [OGRN])

    return total_result

# Функция записи/дозаписи в файл
def csv_writer(data):
    FILENAME = "Database.csv"

    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(data)


if __name__ == "__main__":
    web_site = sys.argv[1]
    driver = init_driver()
    csv_writer(get_info())
    time.sleep(5)
