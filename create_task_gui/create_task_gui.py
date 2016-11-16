#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import * #Select
#from selenium webdriver.support.ui import *
from selenium.webdriver.support import expected_conditions as EC #
from selenium.webdriver.common.by import By #
import unittest
import time

import xlrd
import xlwt
#import openpyxl

from datetime import datetime, timedelta
from random import Random
import copy

from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *

#import hashlib
#hash_object = hashlib.sha1(b'Password1')
#hex_dig = hash_object.hexdigest()
#print(hash_object)
#print(hex_dig)


'''
# Excel 2007
#получаем список значений из всех записей
#vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]

#val = sheet.row_values(0)[0]
#date = sheet.cell_value(0, 0)


# Работа с файлом Excel 2010
wb = openpyxl.load_workbook(filename = 'C:/Users/DShorokh/Desktop/selenium_excel.xlsx')
sheet = wb['СПР7']
#считываем значение определенной ячейки
val = sheet['C2'].value
print(val)
#считываем заданный диапазон
vals = [v[0].value for v in sheet.range('C2:AT')]
'''

def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)

# ---------------

def wait_for_page_load1(driver, timeout):
    old_page = driver.find_element_by_tag_name('html')
    yield
    WebDriverWait(driver, timeout).until(
        EC.staleness_of(old_page)
    )


list_gui = []
# Реализация интерфейса
def from_gui(event):

    flag = True
    p1 = ent1.get()
    p2 = ent2.get()
    p3 = ent3.get()
    p4 = var1.get()
    p5 = var2.get()
    p6 = var3.get()
    p7 = var4.get()

    if p1 == "" or p2 == "" or p3 == "" or p2 == p3 or int(p2) < 0 or int(p3) < 0:
        showinfo("Ошибка", "Заполните все поля")
        flag = False


    if(flag):
        list_gui.append(p1)
        list_gui.append(p2)
        list_gui.append(p3)
        list_gui.append(p4)
        list_gui.append(p5)
        list_gui.append(p6)
        list_gui.append(p7)
        root.destroy()
    return list_gui

# Главное окно
root = Tk()

# Кнопка "Создать"
but1 = Button(root, text = "Создать", width = 40, height = 3, bg = "white",fg = "black")
but1.bind("<Button-1>", from_gui)

# Поле для ввода пути к файлу
lab1 = Label(root, text = "Путь к таблице excel")
ent1 = Entry(root, width = 50, bd =3)
ent1.insert(END, 'C:/Users/DShorokh/Desktop/selenium_excel.xls')

# Поле для ввода номера строки с ключами
lab2 = Label(root, text = "Номер строки с ключами")
ent2 = Entry(root, width = 50, bd =3)
ent2.insert(END, '1')


# Поле для ввода начальной строки с клиентом
lab3 = Label(root, text = "Первая строчка с клиентом")
ent3 = Entry(root, width = 50, bd =3)
ent3.insert(END, '2')

# Выбор количества заявок
lab4 = Label(root, text = "Количество заявок")
var1=IntVar()
var1.set(1)
rad1_1 = Radiobutton(root,text="1",
          variable=var1,value=1)
rad1_2 = Radiobutton(root,text="2",
          variable=var1,value=2)
rad1_3 = Radiobutton(root, text="3",
          variable=var1, value=3)
rad1_4 = Radiobutton(root, text="4",
          variable=var1, value=4)
rad1_5 = Radiobutton(root, text="5",
          variable=var1, value=5)

# Выбор тестовой среды
lab5 = Label(root, text = "Тестовая среда")
var2=IntVar()
var2.set(1)
rad2_1 = Radiobutton(root,text="test1",
          variable=var2,value=1)
rad2_2 = Radiobutton(root,text="test3",
          variable=var2,value=2)

# Выбор региона
lab6 = Label(root, text = "Выбор региона")
var3=IntVar()
var3.set(1)
rad3_1 = Radiobutton(root,text="Регион присутствия",
          variable=var3,value=1)
rad3_2 = Radiobutton(root,text="Не регион присутствия",
          variable=var3,value=2)

# Выбор способа выдачи
lab7 = Label(root, text = "Выбор способа выдачи")
var4=IntVar()
var4.set(1)
rad4_1 = Radiobutton(root,text="Карта",
          variable=var4,value=1)
rad4_2 = Radiobutton(root,text="Контакт",
          variable=var4,value=2)
rad4_3 = Radiobutton(root, text="Юнистрим",
          variable=var4,value=3)

# Размещение элементов
lab1.pack()
ent1.pack()
lab2.pack()
ent2.pack()
lab3.pack()
ent3.pack()
lab4.pack()
rad1_1.pack()
rad1_2.pack()
rad1_3.pack()
rad1_4.pack()
rad1_5.pack()
lab5.pack()
rad2_1.pack()
rad2_2.pack()
lab6.pack()
rad3_1.pack()
rad3_2.pack()
lab7.pack()
rad4_1.pack()
rad4_2.pack()
rad4_3.pack()
but1.pack()
root.mainloop()


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
password = []

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
visa_prefix = ['4','1','2','5','1']

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
    day = ""
    month = ""
    date = datetime(*xlrd.xldate_as_tuple(date, 0))
    day = str(date.day)
    if (len(day) == 1): day = "0" + day
    month = str(date.month)
    if (len(month) == 1): month = "0" + month
    date = day + "." + month + "." + str(date.year)
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
def fill_1_page(driver, test_env, sum, term, lastname, name, patronymic, date_birthday, nationality, rf_perm_region, region, mobile_phone, email, password):

    #driver = webdriver.Firefox()
    #driver.get(test_env)

    # Сумма займа
    elem = driver.find_element_by_css_selector("input#sum")
    #elem.click()
    #elem.clear()

    #elem.send_keys(sum)
    #elem.send_keys(Keys.ENTER)

    # Срок займа
    elem = driver.find_element_by_css_selector("input#term")
    elem.click()
    elem.send_keys(term)

    # Фамилия
    elem = driver.find_element_by_css_selector("input#lastname")
    elem.send_keys(lastname)

    # Имя
    elem = driver.find_element_by_css_selector("input#name")
    elem.send_keys(name)

    # Отчество
    elem = driver.find_element_by_css_selector("input#patronymic")
    elem.send_keys(patronymic)

    # Дата рождения
    elem = driver.find_element_by_css_selector("input#date_birthday")
    elem.click()
    elem.send_keys(date_birthday)

    # Гражданство
    select = Select(driver.find_element_by_css_selector("select#nationality"))
    #select.select_by_visible_text("Российская Федерация")
    if nationality == "РФ":
        select.select_by_index(1)
    else:
        select.select_by_index(2)

    # Наличие постоянной регистрации
    elems = driver.find_elements_by_name("registration")
    if (rf_perm_region == "yes"):
        for option in elems:
            if option.get_attribute("value") == "1":
                option.click()
    else:
        for option in elems:
            if option.get_attribute("value") == "0":
                option.click()

    #print("Value is: %s" % option.get_attribute("value"))


    # Регион проживания
    select = Select(driver.find_element_by_css_selector("select#region_residence"))
    #print(select.options)
    select.select_by_visible_text(region)

    # Мобильный телефон
    elem = driver.find_element_by_css_selector("input#mobile_phone")
    elem.click()
    elem.send_keys(mobile_phone)

    # Электронная почта
    elem = driver.find_element_by_css_selector("input#email")
    elem.send_keys(email)

    # Пароль к личному кабинету
    #elem = driver.find_element_by_css_selector("input#field_p")
    #elem.send_keys(password)
    #elem = driver.find_element_by_css_selector("input#field_p_repeat")
    #elem.send_keys(password)

# Функция заполнения 2ой страницы заявки
def fill_2_page(driver, sex, prev_lastname, sn_passport, code_passport, date_passport, where_passport, place_birthday, \
                region_live, punkt_live, street_live, home_live, str_live, korp_live, flat_live, stac_phone, live_reg_flag):

    # Пол
    elems = driver.find_elements_by_name("sex")
    if (sex == "М"):
        for option in elems:
            if option.get_attribute("value") == "1":
                option.click()
    else:
        for option in elems:
            if option.get_attribute("value") == "2":
                option.click()

    # Предыдущая фамилия
    if(prev_lastname) != "NULL":
        elem = driver.find_element_by_css_selector("input#prev_lastname")
        elem.send_keys(prev_lastname)

    # Серия и номер паспорта
    elem = driver.find_element_by_css_selector("input#sn_passport")
    elem.click()
    elem.send_keys(sn_passport)

    # Код подразделения
    elem = driver.find_element_by_css_selector("input#code_passport")
    elem.click()
    elem.send_keys(code_passport)

    # Дата выдачи паспорта
    elem = driver.find_element_by_css_selector("input#date_passport")
    elem.click()
    elem.send_keys(date_passport)

    # Кем выдан паспорт
    elem = driver.find_element_by_css_selector("input#where_passport")
    elem.send_keys(where_passport)

    # Место рождения
    elem = driver.find_element_by_css_selector("input#place_birthday")
    elem.send_keys(place_birthday)

    # Регион проживания
    select = Select(driver.find_element_by_css_selector("select#region_live"))
    select.select_by_visible_text(region_live)

    # Населенный пункт
    elem = driver.find_element_by_css_selector("input#punkt_live")
    elem.send_keys(punkt_live)


    # Улица
    if(street_live != "NULL"):
        elem = driver.find_element_by_css_selector("input#street_live")
        elem.click()
        elem.send_keys(street_live)

    # Дом
    elem = driver.find_element_by_css_selector("input#home_live")
    elem.send_keys(home_live)

    # Строение
    elem = driver.find_element_by_css_selector("input#str_live")
    elem.send_keys(str_live)

    # Корпус
    elem = driver.find_element_by_css_selector("input#korp_live")
    elem.send_keys(korp_live)

    # Квартира
    elem = driver.find_element_by_css_selector("input#flat_live")
    elem.send_keys(flat_live)

    # Домашний телефон
    elem = driver.find_element_by_css_selector("input#stac_phone")
    elem.click()
    elem.send_keys(stac_phone)

    # Фактический адрес проживания совпадает с адресом регистрации
    if(live_reg_flag == "yes"):
        elem = driver.find_element_by_css_selector("input#live_reg_flag")
        elem.click()
    else: print("error")

