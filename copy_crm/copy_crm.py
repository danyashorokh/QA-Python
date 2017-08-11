#! /usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import datetime

import xlrd
import xlwt
from selenium.common.exceptions import NoSuchElementException
import config as c

#--------------------

# сайт: 1 - т1, 3 - т3, p - prod
test = 3

# номер заявки в CRM
id_crm = ["1-J6T97H"]
'''
id_crm = ["1-V0UIH3",
"1-V06VYR",
"1-UVXELS",
"1-UORECW"]#  "1-J2S7W9"  "1-ISYMSN" # a_7 (не по КЛАДР)   a_11
'''
# логины, пароли
login1 = c.login1
login3 = c.login3
loginp = c.loginp
passwp = c.passwp

# ссылки
url1 = c.url1
url3 = c.url3
urlp = c.urlp

# таймауты
timeout_login = 15
timeout = 2

#--------------------

#fo = open('output.txt','w')
res = {}
my_str = ""
t = "\t"
max_wait = 25 # максимальное ожидание браузера
row = 0

d1 = webdriver.Chrome()
d1.implicitly_wait(max_wait)

if test == 1:
	url = url1
	login = login1
	passw = login1
elif test == 3:
	url = url3
	login = login3
	passw = login3
else:
	url = urlp
	login = loginp
	passw = passwp

wb = xlwt.Workbook()
ws = wb.add_sheet('Result')

d1.get(url)
d1.find_element_by_xpath(".//*[@id='s_swepi_1']").send_keys(login)
d1.find_element_by_xpath(".//*[@id='s_swepi_2']").send_keys(passw)
d1.find_element_by_xpath(".//*[@id='s_swepi_22']").click()


