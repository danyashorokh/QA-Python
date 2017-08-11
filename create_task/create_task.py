#! /usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import * #Select
#from selenium webdriver.support.ui import *
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #
from selenium.webdriver.common.by import By #
from selenium.common.exceptions import *
import unittest
import time

import xlrd
import xlwt
#import openpyxl

from datetime import datetime, timedelta
from random import Random
import copy


#------------------------------

# Path to the table excel
file_name = ''

# Clients amount
clients_amount = 1

# First client row in the table
first_row = 1

# Init url's
test1 = ""
test3 = ""

# Method of obtaining a loan
type1 = ""
type2 = ""
type3 = ""

br1 = "Firefox"
br2 = "Chrome"

ecp1 = ""
cvv = ""
hold_sum = ""

# Init settings <-----------------------------
env = test1
t = type1
b = br2

max_wait = 25 # max browser timeout

one_wait = 3
times_wait = 10

#------------------------------
#display = Display(visible=0, size= (1024, 768))
#display.start()


'''
# Excel 2007
#
#vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]

#val = sheet.row_values(0)[0]
#date = sheet.cell_value(0, 0)


# Excel 2010
wb = openpyxl.load_workbook(filename = 'C:/Users/DShorokh/Desktop/selenium_excel.xlsx')
sheet = wb['СПР7']
#
val = sheet['C2'].value
print(val)
#
vals = [v[0].value for v in sheet.range('C2:AT')]
'''

# Waiting for loading element function
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
                final_text += u"  - Элемент не найден\n"
    if flag1 > 1:
        print(u"Ожидали %d раз(а) по %d секунды" % (flag1, one_time))

def scroll_to(driver, type ,path):
    if type == "xpath":
        elem = driver.find_element_by_xpath(path)
    if type == "id":
        elem = driver.find_element_by_css_selector(path)
    loc = elem.location
    point = "window.scrollTo(0, "+str(loc["y"])+")"
    driver.execute_script(point)