# Функция заполнения 3ей страницы заявки
def fill_3_page(driver, type_work, company_name, company_view, company_status, company_start, work_phone, region_work, punkt_work, \
                street_work, home_work, str_work, korp_work, flat_work, work_stag, last_stag, income_work, income_add, \
                payment_house, payment_credit, payment_other, loan_purpose, education, family_status, partner_lastname, partner_name, \
                partner_patronymic, partner_birthday, partner_income, partner_credit, number_dep, number_child, contacts_name, contacts_status, contacts_phone):

    # Тип занятости
    select = Select(driver.find_element_by_css_selector("select#type_work"))
    select.select_by_visible_text(type_work)

    # Название компании
    if(company_name != "NULL"):
        elem = driver.find_element_by_css_selector("input#company_name")
        elem.send_keys(company_name)

    # Вид деятельности компании
    if (company_view != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#company_view"))
        select.select_by_visible_text(company_view)

    # Занимаемая должность
    if (company_status != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#company_status"))
        select.select_by_visible_text(company_status)

    # Начало работы в организации
    if (company_start != "NULL"):
        elem = driver.find_element_by_css_selector("input#company_start")
        elem.click()
        elem.send_keys(company_start)

    # Рабочий телефон
    if (work_phone != "NULL"):
        elem = driver.find_element_by_css_selector("input#work_phone")
        elem.send_keys(work_phone)

    # Регион рабочего адреса
    if (region_work != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#region_work"))
        select.select_by_visible_text(region_work)

    # Населенный пункт
    if (punkt_work != "NULL"):
        elem = driver.find_element_by_css_selector("input#punkt_work")
        elem.send_keys(punkt_work)

    # Улица
    if (street_work != "NULL"):
        elem = driver.find_element_by_css_selector("input#street_work")
        elem.send_keys(street_work)

    # Дом
    if (home_work != "NULL"):
        elem = driver.find_element_by_css_selector("input#home_work")
        elem.send_keys(home_work)

    # Строение
    if (str_work != "NULL"):
        elem = driver.find_element_by_css_selector("input#str_work")
        elem.send_keys(str_work)

    # Корпус
    if (korp_work != "NULL"):
        elem = driver.find_element_by_css_selector("input#korp_work")
        elem.send_keys(korp_work)

    # Квартира
    if (flat_work != "NULL"):
        elem = driver.find_element_by_css_selector("input#flat_work")
        elem.send_keys(flat_work)

    # Общий трудовой стаж
    if (work_stag != "NULL"):
        elem = driver.find_element_by_css_selector("input#work_stag")
        elem.send_keys(work_stag)

    # Длительность работы на прежнем месте
    if (last_stag != "NULL"):
        elem = driver.find_element_by_css_selector("input#last_stag")
        elem.send_keys(last_stag)

    # Доход по месту работы
    if (income_work != "NULL"):
        elem = driver.find_element_by_css_selector("input#income_work")
        elem.send_keys(income_work)

    # Дополнительный доход
    if (income_add != "NULL"):
        elem = driver.find_element_by_css_selector("input#income_add")
        elem.send_keys(income_add)

    # Расходы на жилье
    if (payment_house != "NULL"):
        elem = driver.find_element_by_css_selector("input#payment_house")
        elem.send_keys(payment_house)

    # Выплаты по кредитам
    if (payment_credit != "NULL"):
        elem = driver.find_element_by_css_selector("input#payment_credit")
        elem.send_keys(payment_credit)

    # Прочие финансовые обязательства
    if (payment_other != "NULL"):
        elem = driver.find_element_by_css_selector("input#payment_other")
        elem.send_keys(payment_other)

    # Цель займа
    if (loan_purpose != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#loan_purpose"))
        select.select_by_visible_text(loan_purpose)

    # Образование
    if (education != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#education"))
        select.select_by_visible_text(education)

    # Семейное положение
    if (family_status != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#family_status"))
        select.select_by_visible_text(family_status)

    # Фамилия супруга(и)
    if (partner_lastname != "NULL"):
        elem = driver.find_element_by_css_selector("input#partner_lastname")
        elem.send_keys(partner_lastname)

    # Имя супруга(и)
    if (partner_name != "NULL"):
        elem = driver.find_element_by_css_selector("input#partner_name")
        elem.send_keys(partner_name)

    # Отчество супруга(и)
    if (partner_patronymic != "NULL"):
        elem = driver.find_element_by_css_selector("input#partner_patronymic")
        elem.send_keys(partner_patronymic)

    # Дата рождения супруга(и)
    if (partner_birthday != "NULL"):
        elem = driver.find_element_by_css_selector("input#partner_birthday")
        elem.click()
        elem.send_keys(partner_birthday)

    # Доход супруга(и)
    if (partner_income != "NULL"):
        elem = driver.find_element_by_css_selector("input#partner_income")
        elem.send_keys(partner_income)

    # Выплаты по кредитам супруга(и)
    if (partner_credit != "NULL"):
        elem = driver.find_element_by_css_selector("input#partner_credit")
        elem.send_keys(partner_credit)

    # Количество иждивенцев
    if (number_dep != "NULL"):
        elem = driver.find_element_by_css_selector("input#number_dep")
        elem.click()
        elem.send_keys(number_dep)

    # Количество детей
    if (number_child != "NULL"):
        elem = driver.find_element_by_css_selector("input#number_child")
        elem.send_keys(number_child)

    # Контактное лицо
    if (contacts_name != "NULL"):
        elem = driver.find_element_by_css_selector("input#contacts_name")
        elem.send_keys(contacts_name)

    # Кем приходится контактное лицо
    if (contacts_status != "NULL"):
        select = Select(driver.find_element_by_css_selector("select#contacts_status"))
        select.select_by_visible_text(contacts_status)

    # Телефон контактного лица
    if (contacts_phone != "NULL"):
        elem = driver.find_element_by_css_selector("input#contacts_phone")
        elem.click()
        elem.send_keys(contacts_phone)

def choose_type_receive(driver,type_receive):

    elems = driver.find_elements_by_class_name("type_receive")

    if (type_receive == "Карта"):
        for option in elems:
            if option.get_attribute("value") == "16":
                option.click()
    elif(type_receive == "Контакт"):
        for option in elems:
            if option.get_attribute("value") == "2":
                option.click()
    elif(type_receive == "Юнистрим"):
        for option in elems:
            if option.get_attribute("value") == "4":
                option.click()

def fill_cc(driver, credit_card, expire_month, expire_year, cardholder, cvc2):

    # Номер карты
    elem = driver.find_element_by_css_selector("input#credit_card_number")
    elem.send_keys(credit_card)

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
    elem = driver.find_element_by_css_selector("input#cardholder")
    elem.click()
    elem.send_keys(cardholder)

    # Код CVC
    elem = driver.find_element_by_css_selector("input#cvv2")
    elem.send_keys(cvc2)

def fill_hold_sum(driver,sum):

    try:
        elem = driver.find_element_by_css_selector("#input#card_sum")
        elem.send_keys(sum)
    except: pass

# Путь к таблице excel
file_name = 'C:/Users/DShorokh/Desktop/selenium_excel.xls'
file_name = list_gui[0]

# Номер строки с ключами
keys_row = int(list_gui[1])-1

# Номер строки с первым клиентом
first_client_row = int(list_gui[2])-1

# Количество клиентов
clients_amount = 0
clients_amount = list_gui[3]

# Выбор региона присутствия true/false
rp = True
if list_gui[5] == 1:
    rp = True
elif list_gui[5] == 2:
    rp = False


# Копируем в словарь clients данные из таблицы
# входные данные: путь к таблице, номер листа с данными, номер строки с ключами, номер строки с данными первого клиента, количество клиентов (от первого подряд)
clients = copy_from_excel(file_name, 0, keys_row, first_client_row, clients_amount)

# Изменяем данные о доходах для прохождения СПР
check_key = 'Доход по основному месту работы'
for item in clients:
    if int(item[check_key]) < 50000:
        item[check_key] = str(50000.0)

# Пароль для ЛК
new_password = "Password1"

# Инициализация полей
for i in range(0, clients_amount):
    sum.append("20000")
    lastname.append(clients[i]['ФАМИЛИЯ'])
    name.append(clients[i]['ИМЯ'])
    patronymic.append(clients[i]['ОТЧЕСТВО'])
    date_birthday.append(clients[i]['ДАТА РОЖДЕНИЯ'])
    nationality.append(clients[i]['ГРАЖДАНСТВО'])
    rf_perm_region.append("yes")
    if(rp): region.append("Московская (обл)")
    else: region.append("Тамбовская (обл)")
    mobile_phone.append(str(clients[i]['Мобильный телефон'])[1:11])
    email.append("test.shorokh@yandex.ru")
    password.append(new_password)
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
    if(rp): region_live.append("Московская (обл)")
    else: region_live.append("Тамбовская (обл)")
    if(rp): punkt_live.append("Дачный поселок Березка (Шатурский р-н)")
    else: punkt_live.append("Выселки(ок) Никольские (Рассказовский р-н)")
    street_live.append("NULL")
    home_live.append("1")
    str_live.append("2")
    korp_live.append("3")
    flat_live.append("4")
    stac_phone.append(str(clients[i]['Домашний телефон'])[1:11])
    live_reg_flag.append("yes")
    #------------------------------
    type_work.append(clients[i]['Тип Занятости'])
    company_name.append(clients[i]['Название Компании'])
    company_view.append(clients[i]['Вид деятельности Компании'])
    company_status.append(clients[i]['Позиция в организации'])
    company_start.append(clients[i]['Длительность работы в данной организации'])
    work_phone.append(str(clients[i]['Рабочий телефон'])[1:11])
    if(rp): region_work.append("Московская (обл)")
    else: region_work.append("Тамбовская (обл)")
    if(rp): punkt_work.append("Дачный поселок Березка (Шатурский р-н)")
    else: punkt_work.append("Выселки(ок) Никольские (Рассказовский р-н)")
    street_work.append("NULL")
    home_work.append("4")
    str_work.append("3")
    korp_work.append("2")
    flat_work.append("1")
    work_stag1 = str(clients[i]['Общий трудовой стаж'])
    if(work_stag1 != "NULL"): work_stag1 = work_stag1[0:-2]
    work_stag.append(work_stag1)
    last_stag1 = str(clients[i]['Стаж работы на предыдущем месте'])
    if(last_stag1 != "NULL"): last_stag1 = last_stag1[0:-2]
    last_stag.append(last_stag1)
    income_work1 = str(clients[i]['Доход по основному месту работы'])
    if(income_work1 != "NULL"): income_work1 = income_work1[0:-2]
    income_work.append(income_work1)
    income_add1 = str(clients[i]['Сумма дополнительных личных доходов'])
    if(income_add1 != "NULL"): income_add1 = income_add1[0:-2]
    income_add.append(income_add1)
    payment_house1 = str(clients[i]['Расходы на жилье и коммунальные платежи'])
    if(payment_house1 != "NULL"): payment_house1 = payment_house1[0:-2]
    payment_house.append(payment_house1)
    payment_credit1 = str(clients[i]['Выплаты клиента по кредитам'])
    if(payment_credit1 != "NULL"): payment_credit1 = payment_credit1[0:-2]
    payment_credit.append(payment_credit1)
    payment_other1 = str(clients[i]['Прочие финансовые обязательства'])
    if(payment_other1 != "NULL"): payment_other1 = payment_other1[0:-2]
    payment_other.append(payment_other1)
    loan_purpose.append(clients[i]['Цель получения займа'])
    education.append(clients[i]['Образование'])
    family_status.append(clients[i]['Семейное положение'])
    partner_lastname.append(clients[i]['Отчество Супруга'])         # Перепутано в excel
    partner_name.append(clients[i]['Фамилия Супруга'])              # Перепутано в excel
    partner_patronymic.append(clients[i]['Имя Супруга'])            # Перепутано в excel
    partner_birthday.append(clients[i]['Дата рождения Супруга'])
    partner_income1 = str(clients[i]['Доход супруга'])
    if(partner_income1 != "NULL"): partner_income1 = partner_income1[0:-2]
    partner_income.append(partner_income1)
    partner_credit1 = str(clients[i]['Выплаты супруга по кредитам'])
    if(partner_credit1 != "NULL"): partner_credit1 = partner_credit1[0:-2]
    partner_credit.append(partner_credit1)
    number_dep.append(str(clients[i]['Количестов иждивенцев'])[0:-2])
    number_child.append(str(clients[i]['Количестов детей'])[0:-2])
    contacts_name.append("Контактное лицо")
    contacts_status.append("Родственник")
    contacts_phone.append("1111111111")


# Запуск браузера
#driver0 = webdriver.Firefox()
#driver1 = webdriver.Firefox()
#driver2 = webdriver.Firefox()


# Инициализация url's
test1 = ""
test3 = ""

# Инициализация способа получения займа
type1 = "Карта"
type2 = "Контакт"
type3 = "Юнистрим"

##-------------------- Создание заявки ----------------------

imp_time = 45
# Реализация создания нескольких заявок
#j = 0

# Инициализация условий создания заявки
env = test1
if list_gui[4] == 1:
    env = test1
elif list_gui[4] == 2:
    env = test3

t = type1
if list_gui[6] == 1:
    t = type1
elif list_gui[6] == 2:
   t = type2
elif list_gui[6] == 3:
    t = type3



for i in range(0, clients_amount):
    print("["+str(i+1)+"]", clients[i]['ФАМИЛИЯ'], clients[i]['ИМЯ'], clients[i]['ОТЧЕСТВО'])
print()

# Процесс создания заявки
if clients_amount == 1:

    d1 = webdriver.Firefox()
    d1.implicitly_wait(imp_time)

    d1.get(env)

    # Заполнение 1ой страницы
    fill_1_page(d1, env, sum[0], 0, lastname[0], name[0], patronymic[0], date_birthday[0], nationality[0], \
                rf_perm_region[0], region[0], mobile_phone[0], email[0], password[0])

    # Переход далее
    d1.find_element_by_css_selector("a#submit_step1").click()
    print("[1]: 1ая страница заполнена")
    #time.sleep(16)

    # ЭЦП-1
    try:
        elem1 = d1.find_element_by_css_selector("input#smscode")
        elem1.send_keys("123456")
    except:
        try:
            elem1 = d1.find_element_by_id("form_final")
            print("[1]:", elem1.text)
        except:
            print("[1]: Ошибка  после 1 страницы")
    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit-step4").click()
        print("[1]: Код ЭЦП-1 введен")
    except: pass
    #time.sleep(5)

    # Заполнение 2ой страницы
    try:
        fill_2_page(d1, sex[0], prev_lastname[0], sn_passport[0], code_passport[0], date_passport[0], \
                    where_passport[0], place_birthday[0], \
                    region_live[0], punkt_live[0], street_live[0], home_live[0], str_live[0], korp_live[0],
                    flat_live[0], \
                    stac_phone[0], live_reg_flag[0])
    except:
        print("[1]: Ошибка  после 1 страницы")


    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit_step2").click()
        print("[1]: 2ая страница заполнена")
    except:
        pass


    #time.sleep(3)

    # Заполнение 3ей страницы
    try:
        fill_3_page(d1, type_work[0], company_name[0], company_view[0], company_status[0], company_start[0], \
                    work_phone[0], region_work[0], punkt_work[0], street_work[0], home_work[0], \
                    str_work[0], korp_work[0], flat_work[0], work_stag[0], last_stag[0], income_work[0], income_add[0], \
                    payment_house[0], payment_credit[0], payment_other[0], loan_purpose[0], \
                    education[0], family_status[0], partner_lastname[0], partner_name[0], partner_patronymic[0], \
                    partner_birthday[0], partner_income[0], partner_credit[0], number_dep[0], number_child[0], \
                    contacts_name[0], contacts_status[0], contacts_phone[0])
    except:
        pass


    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit_step3").click()
        print("[1]: 3я страница заполнена")
    except:
        pass


    #time.sleep(16)
    # with wait_for_page_load1(d1, 10):
    #   pass
    try:
        choose_type_receive(d1, t)
    except:
        try:
            elem1 = d1.find_element_by_id("form_final")
            print("[1]:", elem1.text)
        except:
            print("[1]: Невозможно выбрать способ оплаты")


    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit-step5").click()
        print("[1]: Способ получения займа выбран")
    except:
        pass


    #time.sleep(10)  # 5

    if t == type1:
        # Генерация номера карты
        credit_card = credit_card_number(visa_prefix, 16, clients_amount)
        print("[1]: Номер сгенерированной карты: ", credit_card[0])

        try:
            fill_cc(d1, credit_card[0], "Октябрь", "2018", "Ivan Ivanov", "123")
        except:
            pass


        try:
            elem1 = d1.find_element_by_name("submit")
            elem1.click()
            print("[1]: Данные карты введены")
        except:
            pass
elif clients_amount == 2:

    d1 = webdriver.Firefox()
    d2 = webdriver.Firefox()
    d1.implicitly_wait(imp_time)
    d2.implicitly_wait(imp_time)

    d1.get(env)
    d2.get(env)

    # Заполнение 1ой страницы
    fill_1_page(d1, env, sum[0], 0, lastname[0], name[0], patronymic[0], date_birthday[0], nationality[0], \
                rf_perm_region[0], region[0], mobile_phone[0], email[0], password[0])
    fill_1_page(d2, env, sum[1], 0, lastname[1], name[1], patronymic[1], date_birthday[1], nationality[1], \
                rf_perm_region[1], region[1], mobile_phone[1], email[1], password[1])

    # Переход далее
    d1.find_element_by_css_selector("a#submit_step1").click()
    print("[1]: 1ая страница заполнена")
    d2.find_element_by_css_selector("a#submit_step1").click()
    print("[2]: 1ая страница заполнена")
    #time.sleep(16)

    # ЭЦП-1
    try:
        elem1 = d1.find_element_by_css_selector("input#smscode")
        elem1.send_keys("123456")
    except:
        try:
            elem1 = d1.find_element_by_id("form_final")
            print("[1]:", elem1.text)
        except:
            print("[1]: Ошибка  после 1 страницы")
    try:
        elem2 = d2.find_element_by_css_selector("input#smscode")
        elem2.send_keys("123456")
    except:
        try:
            elem2 = d2.find_element_by_id("form_final")
            print("[2]:", elem2.text)
        except:
            print("[2]: Ошибка  после 1 страницы")

    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit-step4").click()
        print("[1]: Код ЭЦП-1 введен")
    except: pass
    try:
        d2.find_element_by_css_selector("a#submit-step4").click()
        print("[2]: Код ЭЦП-1 введен")
    except: pass
    #time.sleep(5)

    # Заполнение 2ой страницы
    try:
        fill_2_page(d1, sex[0], prev_lastname[0], sn_passport[0], code_passport[0], date_passport[0], \
                    where_passport[0], place_birthday[0], \
                    region_live[0], punkt_live[0], street_live[0], home_live[0], str_live[0], korp_live[0],
                    flat_live[0], \
                    stac_phone[0], live_reg_flag[0])
    except:
        print("[1]: Ошибка  после 1 страницы")
    try:
        fill_2_page(d2, sex[1], prev_lastname[1], sn_passport[1], code_passport[1], date_passport[1], \
                    where_passport[1], place_birthday[1], \
                    region_live[1], punkt_live[1], street_live[1], home_live[1], str_live[1], korp_live[1], \
                    flat_live[1], \
                    stac_phone[1], live_reg_flag[1])
    except:
        print("[2]: Ошибка после 1 страницы")


    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit_step2").click()
        print("[1]: 2ая страница заполнена")
    except:
        pass
    try:
        d2.find_element_by_css_selector("a#submit_step2").click()
        print("[2]: 2ая страница заполнена")
    except:
        pass


    #time.sleep(3)

    # Заполнение 3ей страницы
    try:
        fill_3_page(d1, type_work[0], company_name[0], company_view[0], company_status[0], company_start[0], \
                    work_phone[0], region_work[0], punkt_work[0], street_work[0], home_work[0], \
                    str_work[0], korp_work[0], flat_work[0], work_stag[0], last_stag[0], income_work[0], income_add[0], \
                    payment_house[0], payment_credit[0], payment_other[0], loan_purpose[0], \
                    education[0], family_status[0], partner_lastname[0], partner_name[0], partner_patronymic[0], \
                    partner_birthday[0], partner_income[0], partner_credit[0], number_dep[0], number_child[0], \
                    contacts_name[0], contacts_status[0], contacts_phone[0])
    except:
        pass
    try:
        fill_3_page(d2, type_work[1], company_name[1], company_view[1], company_status[1], company_start[1], \
                    work_phone[1], region_work[1], punkt_work[1], street_work[1], home_work[1], \
                    str_work[1], korp_work[1], flat_work[1], work_stag[1], last_stag[1], income_work[1], income_add[1], \
                    payment_house[1], payment_credit[1], payment_other[1], loan_purpose[1], \
                    education[1], family_status[1], partner_lastname[1], partner_name[1], partner_patronymic[1], \
                    partner_birthday[1], partner_income[1], partner_credit[1], number_dep[1], number_child[1], \
                    contacts_name[1], contacts_status[1], contacts_phone[1])
    except:
        pass


    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit_step3").click()
        print("[1]: 3я страница заполнена")
    except:
        pass
    try:
        d2.find_element_by_css_selector("a#submit_step3").click()
        print("[2]: 3я страница заполнена")
    except:
        pass


    #time.sleep(16)
    try:
        choose_type_receive(d1, t)
    except:
        try:
            elem1 = d1.find_element_by_id("form_final")
            print("[1]:", elem1.text)
        except:
            print("[1]: Невозможно выбрать способ оплаты")
    try:
        choose_type_receive(d2, t)
    except:
        try:
            elem2 = d2.find_element_by_id("form_final")
            print("[2]:", elem2.text)
        except:
            print("[2]: Невозможно выбрать способ оплаты")


    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit-step5").click()
        print("[1]: Способ получения займа выбран")
    except:
        pass
    try:
        d2.find_element_by_css_selector("a#submit-step5").click()
        print("[2]: Способ получения займа выбран")
    except:
        pass


    #time.sleep(10)  # 5

    if t == type1:
        # Генерация номера карты
        credit_card = credit_card_number(visa_prefix, 16, clients_amount)
        print("[1]: Номер сгенерированной карты: ", credit_card[0])
        print("[2]: Номер сгенерированной карты: ", credit_card[1])


        try:
            fill_cc(d1, credit_card[0], "Октябрь", "2018", "Ivan Ivanov", "123")
        except:
            pass
        try:
            fill_cc(d2, credit_card[1], "Октябрь", "2018", "Ivan Ivanov", "123")
        except:
            pass


        try:
            elem1 = d1.find_element_by_name("submit")
            elem1.click()
            print("[1]: Данные карты введены")
        except:
            pass

        try:
            elem2 = d2.find_element_by_name("submit")
            elem2.click()
            print("[2]: Данные карты введены")
        except:
            pass
elif clients_amount == 3:

    d1 = webdriver.Firefox()
    d2 = webdriver.Firefox()
    d3 = webdriver.Firefox()
    d1.implicitly_wait(imp_time)
    d2.implicitly_wait(imp_time)
    d3.implicitly_wait(imp_time)

    d1.get(env)
    d2.get(env)
    d3.get(env)

    # Заполнение 1ой страницы
    fill_1_page(d1, env, sum[0], 0, lastname[0], name[0], patronymic[0], date_birthday[0], nationality[0], \
                rf_perm_region[0], region[0], mobile_phone[0], email[0], password[0])
    fill_1_page(d2, env, sum[1], 0, lastname[1], name[1], patronymic[1], date_birthday[1], nationality[1], \
                rf_perm_region[1], region[1], mobile_phone[1], email[1], password[1])
    fill_1_page(d3, env, sum[2], 0, lastname[2], name[2], patronymic[2], date_birthday[2], nationality[2], \
                rf_perm_region[2], region[2], mobile_phone[2], email[2], password[2])
    # Переход далее
    d1.find_element_by_css_selector("a#submit_step1").click()
    print("[1]: 1ая страница заполнена")
    d2.find_element_by_css_selector("a#submit_step1").click()
    print("[2]: 1ая страница заполнена")
    d3.find_element_by_css_selector("a#submit_step1").click()
    print("[3]: 1ая страница заполнена")
    #time.sleep(16)

    # ЭЦП-1
    try:
        elem1 = d1.find_element_by_css_selector("input#smscode")
        elem1.send_keys("123456")
    except:
        try:
            elem1 = d1.find_element_by_id("form_final")
            print("[1]:", elem1.text)
        except:
            print("[1]: Ошибка  после 1 страницы")
    try:
        elem2 = d2.find_element_by_css_selector("input#smscode")
        elem2.send_keys("123456")
    except:
        try:
            elem2 = d2.find_element_by_id("form_final")
            print("[2]:", elem2.text)
        except:
            print("[2]: Ошибка  после 1 страницы")
    try:
        elem3 = d3.find_element_by_css_selector("input#smscode")
        elem3.send_keys("123456")
    except:
        try:
            elem3 = d3.find_element_by_id("form_final")
            print("[3]:", elem3.text)
        except:
            print("[3]: Ошибка  после 1 страницы")

    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit-step4").click()
        print("[1]: Код ЭЦП-1 введен")
    except: pass
    try:
        d2.find_element_by_css_selector("a#submit-step4").click()
        print("[2]: Код ЭЦП-1 введен")
    except: pass
    try:
        d3.find_element_by_css_selector("a#submit-step4").click()
        print("[3]: Код ЭЦП-1 введен")
    except: pass
    #time.sleep(5)

    # Заполнение 2ой страницы
    try:
        fill_2_page(d1, sex[0], prev_lastname[0], sn_passport[0], code_passport[0], date_passport[0], \
                    where_passport[0], place_birthday[0], \
                    region_live[0], punkt_live[0], street_live[0], home_live[0], str_live[0], korp_live[0],
                    flat_live[0], \
                    stac_phone[0], live_reg_flag[0])
    except:
        print("[1]: Ошибка  после 1 страницы")
    try:
        fill_2_page(d2, sex[1], prev_lastname[1], sn_passport[1], code_passport[1], date_passport[1], \
                    where_passport[1], place_birthday[1], \
                    region_live[1], punkt_live[1], street_live[1], home_live[1], str_live[1], korp_live[1], \
                    flat_live[1], \
                    stac_phone[1], live_reg_flag[1])
    except:
        print("[2]: Ошибка после 1 страницы")
    try:
        fill_2_page(d3, sex[2], prev_lastname[2], sn_passport[2], code_passport[2], date_passport[2], \
                    where_passport[2], place_birthday[2], \
                    region_live[2], punkt_live[2], street_live[2], home_live[2], str_live[2], korp_live[2], \
                    flat_live[2], \
                    stac_phone[2], live_reg_flag[2])
    except:
        print("[3]: Ошибка после 1 страницы")

    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit_step2").click()
        print("[1]: 2ая страница заполнена")
    except:
        pass
    try:
        d2.find_element_by_css_selector("a#submit_step2").click()
        print("[2]: 2ая страница заполнена")
    except:
        pass
    try:
        d3.find_element_by_css_selector("a#submit_step2").click()
        print("[3]: 2ая страница заполнена")
    except:
        pass

    #time.sleep(3)

    # Заполнение 3ей страницы
    try:
        fill_3_page(d1, type_work[0], company_name[0], company_view[0], company_status[0], company_start[0], \
                    work_phone[0], region_work[0], punkt_work[0], street_work[0], home_work[0], \
                    str_work[0], korp_work[0], flat_work[0], work_stag[0], last_stag[0], income_work[0], income_add[0], \
                    payment_house[0], payment_credit[0], payment_other[0], loan_purpose[0], \
                    education[0], family_status[0], partner_lastname[0], partner_name[0], partner_patronymic[0], \
                    partner_birthday[0], partner_income[0], partner_credit[0], number_dep[0], number_child[0], \
                    contacts_name[0], contacts_status[0], contacts_phone[0])
    except:
        pass
    try:
        fill_3_page(d2, type_work[1], company_name[1], company_view[1], company_status[1], company_start[1], \
                    work_phone[1], region_work[1], punkt_work[1], street_work[1], home_work[1], \
                    str_work[1], korp_work[1], flat_work[1], work_stag[1], last_stag[1], income_work[1], income_add[1], \
                    payment_house[1], payment_credit[1], payment_other[1], loan_purpose[1], \
                    education[1], family_status[1], partner_lastname[1], partner_name[1], partner_patronymic[1], \
                    partner_birthday[1], partner_income[1], partner_credit[1], number_dep[1], number_child[1], \
                    contacts_name[1], contacts_status[1], contacts_phone[1])
    except:
        pass
    try:
        fill_3_page(d3, type_work[2], company_name[2], company_view[2], company_status[2], company_start[2], \
                    work_phone[2], region_work[2], punkt_work[2], street_work[2], home_work[2], \
                    str_work[2], korp_work[2], flat_work[2], work_stag[2], last_stag[2], income_work[2], income_add[2], \
                    payment_house[2], payment_credit[2], payment_other[2], loan_purpose[2], \
                    education[2], family_status[2], partner_lastname[2], partner_name[2], partner_patronymic[2], \
                    partner_birthday[2], partner_income[2], partner_credit[2], number_dep[2], number_child[2], \
                    contacts_name[2], contacts_status[2], contacts_phone[2])
    except:
        pass

    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit_step3").click()
        print("[1]: 3я страница заполнена")
    except:
        pass
    try:
        d2.find_element_by_css_selector("a#submit_step3").click()
        print("[2]: 3я страница заполнена")
    except:
        pass
    try:
        d3.find_element_by_css_selector("a#submit_step3").click()
        print("[3]: 3я страница заполнена")
    except:
        pass

    #time.sleep(16)
    # with wait_for_page_load1(d1, 10):
    #   pass
    try:
        choose_type_receive(d1, t)
    except:
        try:
            elem1 = d1.find_element_by_id("form_final")
            print("[1]:", elem1.text)
        except:
            print("[1]: Невозможно выбрать способ оплаты")
    try:
        choose_type_receive(d2, t)
    except:
        try:
            elem2 = d2.find_element_by_id("form_final")
            print("[2]:", elem2.text)
        except:
            print("[2]: Невозможно выбрать способ оплаты")
    try:
        choose_type_receive(d3, t)
    except:
        try:
            elem3 = d3.find_element_by_id("form_final")
            print("[3]:", elem3.text)
        except:
            print("[3]: Невозможно выбрать способ оплаты")


    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit-step5").click()
        print("[1]: Способ получения займа выбран")
    except:
        pass
    try:
        d2.find_element_by_css_selector("a#submit-step5").click()
        print("[2]: Способ получения займа выбран")
    except:
        pass
    try:
        d3.find_element_by_css_selector("a#submit-step5").click()
        print("[3]: Способ получения займа выбран")
    except:
        pass

    #time.sleep(10)  # 5

    if t == type1:
        # Генерация номера карты
        credit_card = credit_card_number(visa_prefix, 16, clients_amount)
        print("[1]: Номер сгенерированной карты: ", credit_card[0])
        print("[2]: Номер сгенерированной карты: ", credit_card[1])
        print("[3]: Номер сгенерированной карты: ", credit_card[2])

        try:
            fill_cc(d1, credit_card[0], "Октябрь", "2018", "Ivan Ivanov", "123")
        except:
            pass
        try:
            fill_cc(d2, credit_card[1], "Октябрь", "2018", "Ivan Ivanov", "123")
        except:
            pass
        try:
            fill_cc(d3, credit_card[2], "Октябрь", "2018", "Ivan Ivanov", "123")
        except:
            pass


        try:
            elem1 = d1.find_element_by_name("submit")
            elem1.click()
            print("[1]: Данные карты введены")
        except:
            pass

        try:
            elem2 = d2.find_element_by_name("submit")
            elem2.click()
            print("[2]: Данные карты введены")
        except:
            pass

        try:
            elem3 = d3.find_element_by_name("submit")
            elem3.click()
            print("[3]: Данные карты введены")
        except:
            pass
elif clients_amount == 4:

    d1 = webdriver.Firefox()
    d2 = webdriver.Firefox()
    d3 = webdriver.Firefox()
    d4 = webdriver.Firefox()
    d1.implicitly_wait(imp_time)
    d2.implicitly_wait(imp_time)
    d3.implicitly_wait(imp_time)
    d4.implicitly_wait(imp_time)

    d1.get(env)
    d2.get(env)
    d3.get(env)
    d4.get(env)

    # Заполнение 1ой страницы
    fill_1_page(d1, env, sum[0], 0, lastname[0], name[0], patronymic[0], date_birthday[0], nationality[0],\
                rf_perm_region[0], region[0], mobile_phone[0], email[0], password[0])
    fill_1_page(d2, env, sum[1], 0, lastname[1], name[1], patronymic[1], date_birthday[1], nationality[1],\
                rf_perm_region[1], region[1], mobile_phone[1], email[1], password[1])
    fill_1_page(d3, env, sum[2], 0, lastname[2], name[2], patronymic[2], date_birthday[2], nationality[2],\
                rf_perm_region[2], region[2], mobile_phone[2], email[2], password[2])
    fill_1_page(d4, env, sum[3], 0, lastname[3], name[3], patronymic[3], date_birthday[3], nationality[3], \
                rf_perm_region[3], region[3], mobile_phone[3], email[3], password[3])
    # Переход далее
    d1.find_element_by_css_selector("a#submit_step1").click()
    print("[1]: 1ая страница заполнена")
    d2.find_element_by_css_selector("a#submit_step1").click()
    print("[2]: 1ая страница заполнена")
    d3.find_element_by_css_selector("a#submit_step1").click()
    print("[3]: 1ая страница заполнена")
    d4.find_element_by_css_selector("a#submit_step1").click()
    print("[4]: 1ая страница заполнена")
    #time.sleep(17)

    # ЭЦП-1
    try:
        elem1 = d1.find_element_by_css_selector("input#smscode")
        elem1.send_keys("123456")
    except:
        try:
            elem1 = d1.find_element_by_id("form_final")
            print("[1]:", elem1.text)
        except:
            print("[1]: Ошибка  после 1 страницы")
    try:
        elem2 = d2.find_element_by_css_selector("input#smscode")
        elem2.send_keys("123456")
    except:
        try:
            elem2 = d2.find_element_by_id("form_final")
            print("[2]:", elem2.text)
        except:
            print("[2]: Ошибка  после 1 страницы")
    try:
        elem3 = d3.find_element_by_css_selector("input#smscode")
        elem3.send_keys("123456")
    except:
        try:
            elem3 = d3.find_element_by_id("form_final")
            print("[3]:", elem3.text)
        except:
            print("[3]: Ошибка  после 1 страницы")
    try:
        elem4 = d4.find_element_by_css_selector("input#smscode")
        elem4.send_keys("123456")
    except:
        try:
            elem4 = d4.find_element_by_id("form_final")
            print("[4]:", elem4.text)
        except:
            print("[4]: Ошибка  после 1 страницы")


    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit-step4").click()
        print("[1]: Код ЭЦП-1 введен")
    except: pass
    try:
        d2.find_element_by_css_selector("a#submit-step4").click()
        print("[2]: Код ЭЦП-1 введен")
    except: pass
    try:
        d3.find_element_by_css_selector("a#submit-step4").click()
        print("[3]: Код ЭЦП-1 введен")
    except: pass
    try:
        d4.find_element_by_css_selector("a#submit-step4").click()
        print("[4]: Код ЭЦП-1 введен")
    except: pass
    #time.sleep(5)

    # Заполнение 2ой страницы
    try: fill_2_page(d1, sex[0], prev_lastname[0], sn_passport[0], code_passport[0], date_passport[0], \
                where_passport[0], place_birthday[0], \
                region_live[0], punkt_live[0], street_live[0], home_live[0], str_live[0], korp_live[0],
                flat_live[0], \
                stac_phone[0], live_reg_flag[0])
    except: print("[1]: Ошибка  после 1 страницы")
    try: fill_2_page(d2, sex[1], prev_lastname[1], sn_passport[1], code_passport[1], date_passport[1], \
                where_passport[1], place_birthday[1], \
                region_live[1], punkt_live[1], street_live[1], home_live[1], str_live[1], korp_live[1],\
                flat_live[1], \
                stac_phone[1], live_reg_flag[1])
    except: print("[2]: Ошибка после 1 страницы")
    try: fill_2_page(d3, sex[2], prev_lastname[2], sn_passport[2], code_passport[2], date_passport[2], \
                where_passport[2], place_birthday[2], \
                region_live[2], punkt_live[2], street_live[2], home_live[2], str_live[2], korp_live[2],\
                flat_live[2], \
                stac_phone[2], live_reg_flag[2])
    except: print("[3]: Ошибка после 1 страницы")
    try: fill_2_page(d4, sex[3], prev_lastname[3], sn_passport[3], code_passport[3], date_passport[3], \
                where_passport[3], place_birthday[3], \
                region_live[3], punkt_live[3], street_live[3], home_live[3], str_live[3], korp_live[3], \
                flat_live[3], \
                stac_phone[3], live_reg_flag[3])
    except: print("[4]: Ошибка после 1 страницы")
    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit_step2").click()
        print("[1]: 2ая страница заполнена")
    except: pass
    try:
        d2.find_element_by_css_selector("a#submit_step2").click()
        print("[2]: 2ая страница заполнена")
    except: pass
    try:
        d3.find_element_by_css_selector("a#submit_step2").click()
        print("[3]: 2ая страница заполнена")
    except: pass
    try:
        d4.find_element_by_css_selector("a#submit_step2").click()
        print("[4]: 2ая страница заполнена")
    except:pass
    #time.sleep(3)

    # Заполнение 3ей страницы
    try: fill_3_page(d1, type_work[0], company_name[0], company_view[0], company_status[0], company_start[0], \
                work_phone[0], region_work[0], punkt_work[0], street_work[0], home_work[0], \
                str_work[0], korp_work[0], flat_work[0], work_stag[0], last_stag[0], income_work[0], income_add[0], \
                payment_house[0], payment_credit[0], payment_other[0], loan_purpose[0], \
                education[0], family_status[0], partner_lastname[0], partner_name[0], partner_patronymic[0], \
                partner_birthday[0], partner_income[0], partner_credit[0], number_dep[0], number_child[0], \
                contacts_name[0], contacts_status[0], contacts_phone[0])
    except: pass
    try: fill_3_page(d2, type_work[1], company_name[1], company_view[1], company_status[1], company_start[1], \
                work_phone[1], region_work[1], punkt_work[1], street_work[1], home_work[1], \
                str_work[1], korp_work[1], flat_work[1], work_stag[1], last_stag[1], income_work[1], income_add[1], \
                payment_house[1], payment_credit[1], payment_other[1], loan_purpose[1], \
                education[1], family_status[1], partner_lastname[1], partner_name[1], partner_patronymic[1], \
                partner_birthday[1], partner_income[1], partner_credit[1], number_dep[1], number_child[1], \
                contacts_name[1], contacts_status[1], contacts_phone[1])
    except: pass
    try: fill_3_page(d3, type_work[2], company_name[2], company_view[2], company_status[2], company_start[2], \
                work_phone[2], region_work[2], punkt_work[2], street_work[2], home_work[2], \
                str_work[2], korp_work[2], flat_work[2], work_stag[2], last_stag[2], income_work[2], income_add[2], \
                payment_house[2], payment_credit[2], payment_other[2], loan_purpose[2], \
                education[2], family_status[2], partner_lastname[2], partner_name[2], partner_patronymic[2], \
                partner_birthday[2], partner_income[2], partner_credit[2], number_dep[2], number_child[2], \
                contacts_name[2], contacts_status[2], contacts_phone[2])
    except: pass
    try: fill_3_page(d4, type_work[3], company_name[3], company_view[3], company_status[3], company_start[3], \
                work_phone[3], region_work[3], punkt_work[3], street_work[3], home_work[3], \
                str_work[3], korp_work[3], flat_work[3], work_stag[3], last_stag[3], income_work[3], income_add[3], \
                payment_house[3], payment_credit[3], payment_other[3], loan_purpose[3], \
                education[3], family_status[3], partner_lastname[3], partner_name[3], partner_patronymic[3], \
                partner_birthday[3], partner_income[3], partner_credit[3], number_dep[3], number_child[3], \
                contacts_name[3], contacts_status[3], contacts_phone[3])
    except: pass

    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit_step3").click()
        print("[1]: 3я страница заполнена")
    except: pass
    try:
        d2.find_element_by_css_selector("a#submit_step3").click()
        print("[2]: 3я страница заполнена")
    except: pass
    try:
        d3.find_element_by_css_selector("a#submit_step3").click()
        print("[3]: 3я страница заполнена")
    except: pass
    try:
        d4.find_element_by_css_selector("a#submit_step3").click()
        print("[4]: 3я страница заполнена")
    except: pass

    #time.sleep(16)
    # with wait_for_page_load1(d1, 10):
    #   pass
    try: choose_type_receive(d1, t)
    except:
        try:
            elem1 = d1.find_element_by_id("form_final")
            print("[1]:", elem1.text)
        except: print("[1]: Невозможно выбрать способ оплаты")
    try: choose_type_receive(d2, t)
    except:
        try:
            elem2 = d2.find_element_by_id("form_final")
            print("[2]:", elem2.text)
        except: print("[2]: Невозможно выбрать способ оплаты")
    try: choose_type_receive(d3, t)
    except:
        try:
            elem3 = d3.find_element_by_id("form_final")
            print("[3]:", elem3.text)
        except: print("[3]: Невозможно выбрать способ оплаты")
    try: choose_type_receive(d4, t)
    except:
        try:
            elem4 = d4.find_element_by_id("form_final")
            #elem2 = d4.find_element_by_class_name("final-step false")
            #find_element_by_xpath("//p[contains(., 'Film')][1]")
            print("[4]:", elem4.text)
        except: print("[4]: Невозможно выбрать способ оплаты")

    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit-step5").click()
        print("[1]: Способ получения займа выбран")
    except: pass
    try:
        d2.find_element_by_css_selector("a#submit-step5").click()
        print("[2]: Способ получения займа выбран")
    except: pass
    try:
        d3.find_element_by_css_selector("a#submit-step5").click()
        print("[3]: Способ получения займа выбран")
    except: pass
    try:
        d4.find_element_by_css_selector("a#submit-step5").click()
        print("[4]: Способ получения займа выбран")
    except: pass
    # with wait_for_page_load(d1):
    #    with wait_for_page_load(d2):
    #        pass
    #time.sleep(10)  # 5

    if t == type1:
        # Генерация номера карты
        credit_card = credit_card_number(visa_prefix, 16, clients_amount)
        print("[1]: Номер сгенерированной карты: ", credit_card[0])
        print("[2]: Номер сгенерированной карты: ", credit_card[1])
        print("[3]: Номер сгенерированной карты: ", credit_card[2])
        print("[4]: Номер сгенерированной карты: ", credit_card[3])

        try: fill_cc(d1, credit_card[0], "Октябрь", "2018", "Ivan Ivanov", "123")
        except: pass
        try: fill_cc(d2, credit_card[1], "Октябрь", "2018", "Ivan Ivanov", "123")
        except: pass
        try: fill_cc(d3, credit_card[2], "Октябрь", "2018", "Ivan Ivanov", "123")
        except: pass
        try: fill_cc(d4, credit_card[3], "Октябрь", "2018", "Ivan Ivanov", "123")
        except: pass


        try:
            elem1 = d1.find_element_by_name("submit")
            elem1.click()
            print("[1]: Данные карты введены")
        except: pass

        try:
            elem2 = d2.find_element_by_name("submit")
            elem2.click()
            print("[2]: Данные карты введены")
        except: pass

        try:
            elem3 = d3.find_element_by_name("submit")
            elem3.click()
            print("[3]: Данные карты введены")
        except: pass

        try:
            elem4 = d4.find_element_by_name("submit")
            elem4.click()
            print("[4]: Данные карты введены")
        except: pass

        '''
        #time.sleep(15)

        try:
            alert1 = d1.switch_to.alert()
            alert1.accept()
        except: print("alert error1")

        try:
            confirm1 = d1.switch_to.alert()
            print("nashel alert")
        except:
            print("alert error2")

        #time.sleep(15)
        try: d1.find_element_by_css_selector("a#submit-step5_16").click()
        except: print("net knopki submit hold sum")
        '''
elif clients_amount == 5:

    d1 = webdriver.Firefox()
    d2 = webdriver.Firefox()
    d3 = webdriver.Firefox()
    d4 = webdriver.Firefox()
    d5 = webdriver.Firefox()
    d1.implicitly_wait(imp_time)
    d2.implicitly_wait(imp_time)
    d3.implicitly_wait(imp_time)
    d4.implicitly_wait(imp_time)
    d5.implicitly_wait(imp_time)

    d1.get(env)
    d2.get(env)
    d3.get(env)
    d4.get(env)
    d5.get(env)

    # Заполнение 1ой страницы
    fill_1_page(d1, env, sum[0], 0, lastname[0], name[0], patronymic[0], date_birthday[0], nationality[0], \
                rf_perm_region[0], region[0], mobile_phone[0], email[0], password[0])
    fill_1_page(d2, env, sum[1], 0, lastname[1], name[1], patronymic[1], date_birthday[1], nationality[1], \
                rf_perm_region[1], region[1], mobile_phone[1], email[1], password[1])
    fill_1_page(d3, env, sum[2], 0, lastname[2], name[2], patronymic[2], date_birthday[2], nationality[2], \
                rf_perm_region[2], region[2], mobile_phone[2], email[2], password[2])
    fill_1_page(d4, env, sum[3], 0, lastname[3], name[3], patronymic[3], date_birthday[3], nationality[3], \
                rf_perm_region[3], region[3], mobile_phone[3], email[3], password[3])
    fill_1_page(d5, env, sum[4], 0, lastname[4], name[4], patronymic[4], date_birthday[4], nationality[4], \
                rf_perm_region[4], region[4], mobile_phone[4], email[4], password[4])
    # Переход далее
    d1.find_element_by_css_selector("a#submit_step1").click()
    print("[1]: 1ая страница заполнена")
    d2.find_element_by_css_selector("a#submit_step1").click()
    print("[2]: 1ая страница заполнена")
    d3.find_element_by_css_selector("a#submit_step1").click()
    print("[3]: 1ая страница заполнена")
    d4.find_element_by_css_selector("a#submit_step1").click()
    print("[4]: 1ая страница заполнена")
    d5.find_element_by_css_selector("a#submit_step1").click()
    print("[5]: 1ая страница заполнена")
    #time.sleep(16)

    # ЭЦП-1
    try:
        elem1 = d1.find_element_by_css_selector("input#smscode")
        elem1.send_keys("123456")
    except:
        try:
            elem1 = d1.find_element_by_id("form_final")
            print("[1]:", elem1.text)
        except:
            print("[1]: Ошибка  после 1 страницы")
    try:
        elem2 = d2.find_element_by_css_selector("input#smscode")
        elem2.send_keys("123456")
    except:
        try:
            elem2 = d2.find_element_by_id("form_final")
            print("[2]:", elem2.text)
        except:
            print("[2]: Ошибка  после 1 страницы")
    try:
        elem3 = d3.find_element_by_css_selector("input#smscode")
        elem3.send_keys("123456")
    except:
        try:
            elem3 = d3.find_element_by_id("form_final")
            print("[3]:", elem3.text)
        except:
            print("[3]: Ошибка  после 1 страницы")
    try:
        elem4 = d4.find_element_by_css_selector("input#smscode")
        elem4.send_keys("123456")
    except:
        try:
            elem4 = d4.find_element_by_id("form_final")
            print("[4]:", elem4.text)
        except:
            print("[4]: Ошибка  после 1 страницы")
    try:
        elem5 = d5.find_element_by_css_selector("input#smscode")
        elem5.send_keys("123456")
    except:
        try:
            elem5 = d5.find_element_by_id("form_final")
            print("[5]:", elem5.text)
        except:
            print("[5]: Ошибка  после 1 страницы")


    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit-step4").click()
        print("[1]: Код ЭЦП-1 введен")
    except: pass
    try:
        d2.find_element_by_css_selector("a#submit-step4").click()
        print("[2]: Код ЭЦП-1 введен")
    except: pass
    try:
        d3.find_element_by_css_selector("a#submit-step4").click()
        print("[3]: Код ЭЦП-1 введен")
    except: pass
    try:
        d4.find_element_by_css_selector("a#submit-step4").click()
        print("[4]: Код ЭЦП-1 введен")
    except: pass
    try:
        d5.find_element_by_css_selector("a#submit-step4").click()
        print("[5]: Код ЭЦП-1 введен")
    except: pass
    #time.sleep(5)

    # Заполнение 2ой страницы
    try:
        fill_2_page(d1, sex[0], prev_lastname[0], sn_passport[0], code_passport[0], date_passport[0], \
                    where_passport[0], place_birthday[0], \
                    region_live[0], punkt_live[0], street_live[0], home_live[0], str_live[0], korp_live[0],
                    flat_live[0], \
                    stac_phone[0], live_reg_flag[0])
    except:
        print("[1]: Ошибка  после 1 страницы")
    try:
        fill_2_page(d2, sex[1], prev_lastname[1], sn_passport[1], code_passport[1], date_passport[1], \
                    where_passport[1], place_birthday[1], \
                    region_live[1], punkt_live[1], street_live[1], home_live[1], str_live[1], korp_live[1], \
                    flat_live[1], \
                    stac_phone[1], live_reg_flag[1])
    except:
        print("[2]: Ошибка после 1 страницы")
    try:
        fill_2_page(d3, sex[2], prev_lastname[2], sn_passport[2], code_passport[2], date_passport[2], \
                    where_passport[2], place_birthday[2], \
                    region_live[2], punkt_live[2], street_live[2], home_live[2], str_live[2], korp_live[2], \
                    flat_live[2], \
                    stac_phone[2], live_reg_flag[2])
    except:
        print("[3]: Ошибка после 1 страницы")
    try:
        fill_2_page(d4, sex[3], prev_lastname[3], sn_passport[3], code_passport[3], date_passport[3], \
                    where_passport[3], place_birthday[3], \
                    region_live[3], punkt_live[3], street_live[3], home_live[3], str_live[3], korp_live[3], \
                    flat_live[3], \
                    stac_phone[3], live_reg_flag[3])
    except:
        print("[4]: Ошибка после 1 страницы")
    try:
        fill_2_page(d5, sex[4], prev_lastname[4], sn_passport[4], code_passport[4], date_passport[4], \
                    where_passport[4], place_birthday[4], \
                    region_live[4], punkt_live[4], street_live[4], home_live[4], str_live[4], korp_live[4], \
                    flat_live[4], \
                    stac_phone[4], live_reg_flag[4])
    except:
        print("[4]: Ошибка после 1 страницы")
    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit_step2").click()
        print("[1]: 2ая страница заполнена")
    except:
        pass
    try:
        d2.find_element_by_css_selector("a#submit_step2").click()
        print("[2]: 2ая страница заполнена")
    except:
        pass
    try:
        d3.find_element_by_css_selector("a#submit_step2").click()
        print("[3]: 2ая страница заполнена")
    except:
        pass
    try:
        d4.find_element_by_css_selector("a#submit_step2").click()
        print("[4]: 2ая страница заполнена")
    except:
        pass
    try:
        d5.find_element_by_css_selector("a#submit_step2").click()
        print("[5]: 2ая страница заполнена")
    except:
        pass
    #time.sleep(3)

    # Заполнение 3ей страницы
    try:
        fill_3_page(d1, type_work[0], company_name[0], company_view[0], company_status[0], company_start[0], \
                    work_phone[0], region_work[0], punkt_work[0], street_work[0], home_work[0], \
                    str_work[0], korp_work[0], flat_work[0], work_stag[0], last_stag[0], income_work[0], income_add[0], \
                    payment_house[0], payment_credit[0], payment_other[0], loan_purpose[0], \
                    education[0], family_status[0], partner_lastname[0], partner_name[0], partner_patronymic[0], \
                    partner_birthday[0], partner_income[0], partner_credit[0], number_dep[0], number_child[0], \
                    contacts_name[0], contacts_status[0], contacts_phone[0])
    except:
        pass
    try:
        fill_3_page(d2, type_work[1], company_name[1], company_view[1], company_status[1], company_start[1], \
                    work_phone[1], region_work[1], punkt_work[1], street_work[1], home_work[1], \
                    str_work[1], korp_work[1], flat_work[1], work_stag[1], last_stag[1], income_work[1], income_add[1], \
                    payment_house[1], payment_credit[1], payment_other[1], loan_purpose[1], \
                    education[1], family_status[1], partner_lastname[1], partner_name[1], partner_patronymic[1], \
                    partner_birthday[1], partner_income[1], partner_credit[1], number_dep[1], number_child[1], \
                    contacts_name[1], contacts_status[1], contacts_phone[1])
    except:
        pass
    try:
        fill_3_page(d3, type_work[2], company_name[2], company_view[2], company_status[2], company_start[2], \
                    work_phone[2], region_work[2], punkt_work[2], street_work[2], home_work[2], \
                    str_work[2], korp_work[2], flat_work[2], work_stag[2], last_stag[2], income_work[2], income_add[2], \
                    payment_house[2], payment_credit[2], payment_other[2], loan_purpose[2], \
                    education[2], family_status[2], partner_lastname[2], partner_name[2], partner_patronymic[2], \
                    partner_birthday[2], partner_income[2], partner_credit[2], number_dep[2], number_child[2], \
                    contacts_name[2], contacts_status[2], contacts_phone[2])
    except:
        pass
    try:
        fill_3_page(d4, type_work[3], company_name[3], company_view[3], company_status[3], company_start[3], \
                    work_phone[3], region_work[3], punkt_work[3], street_work[3], home_work[3], \
                    str_work[3], korp_work[3], flat_work[3], work_stag[3], last_stag[3], income_work[3], income_add[3], \
                    payment_house[3], payment_credit[3], payment_other[3], loan_purpose[3], \
                    education[3], family_status[3], partner_lastname[3], partner_name[3], partner_patronymic[3], \
                    partner_birthday[3], partner_income[3], partner_credit[3], number_dep[3], number_child[3], \
                    contacts_name[3], contacts_status[3], contacts_phone[3])
    except:
        pass
    try:
        fill_3_page(d5, type_work[4], company_name[4], company_view[4], company_status[4], company_start[4], \
                    work_phone[4], region_work[4], punkt_work[4], street_work[4], home_work[4], \
                    str_work[4], korp_work[4], flat_work[4], work_stag[4], last_stag[4], income_work[4], income_add[4], \
                    payment_house[4], payment_credit[4], payment_other[4], loan_purpose[4], \
                    education[4], family_status[4], partner_lastname[4], partner_name[4], partner_patronymic[4], \
                    partner_birthday[4], partner_income[4], partner_credit[4], number_dep[4], number_child[4], \
                    contacts_name[4], contacts_status[4], contacts_phone[4])
    except:
        pass

    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit_step3").click()
        print("[1]: 3я страница заполнена")
    except:
        pass
    try:
        d2.find_element_by_css_selector("a#submit_step3").click()
        print("[2]: 3я страница заполнена")
    except:
        pass
    try:
        d3.find_element_by_css_selector("a#submit_step3").click()
        print("[3]: 3я страница заполнена")
    except:
        pass
    try:
        d4.find_element_by_css_selector("a#submit_step3").click()
        print("[4]: 3я страница заполнена")
    except:
        pass
    try:
        d5.find_element_by_css_selector("a#submit_step3").click()
        print("[5]: 3я страница заполнена")
    except:
        pass

    #time.sleep(16)
    # with wait_for_page_load1(d1, 10):
    #   pass
    try:
        choose_type_receive(d1, t)
    except:
        try:
            elem1 = d1.find_element_by_id("form_final")
            print("[1]:", elem1.text)
        except:
            print("[1]: Невозможно выбрать способ оплаты")
    try:
        choose_type_receive(d2, t)
    except:
        try:
            elem2 = d2.find_element_by_id("form_final")
            print("[2]:", elem2.text)
        except:
            print("[2]: Невозможно выбрать способ оплаты")
    try:
        choose_type_receive(d3, t)
    except:
        try:
            elem3 = d3.find_element_by_id("form_final")
            print("[3]:", elem3.text)
        except:
            print("[3]: Невозможно выбрать способ оплаты")
    try:
        choose_type_receive(d4, t)
    except:
        try:
            elem4 = d4.find_element_by_id("form_final")
            print("[4]:", elem4.text)
        except:
            print("[4]: Невозможно выбрать способ оплаты")
    try:
        choose_type_receive(d5, t)
    except:
        try:
            elem5 = d5.find_element_by_id("form_final")
            print("[5]:", elem5.text)
        except:
            print("[5]: Невозможно выбрать способ оплаты")

    # Переход далее
    try:
        d1.find_element_by_css_selector("a#submit-step5").click()
        print("[1]: Способ получения займа выбран")
    except:
        pass
    try:
        d2.find_element_by_css_selector("a#submit-step5").click()
        print("[2]: Способ получения займа выбран")
    except:
        pass
    try:
        d3.find_element_by_css_selector("a#submit-step5").click()
        print("[3]: Способ получения займа выбран")
    except:
        pass
    try:
        d4.find_element_by_css_selector("a#submit-step5").click()
        print("[4]: Способ получения займа выбран")
    except:
        pass
    try:
        d5.find_element_by_css_selector("a#submit-step5").click()
        print("[5]: Способ получения займа выбран")
    except:
        pass
    # with wait_for_page_load(d1):
    #    with wait_for_page_load(d2):
    #        pass
    #time.sleep(10)  # 5

    if t == type1:
        # Генерация номера карты
        credit_card = credit_card_number(visa_prefix, 16, clients_amount)
        print("[1]: Номер сгенерированной карты: ", credit_card[0])
        print("[2]: Номер сгенерированной карты: ", credit_card[1])
        print("[3]: Номер сгенерированной карты: ", credit_card[2])
        print("[4]: Номер сгенерированной карты: ", credit_card[3])
        print("[5]: Номер сгенерированной карты: ", credit_card[4])

        try: fill_cc(d1, credit_card[0], "Октябрь", "2018", "Ivan Ivanov", "123")
        except: pass
        try: fill_cc(d2, credit_card[1], "Октябрь", "2018", "Ivan Ivanov", "123")
        except: pass
        try: fill_cc(d3, credit_card[2], "Октябрь", "2018", "Ivan Ivanov", "123")
        except: pass
        try: fill_cc(d4, credit_card[3], "Октябрь", "2018", "Ivan Ivanov", "123")
        except: pass
        try: fill_cc(d5, credit_card[4], "Октябрь", "2018", "Ivan Ivanov", "123")
        except: pass

        try:
            elem1 = d1.find_element_by_name("submit")
            elem1.click()
            print("[1]: Данные карты введены")
        except:
            pass

        try:
            elem2 = d2.find_element_by_name("submit")
            elem2.click()
            print("[2]: Данные карты введены")
        except:
            pass

        try:
            elem3 = d3.find_element_by_name("submit")
            elem3.click()
            print("[3]: Данные карты введены")
        except:
            pass

        try:
            elem4 = d4.find_element_by_name("submit")
            elem4.click()
            print("[4]: Данные карты введены")
        except:
            pass
        try:
            elem5 = d5.find_element_by_name("submit")
            elem5.click()
            print("[5]: Данные карты введены")
        except:
            pass
else: print("Максимум 5 браузеров одновременно")





# -----------------------------------------------------------
'''
# Заполнение 1ой страницы
fill_1_page(driver0, test1, sum[j], 0, lastname[j], name[j], patronymic[j], date_birthday[j], nationality[j], rf_perm_region[j], region[j], mobile_phone[j], email[j], password[j])
# Переход далее
driver0.find_element_by_css_selector("a#submit_step1").click()
print("1ая страница заполнена")
time.sleep(15)

# ЭЦП-1
elem = driver0.find_element_by_css_selector("input#smscode")
elem.send_keys("123456")

# Переход далее
driver0.find_element_by_css_selector("a#submit-step4").click()
#driver1.find_element_by_class_name("confirm-sms").click()
print("Код ЭЦП-1 введен")
time.sleep(5)

# Заполнение 2ой страницы
fill_2_page(driver0, sex[j], prev_lastname[j], sn_passport[j], code_passport[j], date_passport[j], where_passport[j], place_birthday[j], \
            region_live[j], punkt_live[j], street_live[j], home_live[j], str_live[j], korp_live[j], flat_live[j], stac_phone[j], live_reg_flag[j])
# Переход далее
driver0.find_element_by_css_selector("a#submit_step2").click()
print("2ая страница заполнена")
time.sleep(3)

# Заполнение 3ей страницы
fill_3_page(driver0, type_work[j], company_name[j], company_view[j], company_status[j], company_start[j], work_phone[j], region_work[j], punkt_work[j], street_work[j], home_work[j], \
            str_work[j], korp_work[j], flat_work[j], work_stag[j], last_stag[j], income_work[j], income_add[j], payment_house[j], payment_credit[j], payment_other[j], loan_purpose[j], \
            education[j], family_status[j], partner_lastname[j], partner_name[j], partner_patronymic[j], partner_birthday[j], partner_income[j], partner_credit[j], number_dep[j], number_child[j], \
            contacts_name[j], contacts_status[j], contacts_phone[j])
# Переход далее
driver0.find_element_by_css_selector("a#submit_step3").click()
print("3я страница заполнена")

time.sleep(15)

choose_type_receive(driver0, type1)

# Переход далее
driver0.find_element_by_css_selector("a#submit-step5").click()
print("Способ получения займа выбран")

time.sleep(5)

# Генерация номера карты
credit_card = credit_card_number(visa_prefix, 16, clients_amount)
print("Номер сгенерированной карты: ", credit_card[j])

fill_cc(driver0, credit_card[j], "Октябрь", "2018", "Ivan Ivanov", "123")

#elem = driver1.find_element_by_name("submit")
#elem.click()
print("Данные карты введены")
'''
#time.sleep(12)
#alert = driver0.switch_to_alert()
#time.sleep(15)
# Холдированная сумма
#input#card_sum
#submit-step5_16
print()
print("Операция выполнена")

input("Нажмите на любую клавишу для выхода")
print()
print()