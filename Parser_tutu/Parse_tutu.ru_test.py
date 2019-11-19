from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from networkx import Graph
import matplotlib.pyplot as plt


def init_driver():
    path = "C:\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=path)
    driver.get("https://www.tutu.ru/prigorod/")
    return driver


def select_station(driver, first_station, second_station):
    try:
        # Ожидание прогрузки элементов страницы.

        some_element_on_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[@class='b-button__arrow__button j-button j-button-submit _title j-submit_button "
                                        "_blue']"))
        )
    finally:
        # Ввод данных по станциям.

        elem_1 = driver.find_element_by_xpath(
            "//input[@class='input_field j-station_input  j-station_input_from']").click()
        elem_1 = driver.find_element_by_xpath(
            "//input[@class='input_field j-station_input  j-station_input_from']").send_keys(str(first_station))

        elem_2 = driver.find_element_by_xpath(
            "//input[@class='input_field j-station_input  j-station_input_to']").click()
        elem_2 = driver.find_element_by_xpath(
            "//input[@class='input_field j-station_input  j-station_input_to']").send_keys(str(second_station))

        enter = driver.find_element_by_xpath(
            "//button[@class='b-button__arrow__button j-button j-button-submit _title j-submit_button _blue']").click()

        base_timetable = driver.find_element_by_xpath("//span[@class='g-link']").click()

        go_to_train()


def go_to_train():
    window_before = driver.window_handles[0]  # Первоначальная страница поездов.

    # Данная функция может пройтись по всему списку возможных станций range(len(full_elem)) - отключена временно.
    full_elem = driver.find_elements_by_xpath("//a[@class='g-link depTimeLink_1NA_N undefined']")

    for i in range(3):
        magic_elem = driver.find_element_by_xpath("//tr[@class='card_yoy03  '][" + str(
            1 + i) + "]/td[@class='cell_2cdVW depTime_2Ue-g']/a[@class='g-link depTimeLink_1NA_N undefined']").send_keys(
            Keys.SHIFT + Keys.ENTER)

        window_after = driver.window_handles[1]  # Смена текущего окна.
        driver.switch_to_window(window_after)

        get_every_station_and_time()

        driver.switch_to_window(window_before)  # Смена окна на обратное, по завершению работы функ-ции.


def get_every_station_and_time():
    try:
        # Ожидание прогрузки элементов страницы.
        some_elem_on_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='decor_button_button']"))
        )
    finally:
        all_elem = driver.find_elements_by_xpath("//td[@class='flag']/a")

        # Создание графа
        G = Graph()
        temp = None

        # Пройти по всем значениям станция/время
        for i in range(len(all_elem)):
            current_city = driver.find_element_by_xpath("//tr[" + str(i + 1) + "]/td[@class='flag']/a").text
            current_time = driver.find_element_by_xpath(
                "//table[ @ id = 'schedule_table'] / tbody / tr[" + str(i + 1) + "] / td[3]").text

            # Наполнение графа(в разработке)
            if temp is None:
                G.add_node(current_city, Time=5)
            else:
                G.add_edge(temp, current_city, Time=6)
            temp = current_city

            print("Город - ", current_city, ";\t Время - ", current_time)

        driver.close()


if __name__ == "__main__":
    driver = init_driver()
    select_station(driver, 'Москва', 'Пушкино')
