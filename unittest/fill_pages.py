
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import * #Select
import time
from random import Random
import copy


regionDict = {
'Адыгея': {'code': '100000000000', 'region': 'Адыгея (Респ)', 'punkt': 'Город Адыгейск', 'street': 'Абадзехская (ул)'},
'Алтай': {'code': '400000000000', 'region': 'Алтай (Респ)', 'punkt': 'Город Горно-Алтайск', 'street': 'Набережная (ул)'},
'Алтайский': {'code': '2200000000000', 'region': 'Алтайский (край)', 'punkt': 'Город Бийск', 'street': 'Набережная (ул)'},
'Амурская': {'code': '2800000000000', 'region': 'Амурская (обл)', 'punkt': 'Город Благовещенск', 'street': 'Набережная (ул)'},
'Архангельская': {'code': '2900000000000', 'region': 'Архангельская (обл)', 'punkt': 'Город Архангельск', 'street': 'Бабушкина (ул)'},
'Астраханская': {'code': '3000000000000', 'region': 'Астраханская (обл)', 'punkt': 'Город Астрахань', 'street': 'Абаканская (ул)'},
'Байконур': {'code': '9900000000000', 'region': 'Байконур (г)', 'punkt': 'Байконур (г)', 'street': 'Авиационная (ул)'},
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
'Удмуртская': {'code': '1800000000000', 'region': 'Удмуртская (Респ)', 'punkt': 'Город Барышникова ', 'street': 'Барышникова (ул)'},
'Ульяновская': {'code': '7300000000000', 'region': 'Ульяновская (обл)', 'punkt': 'Город Ульяновск', 'street': 'Набережная (ул)'},
'Хабаровский': {'code': '2700000000000', 'region': 'Хабаровский (край)', 'punkt': 'Город Хабаровск', 'street': 'Набережная (ул)'},
'Хакасия': {'code': '1900000000000', 'region': 'Хакасия (Респ)', 'punkt': 'Город Абакан', 'street': 'Набережная (ул)'},
'Ханты-Мансийский Автономный округ - Югра (АО)': {'code': '8600000000000', 'region': 'Ханты-Мансийский Автономный округ - Югра (АО)', 'punkt': 'Город Ханты-Мансийск', 'street': 'Набережная (ул)'},
'Челябинская': {'code': '7400000000000', 'region': 'Челябинская (обл)', 'punkt': 'Город Челябинск', 'street': 'Набережная (ул)'},
'Чеченская': {'code': '2000000000000', 'region': 'Чеченская (Респ)', 'punkt': 'Город Грозный', 'street': 'Набережная (ул)'},
'Чувашская Республика - (Чувашия)': {'code': '2100000000000', 'region': 'Чувашская Республика - (Чувашия)', 'punkt': 'Город Чебоксары', 'street': 'Бабушкина (ул)'},
'Чукотский': {'code': '8700000000000', 'region': 'Чукотский (АО)', 'punkt': 'Город Анадырь', 'street': 'Набережная (ул)'},
'Ямало-Ненецкий': {'code': '8900000000000', 'region': 'Ямало-Ненецкий (АО)', 'punkt': 'Город Салехард', 'street': 'Набережная (ул)'},
'Ярославская': {'code': '7600000000000', 'region': 'Ярославская (обл)', 'punkt': 'Город Ярославль', 'street': 'Базовая (ул)'}
}

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


# Функция заполнения 1ой страницы заявки
def fill_1_page(driver, sum_loan, term, lastname, name, patronymic, date_birthday, nationality, rf_perm_region, region, mobile_phone, email):

    # Сумма займа
    #elem = driver.find_element_by_xpath(".//*[@id='sum']")
    #elem.click()
    #elem.clear()

    #elem.send_keys(sum_loan)
    #elem.send_keys(Keys.ENTER)

    # Срок займа
    elem = driver.find_element_by_xpath(".//*[@id='term']")
    elem.click()
    elem.send_keys(term)

    # Мобильный телефон
    elem = driver.find_element_by_xpath(".//*[@id='mobile_phone']")
    elem.click()
    elem.send_keys(mobile_phone)

    # Фамилия
    elem = driver.find_element_by_xpath(".//*[@id='lastname']")
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
    if nationality == "Российская Федерация":
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