for id_crm_one in id_crm:
    fo = open('output.txt', 'w')
    time.sleep(timeout_login)
    d1.find_element_by_xpath(".//*[@id='s_S_A5_div']/div/form/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/input").send_keys(id_crm_one)

    time.sleep(timeout)
    d1.find_element_by_xpath(".//*[@id='s_5_1_11_0_Ctrl']").click()

    time.sleep(timeout)
    d1.find_element_by_xpath(".//*[@id='1Last_Name']/a").click()
    time.sleep(timeout)

    res["sex"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[8]/td[3]/div/input").get_attribute("value")
    d1.back()

    time.sleep(timeout)
    d1.find_element_by_xpath(".//*[@id='1Name']/a").click()
    time.sleep(timeout)
    '''
    if test == 1:
        d1.find_element_by_xpath(".//*[@id='ui-id-171']").click() # открыть раздел анкета
    elif test == 3:
        d1.find_element_by_xpath(".//*[@id='ui-id-242']").click() # открыть раздел анкета
    else:
        d1.find_element_by_xpath(".//*[@id='ui-id-173']").click() # открыть раздел анкета
    '''
    d1.find_element_by_xpath(".//*[contains(text(),'Анкета')]").click()

    res["id"] = (str(datetime.now()))[11:-2]
    res["id"] = res["id"].replace(":","")
    res["id"] = res["id"].replace(".","")

    try:
        res["lastname"] = d1.find_element_by_xpath(".//*[@id='a_8']/div/table/tbody/tr[2]/td[4]/div/input").get_attribute("value")
        res["name"] = d1.find_element_by_xpath(".//*[@id='a_8']/div/table/tbody/tr[4]/td[3]/div/input").get_attribute("value")
        res["patronymic"] = d1.find_element_by_xpath(".//*[@id='a_8']/div/table/tbody/tr[6]/td[3]/div/input").get_attribute("value")
        res["prev_lastname"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[4]/td[3]/div/input").get_attribute("value")
        res["date_birthday"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[7]/td[3]/div/input").get_attribute("value")
        res["nationality"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[5]/td[3]/div/input").get_attribute("value")
        res["place_birthday"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[8]/td[3]/div/input").get_attribute("value")
        res["s"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[4]/td[6]/div/input").get_attribute("value")
        res["n"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[5]/td[5]/div/input").get_attribute("value")
        res["code_passport"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[6]/td[5]/div/input").get_attribute("value")
        res["where_passport"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[7]/td[5]/div/input").get_attribute("value")
        res["date_passport"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[8]/td[5]/div/input").get_attribute("value")
        res["mobile_phone"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[4]/td[9]/div/input").get_attribute("value")
        res["stac_phone"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[5]/td[7]/div/input").get_attribute("value")
        res["work_phone"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[7]/td[7]/div/input").get_attribute("value")

        # d1.find_element_by_xpath(".//*[@id='3_Address_Type']").click()
        d1.find_element_by_xpath(".//*[@id='last_pager_s_5_l']/span").click()

        try:
            d1.find_element_by_xpath(".//*[@id='a_11']/div/table/tbody/tr[3]/td[3]/div/input")
            adr_id = "a_11"
            print("Адрес по КЛАДР")
        except NoSuchElementException:
            adr_id = "a_7"
            print("Адрес не по КЛАДР")

        index = d1.find_element_by_xpath(".//*[@id='"+adr_id+"']/div/table/tbody/tr[4]/td[6]/div/input").get_attribute("value")
        if len(index) == 0: index = '111111'
        res["adr_live"] = index + ", " + d1.find_element_by_xpath(".//*[@id='"+adr_id+"']/div/table/tbody/tr[6]/td[3]/div/input").get_attribute("value") + ", " \
        + d1.find_element_by_xpath(".//*[@id='"+adr_id+"']/div/table/tbody/tr[5]/td[5]/div/input").get_attribute("value") + ", " \
        + d1.find_element_by_xpath(".//*[@id='"+adr_id+"']/div/table/tbody/tr[7]/td[6]/div/input").get_attribute("value") + ", " \
        + d1.find_element_by_xpath(".//*[@id='"+adr_id+"']/div/table/tbody/tr[4]/td[9]/div/input").get_attribute("value") + ", " \
        + d1.find_element_by_xpath(".//*[@id='"+adr_id+"']/div/table/tbody/tr[5]/td[9]/div/input").get_attribute("value") + ", " \
        + d1.find_element_by_xpath(".//*[@id='"+adr_id+"']/div/table/tbody/tr[6]/td[10]/div/input").get_attribute("value") + ", " \
        + d1.find_element_by_xpath(".//*[@id='"+adr_id+"']/div/table/tbody/tr[7]/td[9]/div/input").get_attribute("value")
        res["adr_reg"] = res["adr_live"]
        res["family_status"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[6]/td[3]/div/input").get_attribute("value")
        #print(res["family_status"])
        res["number_child"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[6]/td[5]/div/input").get_attribute("value")
        #print(res["number_child"])
        res["number_dep"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[5]/td[5]/div/input").get_attribute("value")
        #print(res["number_dep"])
        res["car"] = "NULL"
        #print(res["car"])
        res["type_work"] = d1.find_element_by_xpath(".//*[@id='a_10']/div/table/tbody/tr[4]/td[3]/div/input").get_attribute("value")
        #print(res["type_work"])
        res["company_type"] = "NULL"
        #print(res["company_type"])
        res["company_name"] = d1.find_element_by_xpath(".//*[@id='a_10']/div/table/tbody/tr[5]/td[3]/div/input").get_attribute("value")
        #print(res["company_name"])
        res["company_view"] = d1.find_element_by_xpath(".//*[@id='a_10']/div/table/tbody/tr[7]/td[3]/div/input").get_attribute("value")
        #print(res["company_view"])
        res["company_status"] = d1.find_element_by_xpath(".//*[@id='a_10']/div/table/tbody/tr[6]/td[3]/div/input").get_attribute("value")
        #print(res["company_status"])
        res["company_start"] = d1.find_element_by_xpath(".//*[@id='a_10']/div/table/tbody/tr[4]/td[6]/div/input").get_attribute("value")
        #print(res["company_start"])
        res["education"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[4]/td[5]/div/input").get_attribute("value")
        #print(res["education"])
        res["adr_work"] = res["adr_live"]
        #print(res["adr_work"])
        res["income_work"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[6]/td[3]/div/input").get_attribute("value")
        #print(res["income_work"])
        res["income_add"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[7]/td[3]/div/input").get_attribute("value")
        #print(res["income_add"])
        res["payment_house"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[6]/td[6]/div/input").get_attribute("value")
        #print(res["payment_house"])
        res["payment_credit"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[7]/td[5]/div/input").get_attribute("value")
        #print(res["payment_credit"])
        res["payment_other"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[8]/td[5]/div/input").get_attribute("value")
        #print(res["payment_other"])
        res["loan_purpose"] = d1.find_element_by_xpath(".//*[@id='a_8']/div/table/tbody/tr[12]/td[7]/div/input").get_attribute("value")
        #print(res["loan_purpose"])

        if res["family_status"] == "Женат/Замужем":
            res["partner_lastname"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[7]/td[3]/div/input").get_attribute("value")
            res["partner_name"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[8]/td[3]/div/input").get_attribute("value")
            res["partner_patronymic"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[9]/td[3]/div/input").get_attribute("value")
            res["partner_birthday"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[10]/td[3]/div/input").get_attribute("value")
            res["partner_income"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[8]/td[3]/div/input").get_attribute("value")
            res["partner_credit"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[9]/td[3]/div/input").get_attribute("value")
        else:
            res["partner_lastname"] = "NULL"
            res["partner_name"] = "NULL"
            res["partner_patronymic"] = "NULL"
            res["partner_birthday"] = "NULL"
            res["partner_income"] = "NULL"
            res["partner_credit"] = "NULL"

        if res["mobile_phone"]:
            res["mobile_phone"] = res["mobile_phone"].replace(" ","")
            res["mobile_phone"] = res["mobile_phone"].replace(")","")
            res["mobile_phone"] = res["mobile_phone"].replace("(","")
        if res["stac_phone"]:
            res["stac_phone"] = res["stac_phone"].replace(" ","")
            res["stac_phone"] = res["stac_phone"].replace(")","")
            res["stac_phone"] = res["stac_phone"].replace("(","")
        if res["work_phone"]:
            res["work_phone"] = res["work_phone"].replace(" ","")
            res["work_phone"] = res["work_phone"].replace(")","")
            res["work_phone"] = res["work_phone"].replace("(","")

        if res["income_work"] and res["income_work"]!= 'Null': res["income_work"] = (res["income_work"][:-5]).replace(" ","")
        if res["income_add"] and res["income_add"]!= 'Null': res["income_add"] = (res["income_add"][:-5]).replace(" ","")
        if res["partner_income"] and res["partner_income"]!= 'Null': res["partner_income"] = (res["partner_income"][:-5]).replace(" ","")
        if res["payment_house"] and res["payment_house"]!= 'Null': res["payment_house"] = (res["payment_house"][:-5]).replace(" ","")
        if res["payment_credit"] and res["payment_credit"]!= 'Null': res["payment_credit"] = (res["payment_credit"][:-5]).replace(" ","")
        if res["partner_credit"] and res["partner_credit"]!= 'Null': res["partner_credit"] = (res["partner_credit"][:-5]).replace(" ","")
        if res["payment_other"] and res["payment_other"]!= 'Null': res["payment_other"] = (res["payment_other"][:-5]).replace(" ","")

    except:
        print("error")

    for key in res:
        if res[key]== "":
            res[key] = "NULL"

    my_str = ""
    my_str += res["id"] +t+ res["lastname"] +t+ res["name"] +t+ res["patronymic"] +t+ res["prev_lastname"] +t+ res["date_birthday"] +t+ res["sex"] +t+ res["nationality"] +t+ \
    res["place_birthday"] +t+ res["s"] +t+ res["n"] +t+ res["code_passport"] +t+ res["where_passport"] +t+ res["date_passport"] +t+ res["mobile_phone"][1:] +t+ \
    res["stac_phone"] +t+ res["work_phone"] +t+ res["adr_reg"] +t+ res["adr_live"] +t+ res["family_status"] +t+ res["number_child"] +t+ res["number_dep"] +t+ res["partner_lastname"] +t+ \
    res["partner_name"] +t+ res["partner_patronymic"] +t+ res["partner_birthday"] +t+ res["car"] +t+ res["type_work"] +t+ res["company_type"] +t+ res["company_name"] +t+ \
    res["company_view"] +t+ res["company_status"] +t+ res["company_start"] +t+ "0" +t+ "0" +t+ res["education"] +t+ res["adr_work"] +t+ res["income_work"] +t+ \
    res["income_add"] +t+ res["partner_income"] +t+ res["payment_house"] +t+ res["payment_credit"] +t+ res["partner_credit"] +t+ res["payment_other"] +t+ res["loan_purpose"]

    print(res)

    fo.write(my_str)
    fo.close()

    #wb = xlwt.Workbook()
    #ws = wb.add_sheet('Result')

    my_str_list = []
    my_str_list = my_str.split("\t")

    i = 0

    for item in my_str_list:
        ws.write(row, i, item)
        i += 1
    wb.save('output.xls')
    row += 1

    d1.find_element_by_xpath(".//*[contains(text(),'Домой')]").click()

d1.close()

print("Операция выполнена")
input("")

