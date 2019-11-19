from selenium import webdriver
import time
import re
from selenium.webdriver.common.keys import Keys
import csv


def init_driver():
    path = "C:\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=path)
    driver.get("https://bookmaker-ratings.ru/review/obzor-bukmekerskoj-kontory-ligastavok/all-feedbacks/")
    return driver


def how_many_comment():
    # Поиск значения Общего Количества отзывов
    value_with_number = driver.find_elements_by_xpath("//a[@class='tab-nav-item item active']")[0].text

    # Получаем из текста число
    count_comments = int(re.findall('\d+', value_with_number)[0])
    return count_comments

# Функция парса информации, с возможностью назначение количества необходимых отзывов вручную
def copy_func(comment_count):
    total_result = []
    try:
        # Запуск цикла "пробега" по отзывам
        for i in range(1, comment_count + 1):
            # Тут теле if - лютый велописед для прогрузки последующих отзывов с обходом ошибки ChromeDriver на моей ОС
            if i % 30 == 0:
                time.sleep(5)

                try:
                    driver.find_element_by_xpath("//div[@class='menu-scroll']/a[13]").send_keys(Keys.HOME)
                    time.sleep(5)
                except:
                    pass
                    driver.find_element_by_xpath("//button[@id='all-feedbacks-more-btn']").click()
                    time.sleep(5)

            try:
                # Получаем необходимую текстовую часть. Имя_Роль, Оценку, Отзыв, Дату отзыва

                # Имя_Роль
                name_and_stats = driver.find_elements_by_xpath(
                    "//div[@id='feedbacks-list']/div[" + str(i) + "]/div[@class='head']/div[@class='name']")[0].text

                # Значение оценки
                count = \
                    driver.find_elements_by_xpath(
                        "//div[@id='feedbacks-list']/div[" + str(i) + "]/div[1]/span/span[2]")[
                        0].text

                # Сам отзыв
                comment = \
                    driver.find_elements_by_xpath("//div[@id='feedbacks-list']/div[" + str(i) + "]/div[2]/div[1]")[
                        0].text

                # Дата
                date = driver.find_elements_by_xpath("//div[@id='feedbacks-list']/div[" + str(i) + "]/div[3]/div[1]")[
                    0].text

                temp_value = name_and_stats.split(' ')

                # Временная функция для извлечения отдельно Имени и Роли.
                stats = temp_value[-1:]
                name = ' '.join(temp_value[:-1])

                total_result.append([name] + stats + [str(count)] + [comment] + [date])
            except:
                pass

        return total_result

    except:
        print("Закончили")
        return total_result


# Запись в файл.
def csv_writer(data):
    FILENAME = "Database.csv"

    with open(FILENAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(data)


if __name__ == "__main__":
    driver = init_driver()
    time.sleep(5)
    csv_writer(copy_func(how_many_comment()))
