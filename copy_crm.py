#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
from datetime import datetime

import xlrd
import xlwt

#--------------------

# сайт: 1 - т1, 3 - т3, p - prod
test = 1

# номер заявки в CRM
id_crm = "1-TBY0LG"

# логины, пароли
login1 = "DSHOROKH"
login3 = "DSHOROKH3"
loginp = "DShorokh"
passwp = "Password90"

# ссылки
url1 = 'https://crm-test.migcredit.ru/fins_rus/start.swe?SWECmd=Start&SWEHo=crm-test.migcredit.ru'
url3 = 'https://t3crmas1.mgc.local/fins_rus/start.swe?SWECmd=Start&SWEHo=t3crmas1.mgc.local'
urlp = 'https://crm.migcredit.ru/fins_rus/start.swe?SWECmd=Start&SWEHo=crm.migcredit.ru'

# таймауты
timeout_login = 5
timeout = 1

#--------------------

fo = open('output.txt','w')
res = {}
my_str = ""
t = "\t"
max_wait = 25 # максимальное ожидание браузера

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


d1.get(url)
d1.find_element_by_xpath(".//*[@id='s_swepi_1']").send_keys(login)
d1.find_element_by_xpath(".//*[@id='s_swepi_2']").send_keys(passw)
d1.find_element_by_xpath(".//*[@id='s_swepi_22']").click()

