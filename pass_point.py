#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time

fi = open('input1.txt','r')
fo = open('output1.txt','w')

e_list = []
my_str = ""

for line in fi:
    my_str += line

e_list = my_str.split("\n")
print(e_list)

fi.close()

res = ""
desc_point = ""
pre = ""
t = "\t"

url = 'https://anketa.alfabank.ru/alfaform-pil/endpoint?platformId=alfasite'
max_wait = 1 # максимальное ожидание браузера

d1 = webdriver.Chrome()
d1.implicitly_wait(max_wait)
d1.get(url)



elem1 = d1.find_element_by_xpath(".//*[@id='passportOfficeCode-id']")
elem2 = d1.find_element_by_xpath(".//*[@id='passportOffice-id']")



for em in e_list:
    if(em and len(em) == 7):
        elem1.click()
        elem1.clear()
        elem2.click()
        elem2.clear()
        elem1.click()
        elem1.send_keys(em)
        time.sleep(1)
        elem1.click()
        elem2.click()
        time.sleep(3)

        try:
            desc_point = elem2.get_attribute("value")
            if(desc_point):
                res = res + em + t + desc_point + "\n"
            else:
                res = res + em + t + "unknown" + "\n"

        except: pass
    else: res = res + em + t + "uncorrect code" + "\n"

d1.close()

fo.write(res)
fo.close()

print(res.count("unknown"))

print("Операция выполнена")
input("")