regionDict = {
u'Адыгея': {'code': '100000000000', 'region': 'Адыгея (Респ)', 'punkt': 'Город Адыгейск', 'street': 'Абадзехская (ул)'},
u'Алтай': {'code': '400000000000', 'region': 'Алтай (Респ)', 'punkt': 'Город Горно-Алтайск', 'street': 'Набережная (ул)'},
u'Алтайский': {'code': '2200000000000', 'region': 'Алтайский (край)', 'punkt': 'Город Бийск', 'street': 'Набережная (ул)'},
u'Амурская': {'code': '2800000000000', 'region': 'Амурская (обл)', 'punkt': 'Город Благовещенск', 'street': 'Набережная (ул)'},
u'Архангельская': {'code': '2900000000000', 'region': 'Архангельская (обл)', 'punkt': 'Город Архангельск', 'street': 'Бабушкина (ул)'},
u'Астраханская': {'code': '3000000000000', 'region': 'Астраханская (обл)', 'punkt': 'Город Астрахань', 'street': 'Абаканская (ул)'},
u'Байконур': {'code': '9900000000000', 'region': 'Байконур (г)', 'punkt': 'Байконур (г)', 'street': 'Авиационная (ул)'},
'Башкортостан': {'code': '200000000000', 'region': 'Башкортостан (Респ)', 'punkt': 'Город Салават', 'street': 'Набережная (ул)'},
'Белгородская': {'code': '3100000000000', 'region': 'Белгородская (обл)', 'punkt': 'Город Белгород', 'street': 'Декабристов (ул)'},
'Брянская': {'code': '3200000000000', 'region': 'Брянская (обл)', 'punkt': 'Город Брянск', 'street': 'Бабушкина (ул)'},
'Бурятия': {'code': '300000000000', 'region': 'Бурятия (Респ)', 'punkt': 'Город Северобайкальск', 'street': 'Набережная (ул)'},
'Владимирская': {'code': '3300000000000', 'region': 'Владимирская (обл)', 'punkt': 'Город Владимир', 'street': 'Набережная (ул)'},
'Волгоградская': {'code': '3400000000000', 'region': 'Волгоградская (обл)', 'punkt': 'Город Волгоград', 'street': 'Базовая (ул)'},
'Вологодская': {'code': '3500000000000', 'region': 'Вологодская (обл)', 'punkt': 'Город Вологда', 'street': 'Набережная (ул)'},
'Воронежская': {'code': '3600000000000', 'region': 'Воронежская (обл)', 'punkt': 'Город Воронеж', 'street': 'Набережная (ул)'},
'Дагестан': {'code': '500000000000', 'region': 'Дагестан (Респ)', 'punkt': 'Город Махачкала', 'street': 'Набережная (ул)'},
'Еврейская': {'code': '7900000000000', 'region': 'Еврейская (Аобл)', 'punkt': 'Город Биробиджан', 'street': 'Набережная (ул)'},
'Забайкальский': {'code': '7500000000000', 'region': 'Забайкальский (край)', 'punkt': 'Город Чита', 'street': 'Набережная (ул)'},
'Ивановская': {'code': '3700000000000', 'region': 'Ивановская (обл)', 'punkt': 'Город Иваново', 'street': 'Набережная (ул)'},
'Ингушетия': {'code': '600000000000', 'region': 'Ингушетия (Респ)', 'punkt': 'Город Назрань', 'street': 'Набережная (ул)'},
'Иркутская': {'code': '3800000000000', 'region': 'Иркутская (обл)', 'punkt': 'Город Иркутск', 'street': 'Набережная (ул)'},
'Кабардино-Балкарская': {'code': '700000000000', 'region': 'Кабардино-Балкарская (Респ)', 'punkt': 'Город Нальчик', 'street': 'Балкарова (ул)'},
'Калининградская': {'code': '3900000000000', 'region': 'Калининградская (обл)', 'punkt': 'Город Калининград', 'street': 'Бабаева (ул)'},
'Калмыкия': {'code': '800000000000', 'region': 'Калмыкия (Респ)', 'punkt': 'Город Элиста', 'street': 'Автомобилистов (ул)'},
'Калужская': {'code': '4000000000000', 'region': 'Калужская (обл)', 'punkt': 'Город Калуга', 'street': 'Набережная (ул)'},
'Камчатский': {'code': '4100000000000', 'region': 'Камчатский (край)', 'punkt': 'Город Петропавловск-Камчатский', 'street': 'Набережная (ул)'},
'Карачаево-Черкесская': {'code': '900000000000', 'region': 'Карачаево-Черкесская (Респ)', 'punkt': 'Город Карачаевск', 'street': 'Базарная (ул)'},
'Карелия': {'code': '1000000000000', 'region': 'Карелия (Респ)', 'punkt': 'Город Петрозаводск', 'street': 'Бабушкина (ул)'},
'Кемеровская': {'code': '4200000000000', 'region': 'Кемеровская (обл)', 'punkt': 'Город Кемерово', 'street': 'Базовая (ул)'},
'Кировская': {'code': '4300000000000', 'region': 'Кировская (обл)', 'punkt': 'Город Киров', 'street': 'Набережная (ул)'},
'Коми': {'code': '1100000000000', 'region': 'Коми (Респ)', 'punkt': 'Город Воркута', 'street': 'Набережная (ул)'},
'Костромская': {'code': '4400000000000', 'region': 'Костромская (обл)', 'punkt': 'Город Волгореченск', 'street': 'Набережная (ул)'},
'Краснодарский': {'code': '2300000000000', 'region': 'Краснодарский (край)', 'punkt': 'Город Краснодар', 'street': 'Базарная (ул)'},
'Красноярский': {'code': '2400000000000', 'region': 'Красноярский (край)', 'punkt': 'Город Красноярск', 'street': 'Набережная (ул)'},
'Крым': {'code': '9100000000000', 'region': 'Крым (Респ)', 'punkt': 'Город Симферополь', 'street': 'Набережная (ул)'},
'Курганская': {'code': '4500000000000', 'region': 'Курганская (обл)', 'punkt': 'Город Курган', 'street': 'Набережная (ул)'},
'Курская': {'code': '4600000000000', 'region': 'Курская (обл)', 'punkt': 'Город Курск', 'street': 'Фабричная (ул)'},
'Ленинградская': {'code': '4700000000000', 'region': 'Ленинградская (обл)', 'punkt': 'Город Сосновый Бор', 'street': 'Набережная (ул)'},
'Липецкая': {'code': '4800000000000', 'region': 'Липецкая (обл)', 'punkt': 'Город Липецк', 'street': 'Набережная (ул)'},
'Магаданская': {'code': '4900000000000', 'region': 'Магаданская (обл)', 'punkt': 'Город Магадан', 'street': 'Левонабережная (ул)'},
'Марий Эл': {'code': '1200000000000', 'region': 'Марий Эл (Респ)', 'punkt': 'Город Йошкар-Ола', 'street': 'Набережная (ул)'},
'Мордовия': {'code': '1300000000000', 'region': 'Мордовия (Респ)', 'punkt': 'Город Саранск', 'street': 'Балтийская (ул)'},
'Москва': {'code': '7700000000000', 'region': 'Москва (г)', 'punkt': 'Город Москва', 'street': 'Набережная (ул)'},
'Московская': {'code': '5000000000000', 'region': 'Московская (обл)', 'punkt': 'Город Балашиха', 'street': 'Живописная (ул)'},
'Мурманская': {'code': '5100000000000', 'region': 'Мурманская (обл)', 'punkt': 'Город Мурманск', 'street': 'Набережная (ул)'},
'Ненецкий': {'code': '8300000000000', 'region': 'Ненецкий (АО)', 'punkt': 'Город Нарьян-Мар', 'street': 'Набережная (ул)'},
'Нижегородская': {'code': '5200000000000', 'region': 'Нижегородская (обл)', 'punkt': 'Город Нижний Новгород', 'street': 'Баженова (ул)'},
'Новгородская': {'code': '5300000000000', 'region': 'Новгородская (обл)', 'punkt': 'Город Великий Новгород', 'street': 'Балтийская (ул)'},
'Новосибирская': {'code': '5400000000000', 'region': 'Новосибирская (обл)', 'punkt': 'Город Новосибирск', 'street': 'Набережная (ул)'},
'Омская': {'code': '5500000000000', 'region': 'Омская (обл)', 'punkt': 'Город Омск', 'street': 'Бабушкина (ул)'},
'Оренбургская': {'code': '5600000000000', 'region': 'Оренбургская (обл)', 'punkt': 'Город Оренбург', 'street': 'Набережная (ул)'},
'Орловская': {'code': '5700000000000', 'region': 'Орловская (обл)', 'punkt': 'Город Орёл', 'street': 'Базовая (ул)'},
'Пензенская': {'code': '5800000000000', 'region': 'Пензенская (обл)', 'punkt': 'Город Пенза', 'street': 'Бажова (ул)'},
'Пермский': {'code': '5900000000000', 'region': 'Пермский (край)', 'punkt': 'Город Пермь', 'street': 'Набережная (ул)'},
'Приморский': {'code': '2500000000000', 'region': 'Приморский (край)', 'punkt': 'Город Находка', 'street': 'Набережная (ул)'},
'Псковская': {'code': '6000000000000', 'region': 'Псковская (обл)', 'punkt': 'Город Псков', 'street': 'Балтийская (ул)'},
'Ростовская': {'code': '6100000000000', 'region': 'Ростовская (обл)', 'punkt': 'Город Ростов-на-Дону', 'street': 'Набережная (ул)'},
'Рязанская': {'code': '6200000000000', 'region': 'Рязанская (обл)', 'punkt': 'Город Рязань', 'street': 'Бабушкина (ул)'},
'Самарская': {'code': '6300000000000', 'region': 'Самарская (обл)', 'punkt': 'Город Тольятти', 'street': 'Базовая (ул)'},
'Санкт-Петербург': {'code': '7800000000000', 'region': 'Санкт-Петербург (г)', 'punkt': 'Город Санкт-Петербург', 'street': 'Бабушкина (ул)'},
'Саратовская': {'code': '6400000000000', 'region': 'Саратовская (обл)', 'punkt': 'Город Саратов', 'street': 'Набережная (ул)'},
'Саха /Якутия/': {'code': '1400000000000', 'region': 'Саха /Якутия/ (Респ)', 'punkt': 'Город Якутск', 'street': 'Набережная (ул)'},
'Сахалинская': {'code': '6500000000000', 'region': 'Сахалинская (обл)', 'punkt': 'Город Южно-Сахалинск', 'street': 'Набережная (ул)'},
'Свердловская': {'code': '6600000000000', 'region': 'Свердловская (обл)', 'punkt': 'Город Екатеринбург', 'street': 'Бабушкина (ул)'},
'Севастополь': {'code': '9200000000000', 'region': 'Севастополь (г)', 'punkt': 'Севастополь (г)', 'street': 'Бакинская (ул)'},
'Северная Осетия - Алания': {'code': '1500000000000', 'region': 'Северная Осетия - Алания (Респ)', 'punkt': 'Город Владикавказ', 'street': 'Бакинская (ул)'},
'Смоленская': {'code': '6700000000000', 'region': 'Смоленская (обл)', 'punkt': 'Город Смоленск', 'street': 'Бакунина (ул)'},
'Ставропольский': {'code': '2600000000000', 'region': 'Ставропольский (край)', 'punkt': 'Город Ставрополь', 'street': 'Мира (ул)'},
'Тамбовская': {'code': '6800000000000', 'region': 'Тамбовская (обл)', 'punkt': 'Город Тамбов', 'street': 'Набережная (ул)'},
'Татарстан': {'code': '1600000000000', 'region': 'Татарстан (Респ)', 'punkt': 'Город Казань', 'street': 'Набережная (ул)'},
'Тверская': {'code': '6900000000000', 'region': 'Тверская (обл)', 'punkt': 'Город Тверь', 'street': 'Бакунина (ул)'},
'Томская': {'code': '7000000000000', 'region': 'Томская (обл)', 'punkt': 'Город Томск', 'street': 'Бакунина (ул)'},
'Тульская': {'code': '7100000000000', 'region': 'Тульская (обл)', 'punkt': 'Город Тула', 'street': 'Набережная (ул)'},
'Тыва': {'code': '1700000000000', 'region': 'Тыва (Респ)', 'punkt': 'Город Кызыл', 'street': 'Набережная (ул)'},
'Тюменская': {'code': '7200000000000', 'region': 'Тюменская (обл)', 'punkt': 'Город Тюмень', 'street': 'Набережная (ул)'},
'Удмуртская': {'code': '1800000000000', 'region': 'Удмуртская (Респ)', 'punkt': 'Город Глазов', 'street': 'Барышникова (ул)'},
'Ульяновская': {'code': '7300000000000', 'region': 'Ульяновская (обл)', 'punkt': 'Город Ульяновск', 'street': 'Набережная (ул)'},
'Хабаровский': {'code': '2700000000000', 'region': 'Хабаровский (край)', 'punkt': 'Город Хабаровск', 'street': 'Набережная (ул)'},
'Хакасия': {'code': '1900000000000', 'region': 'Хакасия (Респ)', 'punkt': 'Город Абакан', 'street': 'Набережная (ул)'},
'Ханты-Мансийский Автономный округ - Югра': {'code': '8600000000000', 'region': 'Ханты-Мансийский Автономный округ - Югра (АО)', 'punkt': 'Город Ханты-Мансийск', 'street': 'Набережная (ул)'},
'Челябинская': {'code': '7400000000000', 'region': 'Челябинская (обл)', 'punkt': 'Город Челябинск', 'street': 'Набережная (ул)'},
'Чеченская': {'code': '2000000000000', 'region': 'Чеченская (Респ)', 'punkt': 'Город Грозный', 'street': 'Набережная (ул)'},
'Чувашская Республика - (Чувашия)': {'code': '2100000000000', 'region': 'Чувашская Республика - (Чувашия)', 'punkt': 'Город Чебоксары', 'street': 'Бабушкина (ул)'},
'Чукотский': {'code': '8700000000000', 'region': 'Чукотский (АО)', 'punkt': 'Город Анадырь', 'street': 'Набережная (ул)'},
'Ямало-Ненецкий': {'code': '8900000000000', 'region': 'Ямало-Ненецкий (АО)', 'punkt': 'Город Салехард', 'street': 'Набережная (ул)'},
'Ярославская': {'code': '7600000000000', 'region': 'Ярославская (обл)', 'punkt': 'Город Ярославль', 'street': 'Базовая (ул)'}
}

