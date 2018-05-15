from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import *

import time
from datetime import datetime
import config as c
import ccgen
import pymssql
import sys

max_wait = 25 # максимальное ожидание браузера
mc_prefix = ['5','1','3','7','5']
visa_prefix = ['4','1','2','5','1']

iter = 30;

# Функция выполняющая запрос в SQL
def execute_db(host,user,password,db,request):
    res = []
    conn = pymssql.connect(host, user, password, db)
    #print("aloha db!\n")
    cur = conn.cursor()
    cur.execute(request)

    for row in cur:
        #print(row)
        res.append(row)
    conn.close()
    # print(request)
    return res

# Функция генерации уникального номера карты
def new_card(input_prefix):

    digs = (str(datetime.now()))[5:7] + (str(datetime.now()))[8:10] + \
           (str(datetime.now()))[11:13] + (str(datetime.now()))[14:16] + (str(datetime.now()))[17:19]

    prefix = input_prefix
    for elem in digs:
        prefix.append(elem)

    card = ccgen.credit_card_number_2(prefix, 16,1)
    # print(card)

    return card

# Функция ожидания загрузки элемента на странице
def wait_form(driver, type, path, one_time, max_time, final_text):
    flag1 = 0
    while (True):
        if flag1 == max_time:
            print(final_text + "\n")
            break
            driver.close()
            sys.exit(1)
        else:
            try:
                if type == "xpath":
                    driver.find_element_by_xpath(path).click()
                if type == "id":
                    driver.find_element_by_id(path).click()
                break
            except ElementNotVisibleException:  # NoSuchElementException:
                time.sleep(one_time)
                flag1 += 1
            except NoSuchElementException:
                time.sleep(one_time)
                flag1 += max_time
                final_text += "Элемент не найден\n"
    if flag1 > 1:
        print("Ожидали %d раз(а) по %d секунды" % (flag1, one_time))



if len(sys.argv) < 3:
    print("Ошибка. Вы не ввели необходимые параметры: тестовая среда, ucdb_id")
    sys.exit(1)

else:
    if len(sys.argv[1]) > 2:
        print("Ошибка. Вы ввели некорректную тестовую среду")
        sys.exit(1)
    else:
        if sys.argv[1] == 't1' or sys.argv[1] == '1':
            test = 1
            url = c.url1
        else:
            test = 3
            url = c.url3
    if len(sys.argv[2]) != 10:
        print("Ошибка. Проверьте корректность ucdb_id")
        sys.exit(1)
    else:
        ucdb_id = sys.argv[2]

        if test == 1:
            my_host = c.test1_sql
        else:
            my_host = c.test3_sql

        phone = execute_db(my_host, c.my_user, c.my_password, c.my_db, c.req.replace("REPLACE", ucdb_id))

        if (not phone):
            print("Ошибка. Не найдена пара: ucdb_id - телефон")
            sys.exit(1)

        else:
            print("UCDB_ID: %s, Phone: %s" % (ucdb_id,phone[0][0]))

            d1 = webdriver.Chrome()
            d1.implicitly_wait(max_wait)
            d1.get(url)

            elem = d1.find_element_by_xpath(".//*[@id='ucdb']").send_keys(ucdb_id)
            elem = d1.find_element_by_xpath(".//*[@id='phone']").send_keys(phone[0][0])

            d1.find_element_by_xpath(".//*[@id='submit_step1']").click()

            wait_form(d1, "xpath", ".//*[@id='credit_card_number']", 3, 30, "Форма регистрации карты не загружается")

            card = new_card(visa_prefix)
            cvv2 = "123"
            hold_sum = "1.5"
            print("Card: %s" % card)

            d1.find_element_by_xpath(".//*[@id='credit_card_number']").send_keys(card)

            select = Select(d1.find_element_by_css_selector("select#expire_month"))
            select.select_by_index(3)
            # .//*[@id='expire_month-styler']/div[1]/div[1]
            # .//*[@id='expire_month-styler']/div[1]/div[2]/div

            select = Select(d1.find_element_by_css_selector("select#expire_year"))
            select.select_by_visible_text("2018")
            # .//*[@id='expire_year-styler']/div[1]/div[1]
            # .//*[@id='expire_year-styler']/div[1]/div[2]/div

            d1.find_element_by_xpath(".//*[@id='cardholder']").send_keys("Ivan Ivanov")

            d1.find_element_by_xpath(".//*[@id='cvv2']").send_keys(cvv2)

            time.sleep(2)
            
            d1.find_element_by_xpath(".//*[@id='body']/div[1]/form/div/div[5]/input").click()

            wait_form(d1, "xpath", ".//*[@id='sum_hold']", 3, 30, "Форма ввода холд суммы не загружается")

            time.sleep(3)

            d1.find_element_by_xpath(".//*[@id='sum_hold']").send_keys(hold_sum)

            d1.find_element_by_xpath(".//*[@id='submit_step2']").click()

            #time.sleep(3)

            wait_form(d1, "id", "form_final", 3, 30, "Результат регистрации карты неизвестен")
 

            print(d1.find_element_by_id("form_final").text)


            # d1.close()

