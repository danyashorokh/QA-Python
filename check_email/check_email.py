#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time

fi = open('input.txt','r')

e_list = []
len_list = []
my_str = ""
i = 1


for line in fi:
    my_str += line
    len_list.append(len(line[:-1]))
max_len = max(len_list)

e_list = my_str.split("\n")
print(e_list)

fi.close()

lastname = "Фамилия"
firstname = "Имя"
patr = "Отчество"
phone = "9091111111"

url = ''
max_wait = 1 # максимальное ожидание браузера

d1 = webdriver.Chrome()
d1.implicitly_wait(max_wait)
d1.get(url)

time.sleep(5)

try:
    elem0 = d1.find_element_by_class_name("formCalculator__submit")
    elem0.click()
except:
    print("button isn't found")

elem1 = d1.find_element_by_xpath(".//*[@id = 'signupForm.model.lastName']")
elem1.click()
elem1.send_keys(lastname)

elem = d1.find_element_by_xpath(".//*[@id = 'signupForm.model.firstName']")
elem.click()
elem.send_keys(firstname)

elem = d1.find_element_by_xpath(".//*[@id = 'signupForm.model.patronymic']")
elem.click()
elem.send_keys(patr)

elem = d1.find_element_by_xpath(".//*[@id='fields-container']/mobile-phone/div/div/input[1]")
elem.click()
elem.send_keys(phone)

for em in e_list:
    res = ""

    if(em):

        elem = d1.find_element_by_xpath(".//*[@id='modelEmail']")



        try:

            if (i == 3): d1.find_element_by_class_name("123")
            elem.click()
            elem.clear()
            elem.send_keys(em)

            elem1.click()
        except:
            print("Error with e-mail", em)
            print("There is POPUP on stage!")

            '''
            # Switch to new window opened
            d1.switch_to.window(d1.window_handles[-1])
            # Close the new window
            d1.close()
            # Switch back to original browser (first window)
            d1.switch_to.window(d1.window_handles[0])
            '''
            d1.switch_to.alert()
            print("It's switched to alert")
            time.sleep(10)
            d1.close()
            d1.switch_to.window(d1.window_handles[0])
            #(*//li[contains(@id,'topic_roles_input')]//input[@type="checkbox"])[2]



        #if(d1.find_element_by_xpath(".//*[@id='fields-container']/email/div[1]/div/span[1]/span").is_displayed()):
        #if(d1.find_element_by_xpath(".//span[@class='form__error-box']")):
        try:
            d1.find_element_by_xpath(".//span[contains(text(),'Пользователь с такой электронной почтой уже зарегистрирован.')]")
            res = res + em + (max_len - len(em) + 5)*" " + "exist"
        except:
            res = res + em + (max_len - len(em) + 5)*" " + "not exist"
    else: pass

    fo = open('output.txt', 'a')
    fo.write(res)
    fo.close()

    while not fo.closed:
        time.sleep(1)

    print(str(i)+" "+res)
    i += 1



d1.close()

#fo.write(res)
#fo.close()

print("Операция выполнена")
input("")