# Элементы 1ой страницы
sum = []
lastname = []
name = []
patronymic = []
date_birthday = []
nationality = []
rf_perm_region = []
region = []
mobile_phone = []
email = []

# Элементы 2ой страницы
sex = []
prev_lastname = []
s = []
n = []
sn_passport = []
code_passport = []
date_passport = []
where_passport = []
place_birthday = []
region_live = []
punkt_live = []
street_live = []
home_live = []
str_live = []
korp_live = []
flat_live = []
stac_phone = []
live_reg_flag = []

# Элементы 3ей страницы
type_work = []
company_name = []
company_view = []
company_status = []
company_start = []
work_phone = []
region_work = []
punkt_work = []
street_work = []
home_work = []
str_work = []
korp_work = []
flat_work = []
work_stag = []
last_stag = []
income_work = []
income_add = []
payment_house = []
payment_credit = []
payment_other = []
loan_purpose = []
education = []
family_status = []
partner_lastname = []
partner_name = []
partner_patronymic = []
partner_birthday = []
partner_income = []
partner_credit = []
number_dep = []
number_child = []
contacts_name = []
contacts_status = []
contacts_phone = []

# Функции для генерации номера карты
mc_prefix = ['5','1','3','7','6']
visa_prefix = ['4','1','2','5','4']


def completed_number(prefix, length):

    generator = Random()
    generator.seed()

    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1):
        digit = str(generator.choice(range(0, 10)))
        #digit = str(0)
        ccnumber.append(digit)


    # Calculate sum

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    mynumber = ccnumber

    while pos < length - 1:

        if (pos % 2 == 0):
            odd = int(mynumber[pos]) * 2
            if odd > 9:
                odd -= 9
            sum += odd
        else: sum += int(mynumber[pos])

        pos += 1

    # Calculate check digit
    checkdigit = sum % 10
    #print(checkdigit)
    if(checkdigit == 0):
        checkdigit = 0
    else: checkdigit = 10 - checkdigit

    ccnumber.append(str(checkdigit))
    return ''.join(ccnumber)
def credit_card_number(prefix, length, amount):

    result = []
    i = 0

    while i < amount:

        ccnumber = copy.copy(prefix)
        result.append(completed_number(ccnumber, length))
        i += 1

    return result