time.sleep(timeout_login)
d1.find_element_by_xpath(".//*[@id='s_S_A5_div']/div/form/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/input").send_keys(id_crm)

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
	res["lastname"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[2]/td[4]/div/input").get_attribute("value")
	res["name"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[4]/td[3]/div/input").get_attribute("value")
	res["patronymic"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[6]/td[3]/div/input").get_attribute("value")
	res["prev_lastname"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[4]/td[3]/div/input").get_attribute("value")
	res["date_birthday"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[7]/td[3]/div/input").get_attribute("value")
	#res["sex"] = "М"# sex .//*[@id='a_3']/div/table/tbody/tr[8]/td[3]/div/input
	res["nationality"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[5]/td[3]/div/input").get_attribute("value")
	res["place_birthday"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[8]/td[3]/div/input").get_attribute("value")
	res["s"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[4]/td[6]/div/input").get_attribute("value")
	res["n"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[5]/td[5]/div/input").get_attribute("value")
	res["code_passport"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[6]/td[5]/div/input").get_attribute("value")
	res["where_passport"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[7]/td[5]/div/input").get_attribute("value")
	res["date_passport"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[8]/td[5]/div/input").get_attribute("value")
	res["mobile_phone"] = d1.find_element_by_xpath(".//*[@id='a_12']/div/table/tbody/tr[8]/td[3]/div/input").get_attribute("value")
	res["stac_phone"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[5]/td[7]/div/input").get_attribute("value")
	res["work_phone"] = d1.find_element_by_xpath(".//*[@id='a_4']/div/table/tbody/tr[7]/td[7]/div/input").get_attribute("value")
	index = d1.find_element_by_xpath(".//*[@id='a_11']/div/table/tbody/tr[4]/td[6]/div/input").get_attribute("value")
	if len(index) == 0: index = '111111'
	res["adr_live"] = index + ", " + d1.find_element_by_xpath(".//*[@id='a_11']/div/table/tbody/tr[6]/td[3]/div/input").get_attribute("value") + ", " \
	+ d1.find_element_by_xpath(".//*[@id='a_11']/div/table/tbody/tr[5]/td[5]/div/input").get_attribute("value") + ", " \
	+ d1.find_element_by_xpath(".//*[@id='a_11']/div/table/tbody/tr[7]/td[6]/div/input").get_attribute("value") + ", " \
	+ d1.find_element_by_xpath(".//*[@id='a_11']/div/table/tbody/tr[4]/td[9]/div/input").get_attribute("value") + ", " \
	+ d1.find_element_by_xpath(".//*[@id='a_11']/div/table/tbody/tr[5]/td[9]/div/input").get_attribute("value") + ", " \
	+ d1.find_element_by_xpath(".//*[@id='a_11']/div/table/tbody/tr[6]/td[10]/div/input").get_attribute("value") + ", " \
	+ d1.find_element_by_xpath(".//*[@id='a_11']/div/table/tbody/tr[7]/td[9]/div/input").get_attribute("value")
	res["adr_reg"] = res["adr_live"]
	res["family_status"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[6]/td[3]/div/input").get_attribute("value")
	res["number_child"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[6]/td[5]/div/input").get_attribute("value")
	res["number_dep"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[5]/td[5]/div/input").get_attribute("value")
	res["partner_lastname"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[7]/td[3]/div/input").get_attribute("value")
	res["partner_name"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[8]/td[3]/div/input").get_attribute("value")
	res["partner_patronymic"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[9]/td[3]/div/input").get_attribute("value")
	res["partner_birthday"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[10]/td[3]/div/input").get_attribute("value")
	res["car"] = "NULL"
	res["type_work"] = d1.find_element_by_xpath(".//*[@id='a_10']/div/table/tbody/tr[4]/td[3]/div/input").get_attribute("value")
	res["company_type"] = "NULL"
	res["company_name"] = d1.find_element_by_xpath(".//*[@id='a_10']/div/table/tbody/tr[5]/td[3]/div/input").get_attribute("value")
	res["company_view"] = d1.find_element_by_xpath(".//*[@id='a_10']/div/table/tbody/tr[7]/td[3]/div/input").get_attribute("value")
	res["company_status"] = d1.find_element_by_xpath(".//*[@id='a_10']/div/table/tbody/tr[6]/td[3]/div/input").get_attribute("value")
	res["company_start"] = d1.find_element_by_xpath(".//*[@id='a_10']/div/table/tbody/tr[4]/td[6]/div/input").get_attribute("value")
	res["education"] = d1.find_element_by_xpath(".//*[@id='a_3']/div/table/tbody/tr[4]/td[5]/div/input").get_attribute("value")
	res["adr_work"] = res["adr_live"]
	res["income_work"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[6]/td[3]/div/input").get_attribute("value")
	res["income_add"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[7]/td[3]/div/input").get_attribute("value")
	res["partner_income"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[8]/td[3]/div/input").get_attribute("value")
	res["payment_house"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[6]/td[6]/div/input").get_attribute("value")
	res["payment_credit"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[7]/td[5]/div/input").get_attribute("value")
	res["partner_credit"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[9]/td[3]/div/input").get_attribute("value")
	res["payment_other"] = d1.find_element_by_xpath(".//*[@id='a_6']/div/table/tbody/tr[8]/td[5]/div/input").get_attribute("value")
	res["loan_purpose"] = d1.find_element_by_xpath(".//*[@id='a_12']/div/table/tbody/tr[12]/td[7]/div/input").get_attribute("value")

	res["mobile_phone"] = res["mobile_phone"].replace(" ","")
	res["mobile_phone"] = res["mobile_phone"].replace(")","")
	res["mobile_phone"] = res["mobile_phone"].replace("(","")
	res["stac_phone"] = res["stac_phone"].replace(" ","")
	res["stac_phone"] = res["stac_phone"].replace(")","")
	res["stac_phone"] = res["stac_phone"].replace("(","")
	res["work_phone"] = res["work_phone"].replace(" ","")
	res["work_phone"] = res["work_phone"].replace(")","")
	res["work_phone"] = res["work_phone"].replace("(","")

	res["income_work"] = (res["income_work"][:-5]).replace(" ","")
	res["income_add"] = (res["income_add"][:-5]).replace(" ","")
	res["partner_income"] = (res["partner_income"][:-5]).replace(" ","")
	res["payment_house"] = (res["payment_house"][:-5]).replace(" ","")
	res["payment_credit"] = (res["payment_credit"][:-5]).replace(" ","")
	res["partner_credit"] = (res["partner_credit"][:-5]).replace(" ","")
	res["payment_other"] = (res["payment_other"][:-5]).replace(" ","")

except:
	print("error")

for key in res:
	if res[key]== "":
		res[key] = "NULL"


my_str += res["id"] +t+ res["lastname"] +t+ res["name"] +t+ res["patronymic"] +t+ res["prev_lastname"] +t+ res["date_birthday"] +t+ res["sex"] +t+ res["nationality"] +t+ \
res["place_birthday"] +t+ res["s"] +t+ res["n"] +t+ res["code_passport"] +t+ res["where_passport"] +t+ res["date_passport"] +t+ res["mobile_phone"][1:] +t+ \
res["stac_phone"] +t+ res["work_phone"] +t+ res["adr_reg"] +t+ res["adr_live"] +t+ res["family_status"] +t+ res["number_child"] +t+ res["number_dep"] +t+ res["partner_lastname"] +t+ \
res["partner_name"] +t+ res["partner_patronymic"] +t+ res["partner_birthday"] +t+ res["car"] +t+ res["type_work"] +t+ res["company_type"] +t+ res["company_name"] +t+ \
res["company_view"] +t+ res["company_status"] +t+ res["company_start"] +t+ "0" +t+ "0" +t+ res["education"] +t+ res["adr_work"] +t+ res["income_work"] +t+ \
res["income_add"] +t+ res["partner_income"] +t+ res["payment_house"] +t+ res["payment_credit"] +t+ res["partner_credit"] +t+ res["payment_other"] +t+ res["loan_purpose"]

print(res)


d1.close()

fo.write(my_str)
fo.close()


wb = xlwt.Workbook()
ws = wb.add_sheet('Result')

my_str_list = []
my_str_list = my_str.split("\t")

i = 0
for item in my_str_list:
    ws.write(0, i, item)
    i += 1
wb.save('output.xls')


print("Операция выполнена")
input("")