# Функция для конвертирования форматы даты из excel
def convert_date(date):
    '''
    day = ""
    month = ""
    date = datetime(*xlrd.xldate_as_tuple(date, 0))
    day = str(date.day)
    if (len(day) == 1): day = "0" + day
    month = str(date.month)
    if (len(month) == 1): month = "0" + month
    date = day + "." + month + "." + str(date.year)
    '''

    el = date.split("-")
    date = el[2]+"."+el[1]+"."+el[0]

    return date

# Функция для копирования данных из таблицы excel в словарь clients
def copy_from_excel(file_name, active_list, keys_row, start_row, clients_amount):
    # Работа с файлом Excel 2007
    # открываем файл 2007
    rb = xlrd.open_workbook(file_name, formatting_info=True)
    # выбираем активный лист
    sheet = rb.sheet_by_index(active_list)

    clients = []
    # client = {}

    # получаем ключи из таблицы
    keys = sheet.row_values(keys_row)

    # получаем данные по клиенту в соответствии с ключами
    for i in range(0, clients_amount):
        client = {}
        values = sheet.row_values(start_row)
        for key, value in zip(keys, values):
            client[key] = value


        # Для дат необходимо выполнить преобразования
        if (client['ДАТА РОЖДЕНИЯ']!= "NULL"):
            client['ДАТА РОЖДЕНИЯ'] = convert_date(client['ДАТА РОЖДЕНИЯ'])
        if (client['Дата выдачи'] != "NULL"):
            client['Дата выдачи'] = convert_date(client['Дата выдачи'])
        if (client['Длительность работы в данной организации'] != "NULL"):
            client['Длительность работы в данной организации'] = convert_date(client['Длительность работы в данной организации'])
        if (client['Дата рождения Супруга'] != "NULL"):
            client['Дата рождения Супруга'] = convert_date(client['Дата рождения Супруга'])


        clients.append(client)
        start_row += 1

    return clients

# Функция для корректирования данных в словаре cleints
def correct_fields(dict, key, value):
    for item in dict:
        item[key] = value
    return dict

# Функция заполнения 1ой страницы заявки
def fill_1_page(driver, test_env, sum, term, lastname, name, patronymic, date_birthday, nationality, rf_perm_region, region, mobile_phone, email):

    #driver = webdriver.Firefox()
    #driver.get(test_env)

    # Сумма займа
    elem = driver.find_element_by_xpath(".//*[@id='sum']")
    elem.click()
    for i in range(0,6):
        elem.send_keys(Keys.BACKSPACE)
    elem.click()
    elem.send_keys(sum)
    elem.send_keys(Keys.ENTER)

    #elem.send_keys(sum)
    #elem.send_keys(Keys.ENTER)

    # Срок займа
    #elem = driver.find_element_by_xpath(".//*[@id='term']")
    #elem.click()
    #elem.send_keys(term)

    # Мобильный телефон
    elem = driver.find_element_by_xpath(".//*[@id='mobile_phone']")
    elem.click()
    elem.send_keys(mobile_phone)

    # Фамилия
    elem = driver.find_element_by_xpath(".//*[@id='lastname']")
    elem.click()
    elem.send_keys(lastname)

    # Имя
    elem = driver.find_element_by_xpath(".//*[@id='name']")
    elem.send_keys(name)

    # Отчество
    elem = driver.find_element_by_xpath(".//*[@id='patronymic']")
    elem.send_keys(patronymic)

    # Дата рождения
    elem = driver.find_element_by_xpath(".//*[@id='date_birthday']")
    elem.click()
    elem.send_keys(date_birthday)

    # Гражданство
    select = Select(driver.find_element_by_css_selector("select#nationality"))
    #select.select_by_visible_text("Российская Федерация")
    if nationality == "РФ":
        select.select_by_index(1)
    else:
        select.select_by_index(2)

    '''
    # Наличие постоянной регистрации
    elems = driver.find_elements_by_name("registration")
    #driver.execute_script("return arguments[0].scrollIntoView();", elems)
    driver.execute_script("window.scrollBy(0, -10);")

    if (rf_perm_region == "yes"):
        for option in elems:
            if option.get_attribute("value") == "1":
                #driver.execute_script("return arguments[0].scrollIntoView();", option)
                option.click()
    else:
        for option in elems:
            if option.get_attribute("value") == "0":
                option.click()
    '''

    elem = driver.find_element_by_xpath(".//*[@id='registration']/label[1]/div")
    elem.click()


    # Регион проживания
    select = Select(driver.find_element_by_css_selector("select#region_residence"))
    #print(select.options)
    select.select_by_visible_text(region)

    # Электронная почта
    elem = driver.find_element_by_xpath(".//*[@id='email']")
    elem.send_keys(email)


# Функция заполнения 2ой страницы заявки
def fill_2_page(driver, sex, prev_lastname, sn_passport, code_passport, date_passport, where_passport, place_birthday, \
                region_live, punkt_live, street_live, home_live, str_live, korp_live, flat_live, stac_phone, live_reg_flag):

    # Пол
    if (sex == "М"):
        elem = driver.find_element_by_xpath(".//*[@id='sex']/label[1]/div")
    else:
        elem = driver.find_element_by_xpath(".//*[@id='sex']/label[2]/div")
    elem.click()

    # Предыдущая фамилия
    if(prev_lastname) != "NULL":
        elem = driver.find_element_by_xpath(".//*[@id='prev_lastname']")
        elem.send_keys(prev_lastname)

    # Серия и номер паспорта
    elem = driver.find_element_by_xpath(".//*[@id='sn_passport']")
    elem.click()
    elem.send_keys(sn_passport)

    # Код подразделения
    elem = driver.find_element_by_xpath(".//*[@id='code_passport']")
    elem.click()
    elem.send_keys(code_passport)

    time.sleep(1)

    # Дата выдачи паспорта
    elem = driver.find_element_by_xpath(".//*[@id='date_passport']")
    elem.click()
    elem.send_keys(date_passport)

    # Кем выдан паспорт
    if driver.find_element_by_xpath(".//*[@id='where_passport']").get_attribute("value") == "Кем выдан":
        driver.find_element_by_xpath(".//*[@id='where_passport']").send_keys(where_passport)


    # Место рождения
    elem = driver.find_element_by_xpath(".//*[@id='place_birthday']")
    elem.send_keys(place_birthday)

    # Регион проживания
    select = Select(driver.find_element_by_css_selector("select#region_live"))
    select.select_by_visible_text(region_live)

    # Населенный пункт
    elem = driver.find_element_by_xpath(".//*[@id='punkt_live']")
    elem.click()
    elem.send_keys(punkt_live)
    elem.send_keys(Keys.ENTER)
    time.sleep(2)


    # Улица
    if(street_live != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='street_live']")
        elem.click()
        for i in range(0, 6):
            elem.send_keys(Keys.BACKSPACE)
        elem.click()
        elem.send_keys(street_live)
        elem.send_keys(Keys.ENTER)

    # Дом
    elem = driver.find_element_by_xpath(".//*[@id='home_live']")
    elem.send_keys(home_live)

    # Строение
    elem = driver.find_element_by_xpath(".//*[@id='str_live']")
    elem.send_keys(str_live)

    # Корпус
    elem = driver.find_element_by_xpath(".//*[@id='korp_live']")
    elem.send_keys(korp_live)

    # Квартира
    elem = driver.find_element_by_xpath(".//*[@id='flat_live']")
    elem.send_keys(flat_live)

    # Домашний телефон
    elem = driver.find_element_by_xpath(".//*[@id='stac_phone']")
    elem.click()
    elem.send_keys(stac_phone)

    # Фактический адрес проживания совпадает с адресом регистрации
    if(live_reg_flag == "yes"):
        elem = driver.find_element_by_xpath(".//*[@id='live_reg_flag-styler']")
        elem.click()
    else: print("error")

# Функция заполнения 3ей страницы заявки
def fill_3_page(driver, type_work, company_name, company_view, company_status, company_start, work_phone, region_work, punkt_work, \
                street_work, home_work, str_work, korp_work, flat_work, work_stag, last_stag, income_work, income_add, \
                payment_house, payment_credit, payment_other, loan_purpose, education, family_status, partner_lastname, partner_name, \
                partner_patronymic, partner_birthday, partner_income, partner_credit, number_dep, number_child, contacts_name, contacts_status, contacts_phone):

    # Тип занятости
    elem = driver.find_element_by_css_selector("select#type_work")
    elem.send_keys(type_work)
    elem.send_keys(Keys.ENTER)
    #select = Select(driver.find_element_by_css_selector("select#type_work"))
    #select.select_by_visible_text(type_work)
    #select.select_by_value(type_work)
    #select.s

    # print(company_name)
    # Название компании
    if(company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='company_name']")
        elem.click()
        elem.send_keys(company_name)

    # print(company_view)
    # Вид деятельности компании
    if (company_view != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#company_view"))
        select.select_by_visible_text(company_view)

    # print(company_status)
    # Занимаемая должность
    if (company_status != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#company_status"))
        select.select_by_visible_text(company_status)


    # print(company_start)
    # Начало работы в организации
    if (company_start != "NULL"):
        company_start = company_start[3:]
        elem = driver.find_element_by_xpath(".//*[@id='company_start']")
        elem.click()
        elem.send_keys(company_start)

    # print(work_phone)
    # Рабочий телефон
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='work_phone']")
        elem.send_keys(work_phone)

    # print(region_work)
    # Регион рабочего адреса
    if (company_name != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#region_work"))
        select.select_by_visible_text(region_work)

    # print(punkt_work)
    # Населенный пункт
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='punkt_work']")
        elem.click()
        elem.send_keys(punkt_work)
        elem.send_keys(Keys.ENTER)
        time.sleep(2)

    # print(street_work)
    # Улица
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='street_work']")
        elem.click()
        for i in range(0, 6):
            elem.send_keys(Keys.BACKSPACE)
        elem.click()
        elem.send_keys(street_work)
        elem.send_keys(Keys.ENTER)

    # print(home_work)
    # Дом
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='home_work']")
        elem.send_keys(home_work)

    # print(str_work)
    # Строение
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='str_work']")
        elem.send_keys(str_work)

    # print(korp_work)
    # Корпус
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='korp_work']")
        elem.send_keys(korp_work)

    # print(flat_work)
    # Квартира
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='flat_work']")
        elem.send_keys(flat_work)

    # Общий трудовой стаж
    #if (work_stag != "NULL"):
    #    elem = driver.find_element_by_css_selector("input#work_stag")
    #    elem.send_keys(work_stag)

    # Длительность работы на прежнем месте
    #if (last_stag != "NULL"):
    #    elem = driver.find_element_by_css_selector("input#last_stag")
    #    elem.send_keys(last_stag)

    # print(income_work)
    # Доход по месту работы
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='income_work']")
        elem.send_keys(income_work)

    # print(income_add)
    # Дополнительный доход
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='income_add']")
        elem.send_keys(income_add)

    # print(payment_house)
    # Расходы на жилье
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='payment_house']")
        elem.send_keys(payment_house)

    # print(payment_credit)
    # Выплаты по кредитам
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='payment_credit']")
        elem.send_keys(payment_credit)

    # print(payment_other)
    # Прочие финансовые обязательства
    if (company_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='payment_other']")
        elem.send_keys(payment_other)

    # print(loan_purpose)
    # Цель займа
    if (loan_purpose != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#loan_purpose"))
        select.select_by_visible_text(loan_purpose)

    # print(education)
    # Образование
    if (education != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#education"))
        select.select_by_visible_text(education)

    # print(family_status)
    # Семейное положение
    if (family_status != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#family_status"))
        select.select_by_visible_text(family_status)

    # print(partner_lastname)
    # Фамилия супруга(и)
    if (partner_lastname != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='partner_lastname']")
        elem.send_keys(partner_lastname)

    # Имя супруга(и)
    if (partner_lastname != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='partner_name']")
        elem.send_keys(partner_name)

    # Отчество супруга(и)
    if (partner_lastname != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='partner_patronymic']")
        elem.send_keys(partner_patronymic)

    # Дата рождения супруга(и)
    if (partner_lastname != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='partner_birthday']")
        elem.click()
        elem.send_keys(partner_birthday)

    # Доход супруга(и)
    if (partner_lastname != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='partner_income']")
        elem.send_keys(partner_income)

    # Выплаты по кредитам супруга(и)
    if (partner_lastname != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='partner_credit']")
        elem.send_keys(partner_credit)

    # Количество иждивенцев
    if (number_dep != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='number_dep']")
        elem.click()
        elem.send_keys(number_dep)

    # Количество детей
    if (number_child != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='number_child']")
        elem.send_keys(number_child)

    # Контактное лицо
    if (contacts_name != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='contacts_name']")
        elem.send_keys(contacts_name)

    # Кем приходится контактное лицо
    if (contacts_status != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#contacts_status"))
        select.select_by_visible_text(contacts_status)

    # Телефон контактного лица
    if (contacts_phone != "NULL"):
        elem = driver.find_element_by_xpath(".//*[@id='contacts_phone']")
        elem.click()
        elem.send_keys(contacts_phone)

def choose_type_receive(driver,type_receive):


    if (type_receive == "Карта"):
        elem = driver.find_element_by_xpath(".//*[@id='type16_wrapper']/td[1]/label/div")
    elif(type_receive == "Контакт"):
        elem = driver.find_element_by_xpath(".//*[@id='type2_wrapper']/td[1]/label/div")
    elif(type_receive == "Юнистрим"):
        elem = driver.find_element_by_xpath(".//*[@id='type4_wrapper']/td[1]/label/div")
    elem.click()

def fill_cc(driver, credit_card, expire_month, expire_year, cardholder, cvc2):

    # Номер карты
    elem = driver.find_element_by_xpath(".//*[@id='credit_card_number']")
    elem.send_keys(credit_card)
    # .//*[@id='credit_card_number']

    # .//*[@id='body']/div[1]/form/div/div[5]/input

    # .//*[@id='card_sum']

    # .//*[@id='submit-step5_16']

    # Срок действия карты: месяц
    select = Select(driver.find_element_by_css_selector("select#expire_month"))
    if expire_month == "Январь":
        select.select_by_index(0)
    elif expire_month == "Февраль":
        select.select_by_index(1)
    elif expire_month == "Март":
        select.select_by_index(2)
    elif expire_month == "Апрель":
        select.select_by_index(3)
    elif expire_month == "Май":
        select.select_by_index(4)
    elif expire_month == "Июнь":
        select.select_by_index(5)
    elif expire_month == "Июль":
        select.select_by_index(6)
    elif expire_month == "Август":
        select.select_by_index(7)
    elif expire_month == "Сентябрь":
        select.select_by_index(8)
    elif expire_month == "Октябрь":
        select.select_by_index(9)
    elif expire_month == "Ноябрь":
        select.select_by_index(10)
    elif expire_month == "Декабрь":
        select.select_by_index(11)

    # Срок действия карты: год
    select = Select(driver.find_element_by_css_selector("select#expire_year"))
    select.select_by_visible_text(expire_year)

    # Владелец карты
    elem = driver.find_element_by_xpath(".//*[@id='cardholder']")
    elem.click()
    elem.send_keys(cardholder)

    # Код CVC+
    elem = driver.find_element_by_xpath(".//*[@id='cvv2']")
    elem.send_keys(cvc2)

def fill_hold_sum(driver,sum):

    try:
        elem = driver.find_element_by_css_selector("#input#card_sum")
        elem.send_keys(sum)
    except: pass

def get_region(adr):
    reg_key = ""
    first_div = adr.find(",",0,len(adr))
    second_div = adr.find(",", first_div+1, len(adr))
    if first_div == 6 and adr[0:first_div] != "Москва" and adr[0:first_div] != "Адыгея":
        reg_key = adr[first_div+2:second_div]
    else: 
        reg_key = adr[0:first_div]
    #print(first_div, second_div)
    #print(reg_key)
    return reg_key


# Выбор региона присутствия true/false
rp = 2
reg_rp = "Московская (обл)"
reg_not_rp = "Тамбовская (обл)"
reg_real = ""
punkt_rp = "Дачный поселок Березка (Шатурский р-н)"
punkt_not_rp = "Выселки(ок) Никольские (Рассказовский р-н)"
punkt_real = ""
street_rp = "NULL"
street_not_rp = "NULL"
street_real = ""

# Копируем в словарь clients данные из таблицы
# входные данные: путь к таблице, номер листа с данными, номер строки с ключами, номер строки с данными первого клиента, количество клиентов (от первого подряд)
clients = copy_from_excel(file_name, 0, 0, first_row, clients_amount)

# Изменяем данные о доходах для прохождения СПР
#check_key = 'Доход по основному месту работы'
#for item in clients:
#    if int(item[check_key]) < 70000:
#        item[check_key] = str(70000.0)

#print(clients[0]['ФАМИЛИЯ'],clients[0]['ИМЯ'],clients[0]['ОТЧЕСТВО'],clients[0]['Доход по основному месту работы'],clients[0]['Расходы на жилье и коммунальные платежи'])
#print()
#print(clients[0]['Количестов иждивенцев'],clients[0]['Количестов детей'])


# Инициализация полей
for i in range(0, clients_amount):
    sum.append("20000")
    lastname.append(clients[i]['ФАМИЛИЯ'])
    name.append(clients[i]['ИМЯ'])
    patronymic.append(clients[i]['ОТЧЕСТВО'])
    date_birthday.append(clients[i]['ДАТА РОЖДЕНИЯ'])
    nationality.append(clients[i]['ГРАЖДАНСТВО'])
    rf_perm_region.append("yes")

    #print(clients[i]['Адрес Проживания'])
    adr_key = get_region(clients[i]['Адрес Проживания'])
    #print(adr_key)
    reg_real = regionDict[adr_key]['region']
    #print(reg_real)
    punkt_real = regionDict[adr_key]['punkt']
    #print(punkt_real)
    street_real = regionDict[adr_key]['street']
    #print(street_real)

    if(rp == 0): region.append(reg_rp)
    elif(rp == 1): region.append(reg_not_rp)
    elif(rp == 2): region.append(reg_real)
    else: print("var rp isn't correct")
    mobile_phone.append(str(clients[i]['Мобильный телефон'])[2:12])
    email.append("dshorokh@migcredit.ru")
    #------------------------------
    sex.append(clients[i]['ПОЛ'])
    prev_lastname.append(clients[i]['ПРЕДЫДУЩАЯ ФАМИЛИЯ'])
    s1 = str(clients[i]['СЕРИЯ ПАСПОРТА'])[:3]
    if (len(s1)<4): s1 += "0" * (4-len(s1))
    s.append(s1)
    n1 = (str(clients[i]['НОМЕР ПАСПОРТА']))[:5]
    if (len(n1)<6): n1 += "0" * (6-len(n1))
    n.append(n1)
    sn_passport.append(s1 + " " + n1)
    code_passport.append(clients[i]['Код подразделения'])
    date_passport.append(clients[i]['Дата выдачи'])
    where_passport.append(clients[i]['Кем выдан'])
    place_birthday.append(clients[i]['МЕСТО РОЖДЕНИЯ'])
    if(rp == 0): 
        region_live.append(reg_rp)
        punkt_live.append(punkt_rp)
        street_live.append(street_rp)
    elif(rp == 1): 
        region_live.append(reg_not_rp)
        punkt_live.append(punkt_not_rp)
        street_live.append(street_not_rp)
    elif(rp == 2): 
        region_live.append(reg_real)
        punkt_live.append(punkt_real)
        street_live.append(street_real)
    else: print("var rp isn't correct")
    home_live.append("1")
    str_live.append("2")
    korp_live.append("3")
    flat_live.append("4")
    stac_phone.append(str(clients[i]['Домашний телефон'])[2:12])
    live_reg_flag.append("yes")
    #------------------------------
    type_work.append(clients[i]['Тип Занятости'])
    company_name.append(clients[i]['Название Компании'])
    company_view.append(clients[i]['Вид деятельности Компании'])
    company_status.append(clients[i]['Позиция в организации'])
    company_start.append(str(clients[i]['Длительность работы в данной организации']))
    work_phone1 = str(clients[i]['Рабочий телефон'])
    if (work_phone1 != "NULL"):
        work_phone1 = work_phone1[2:12]
    work_phone.append(work_phone1)
    if(rp == 0): 
        region_work.append(reg_rp)
        punkt_work.append(punkt_rp)
        street_work.append(street_rp)
    if(rp == 1): 
        region_work.append(reg_not_rp)
        punkt_work.append(punkt_not_rp)
        street_work.append(street_not_rp)
    if(rp == 2): 
        region_work.append(reg_real)
        punkt_work.append(punkt_real)
        street_work.append(street_real)
    else: print("var rp isn't correct")  
    home_work.append("4")
    str_work.append("3")
    korp_work.append("2")
    flat_work.append("1")
    work_stag1 = str(clients[i]['Общий трудовой стаж'])
    if(work_stag1 != "NULL" and work_stag1.find(".",0,len(work_stag1)) > 0): work_stag1 = work_stag1[0:-2]
    work_stag.append(work_stag1)
    last_stag1 = str(clients[i]['Стаж работы на предыдущем месте'])
    if(last_stag1 != "NULL" and last_stag1.find(".",0,len(last_stag1)) > 0): last_stag1 = last_stag1[0:-2]
    last_stag.append(last_stag1)
    income_work1 = str(clients[i]['Доход по основному месту работы'])
    if(income_work1 != "NULL" and income_work1.find(".",0,len(income_work1)) > 0):
        income_work1 = income_work1[0:-2]
    income_work.append(income_work1)
    income_add1 = str(clients[i]['Сумма дополнительных личных доходов'])
    if(income_add1 != "NULL" and income_add1.find(".",0,len(income_add1)) > 0): #income_add1 = income_add1[0:-2]
        income_add1 = income_add1[0:-2]
    income_add.append(income_add1)
    payment_house1 = str(clients[i]['Расходы на жилье и коммунальные платежи'])
    if(payment_house1 != "NULL" and payment_house1.find(".",0,len(payment_house1)) > 0): #payment_house1 = payment_house1[0:-2]
        payment_house1 = payment_house1[0:-2]
    payment_house.append(payment_house1)
    payment_credit1 = str(clients[i]['Выплаты клиента по кредитам'])
    if(payment_credit1 != "NULL" and payment_credit1.find(".",0,len(payment_credit1)) > 0): #payment_credit1 = payment_credit1[0:-2]
        payment_credit1 = payment_credit1[0:-2]
    payment_credit.append(payment_credit1)
    payment_other1 = str(clients[i]['Прочие финансовые обязательства'])
    if(payment_other1 != "NULL" and payment_other1.find(".",0,len(payment_other1)) > 0): #payment_other1 = payment_other1[0:-2]
        payment_other1 = payment_other1[0:-2]
    payment_other.append(payment_other1)
    loan_purpose.append(clients[i]['Цель получения займа'])
    education.append(clients[i]['Образование'])
    family_status.append(clients[i]['Семейное положение'])
    partner_lastname.append(clients[i]['Отчество Супруга'])         # Перепутано в excel
    partner_name.append(clients[i]['Фамилия Супруга'])              # Перепутано в excel
    partner_patronymic.append(clients[i]['Имя Супруга'])            # Перепутано в excel
    partner_birthday.append(clients[i]['Дата рождения Супруга'])
    partner_income1 = str(clients[i]['Доход супруга'])
    if(partner_income1 != "NULL" and partner_income1.find(".",0,len(partner_income1)) > 0):
        partner_income1 = partner_income1[0:-2]
    partner_income.append(partner_income1)
    partner_credit1 = str(clients[i]['Выплаты супруга по кредитам'])
    if(partner_credit1 != "NULL" and partner_credit1.find(".",0,len(partner_credit1)) > 0):
        partner_credit1 = partner_credit1[0:-2]
    partner_credit.append(partner_credit1)
    number_dep.append(str(clients[i]['Количестов иждивенцев']))
    number_child.append(str(clients[i]['Количестов детей']))
    contacts_name.append("Контактное лицо")
    contacts_status.append("Родственник")
    contacts_phone.append("1111111111")

#------------ Создание заявки -------------
for i in range(0, clients_amount):
    print("["+str(i+1)+"]", clients[i]['Адрес Проживания'], clients[i]['ФАМИЛИЯ'], clients[i]['ИМЯ'], clients[i]['ОТЧЕСТВО'],  region_live[i], punkt_live[i], street_live[i])
print()

# Создание копии браузера
ds = []
dsa = []

for i in range(0,clients_amount):
    if b == br1:
        ds.append(webdriver.Firefox())
    elif b == br2:
        ds.append(webdriver.Chrome())
    else:
        print("Выберите корректный браузер")
        break

for i, d in enumerate(ds, start=1):
    d.implicitly_wait(max_wait)

    # Флаг активности браузеров
    dsa.append(True)

# -----------------------------------------

# Процесс создания заявки
for i,d in enumerate(ds,start=1):
    d.get(env)

# Заполнение 1ой страницы
for i,d in enumerate(ds,start=1):
    j = i - 1
    fill_1_page(d, env, sum[j], 0, lastname[j], name[j], patronymic[j], date_birthday[j], nationality[j], \
            rf_perm_region[j], region[j], mobile_phone[j], email[j])

# Переход далее
for i,d in enumerate(ds,start=1):
    scroll_to(d, "xpath", ".//*[@id='submit_step1']")
    d.find_element_by_xpath(".//*[@id='submit_step1']").click()
    print("["+str(i)+"]: 1ая страница заполнена")

for i,d in enumerate(ds,start=1):
    wait_form(d, "xpath", ".//*[@id='smscode']", one_wait, times_wait, "["+str(i)+"]: Форма ввода ЭЦП-1 не загружается")


# ЭЦП-1
for i,d in enumerate(ds,start=1):
    d.find_element_by_xpath(".//*[@id='smscode']").send_keys(ecp1)

# Переход далее
for i,d in enumerate(ds,start=1):
    try:
        scroll_to(d, "xpath", ".//*[@id='submit-step4']")
        d.find_element_by_xpath(".//*[@id='submit-step4']").click()
        print("["+str(i)+"]: Код ЭЦП-1 введен")
    except:
        dsa[i - 1] = False
        print("[" + str(i) + "]: Браузер деактивирован")


for i,d in enumerate(ds,start=1):
    wait_form(d, "xpath", ".//*[@id='sn_passport']", one_wait, times_wait, "["+str(i)+"]: 2 страница не загружается")

# Заполнение 2ой страницы
for i,d in enumerate(ds,start=1):
    j = i - 1
    fill_2_page(d, sex[j], prev_lastname[j], sn_passport[j], code_passport[j], date_passport[j], \
                    where_passport[j], place_birthday[j], \
                    region_live[j], punkt_live[j], street_live[j], home_live[j], str_live[j], korp_live[j],
                    flat_live[j], \
                    stac_phone[j], live_reg_flag[j])


# Переход далее
for i,d in enumerate(ds,start=1):
    try:
        scroll_to(d, "xpath", ".//*[@id='submit_step2']")
        d.find_element_by_xpath(".//*[@id='submit_step2']").click()
        print("["+str(i)+"]: 2ая страница заполнена")
    except:
        dsa[i - 1] = False
        print("[" + str(i) + "]: Браузер деактивирован")

    wait_form(d, "xpath", ".//*[@id='contacts_name']", one_wait, times_wait, "["+str(i)+"]: 3 страница не загружается")




# Заполнение 3ей страницы
for i,d in enumerate(ds,start=1):
    j = i - 1
    fill_3_page(d, type_work[j], company_name[j], company_view[j], company_status[j], company_start[j], \
                    work_phone[j], region_work[j], punkt_work[j], street_work[j], home_work[j], \
                    str_work[j], korp_work[j], flat_work[j], work_stag[j], last_stag[j], income_work[j], income_add[j], \
                    payment_house[j], payment_credit[j], payment_other[j], loan_purpose[j], \
                    education[j], family_status[j], partner_lastname[j], partner_name[j], partner_patronymic[j], \
                    partner_birthday[j], partner_income[j], partner_credit[j], number_dep[j], number_child[j], \
                    contacts_name[j], contacts_status[j], contacts_phone[j])

# Переход далее
for i,d in enumerate(ds,start=1):
    try:
        scroll_to(d, "xpath", ".//*[@id='submit_step3']")
        d.find_element_by_xpath(".//*[@id='submit_step3']").click()
        print("["+str(i)+"]: 3я страница заполнена")
    except:
        dsa[i - 1] = False
        print("[" + str(i) + "]: Браузер деактивирован")

for i,d in enumerate(ds,start=1):
    wait_form(d, "xpath", ".//*[@id='type16_wrapper']/td[1]/label/div", one_wait, 2 * times_wait,
              "["+str(i)+"]: Страница выбора способа получения займа не загружается")



# Выбор способа получения займа
for i,d in enumerate(ds,start=1):
    try:
        choose_type_receive(d, t)
        time.sleep(1)
    except:
        try:
            elem1 = d.find_element_by_id("form_final")
            print("["+str(i)+"]:", elem1.text)
        except:
            print("["+str(i)+"]: Невозможно выбрать способ оплаты")

        dsa[i-1] = False
        print("[" + str(i) + "]: Браузер деактивирован")



# Переход далее
for i,d in enumerate(ds,start=1):
    if dsa[i-1]:
        try:
            scroll_to(d, "xpath", ".//*[@id='submit-step5']")
            d.find_element_by_xpath(".//*[@id='submit-step5']").click()
            print("["+str(i)+"]: Способ получения займа выбран" +": " + t)
        except:
            pass



if t == type1:

    for i, d in enumerate(ds, start=1):
        wait_form(d, "xpath", ".//*[@id='credit_card_number']", one_wait, times_wait,
                  "["+str(i)+"]: Форма ввода данных по карте не загружается")

    # Генерация номера карты
    credit_card = credit_card_number(visa_prefix, 16, clients_amount)
    for i, d in enumerate(ds, start=1):
        print("["+str(i)+"]: Номер сгенерированной карты: ", credit_card[i-1])

    # Ввод данных по карте
    for i, d in enumerate(ds, start=1):
        try:
            fill_cc(d, credit_card[i-1], "Октябрь", "2018", "Ivan Ivanov", cvv)
        except:
            pass

    # Переход далее
    for i, d in enumerate(ds, start=1):
        try:
            elem1 = d.find_element_by_name("submit")
            elem1.click()
            print("["+str(i)+"]: Данные карты введены")
        except:
            pass

    for i, d in enumerate(ds, start=1):
        wait_form(d, "xpath", ".//*[@id='card_sum']", one_wait, 2 * times_wait,
                  "["+str(i)+"] Форма ввода холд суммы не загружается")


    # Ввод холдированной суммы
    for i, d in enumerate(ds, start=1):
        try:
            d.find_element_by_xpath(".//*[@id='card_sum']").send_keys(hold_sum)
            time.sleep(1)
            d.find_element_by_xpath(".//*[@id='submit-step5_16']").click()
            print("["+str(i)+"]: Холдированная сумма введена")
        except:
            try:
                elem1 = d.find_element_by_id("form_final")
                print("["+str(i)+"]:", elem1.text)
            except:
                print("["+str(i)+"]: Ошибка после ввода данных по карте")



# -----------------------------------------------------------

#alert = driver0.switch_to_alert()

print()
print("Операция выполнена")

input("the end")
