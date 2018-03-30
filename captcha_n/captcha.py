
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import *
import sys
import os
import requests
import cv2
import numpy as np
from datetime import datetime

proxies = {
    "https": "https://dshorokh:Password40@fx-proxy:8080",
    "http": "http://dshorokh:Password40@fx-proxy:8080",
}

api_key = "6f5a3f20dfe0fe9cd15e5f08a1c9a0af"

captcha_id = ""

# https://rucaptcha.com
# login: testmigcredit@gmail.com
# pass: Migcredit

# обновите драйвер хрома https://chromedriver.storage.googleapis.com/index.html?path=2.35/

# Функция ожидания загрузки элемента на странице
def wait_form(driver, type, path, one_time, max_time, final_text):
    flag1 = 0
    while (True):
        if flag1 == max_time:
            print(final_text)
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
    if flag1 > 1:
        print("Ожидали %d раз(а) по %d секунды" % (flag1, one_time))

def get_captcha(file_name):
    path = os.getcwd() +"/"+file_name
    mime='image/jpeg'
    url1 = "http://rucaptcha.com/in.php"

    files = [
        ('file', ('captcha', open(path, 'rb'), mime))
    ]
    data1 = {
        'method': 'post',
        'key': api_key,
        'phrase': 0,
        'regsense': 0,
        'numeric': 1,
        'min_len': 0,
        'max_len': 30,
        'language': 0
    }

    #def captcha(file_name):

    r = requests.post(url1, files=files, data=data1, proxies=proxies)
    print(r.status_code)
    if r.status_code == 200:
        content = str(r.content)
    if "|" in content:
            code, captcha_id = content.split('|', 1)
            code = code[2:4]
            captcha_id = captcha_id[:-1]
            if code == "OK":
                print("captcha_id: {captcha_id!r}".format(captcha_id=captcha_id))



    url2 = "http://rucaptcha.com/res.php?key={apikey}&action=get&id={captcha_id}".format(apikey=api_key, captcha_id=captcha_id)

    # url_bad = "http://rucaptcha.com/res.php?key={apikey}&action=reportbad&id={captcha_id}".format(apikey=api_key, captcha_id=captcha_id)

    value = ""

    while(1):
        time.sleep(5)
        r = requests.get(url2, proxies=proxies)
        if r.status_code == 200:
            content = str(r.content)
            if "CAPCHA_NOT_READY" in content:
                print("Capcha not ready.")
            elif "|" in content:
                code, value = content.split("|", 1)
                code = code[2:4]
                value = value[:-1]
                if code == "OK":
                    print(code, value)
                    break
                else:
                    print("Error code: {code!r} => {value!r}".format(code=code, value=value))
                    break
            else:
                print("Unknown response: {response!r}".format(response=content))
                break

    return value

# input format
# Варфоламеева	Ирина	Валерьевна	1989-02-21	3711	458808	2012-01-25
# разделены \t

fi = open('input.txt','r')
os.remove(os.getcwd() + "/output.txt")
fo = open('output.txt','w')

e_list = []
my_str = ""

for line in fi:
    my_str += line
e_list = my_str.split("\n")

#print(e_list)

fi.close()

url1 = 'https://service.nalog.ru/inn.do'
url2 = 'http://imacros2.rucaptcha.com/new/'
max_wait = 3  # максимальное ожидание браузера

d1 = webdriver.Chrome()
d1.implicitly_wait(max_wait)
#d2 = webdriver.Chrome()
#d2.implicitly_wait(max_wait)

time.sleep(4)

i = 1



for em in e_list:

    d1.get(url1)
    d1.execute_script("window.scrollTo(0, 0)")
    time.sleep(2)
    res = ""
    res += em

    wait_form(d1, "xpath", ".//*[@id='fam']", 5, 10, "Форма ввода данных не загружается")

    if(em):

        print(str(i)+"\t"+str(datetime.now())+": ")

        data = []
        data = em.split("\t")

        date = data[3].split("-")
        data[3] = date[2]+"."+date[1]+"."+date[0]
        date = data[6].split("-")
        data[6] = date[2] + "." + date[1] + "." + date[0]

        elem = d1.find_element_by_xpath(".//*[@id='fam']")
        for ch in data[0]:
            elem.send_keys(ch)
        # resend fam
        if (elem.get_attribute("text") != data[0]):
            elem.clear()
            for ch in data[0]:
                elem.send_keys(ch)

        elem = d1.find_element_by_xpath(".//*[@id='nam']")
        for ch in data[1]:
            elem.send_keys(ch)

        if (data[2]!= "NULL"):
            elem = d1.find_element_by_xpath(".//*[@id='otch']")
            for ch in data[2]:
                elem.send_keys(ch)
        else:
            d1.find_element_by_xpath(".//*[@id='unichk_0']").click()

        d1.find_element_by_xpath(".//*[@id='bdate']").send_keys(data[3])
        if len(data[5]) < 6:
            data[5] = (6-len(data[6]))*"0"+data[5]
        d1.find_element_by_xpath(".//*[@id='docno']").send_keys(data[4][0:2]+" "+data[4][2:4]+" "+data[5])
        d1.find_element_by_xpath(".//*[@id='docdt']").send_keys(data[6])

        #d1.find_element_by_xpath(".//*[@id='frmInn']/div[2]/div/div[1]/div[10]/div/div/a").click()


        img = d1.find_element_by_xpath(".//*[@id='frmInn']/div[5]/div[1]/div[10]/div/div/img")

        loc = img.location
        # print(loc)

        scroll = "window.scrollTo(0, " + str(loc['y'])+")"
        d1.execute_script(scroll)
        d1.save_screenshot('screenshot.png')

        page_size = d1.get_window_size()
        y_from_down = page_size['height'] - loc['y']
        #print(page_size['height'], loc['y'], y_from_down)

        #print(loc)

        image = cv2.imread('screenshot.png', 0)
        out = image

        x_roi = loc['x']
        y_roi = loc['y']
        h,w = image.shape

        y_roi = y_from_down + 80
        #print(y_roi)

        out = out[y_roi:y_roi+100, x_roi:x_roi+200]
        cv2.imwrite('captcha.png', out)

        '''
        # get the image source
        img = d1.find_element_by_xpath(".//*[@id='frmInn']/div[5]/div[1]/div[10]/div/div/img")
        src = img.get_attribute('src')

        d2.get(src)
        d2.save_screenshot("captcha.png")
        '''

        #d2.get(url2)


        #wait_form(d2, "xpath", "html/body/form/input[1]", 3, 30, "Форма распознавания капчи не загружается")

        #d2.find_element_by_xpath("html/body/form/input[1]").send_keys(api_key)
        #d2.find_element_by_xpath("html/body/form/input[2]").send_keys(os.getcwd() + "/captcha.png")

        #time.sleep(1)

        #d2.find_element_by_xpath("html/body/form/input[4]").click() # captcha send

        #time.sleep(10)

        #cap = d2.find_element_by_xpath("html/body").text
        #print(cap)

        cap = get_captcha("captcha.png")

        if len(cap) == 6:
            for ch in cap:
                d1.find_element_by_xpath(".//*[@id='captcha']").send_keys(ch)

            d1.find_element_by_xpath(".//*[@id='btn_send']").click()

            wait_form(d1, "xpath", ".//*[@id='resultInn']", 4, 3, "Результата нет")

            inn = d1.find_element_by_xpath(".//*[@id='resultInn']").text

            if len(inn) == 12:
                res += "\t" + inn + "\n"
                #print(inn)
            else:
                try:
                    d1.find_element_by_xpath(".//label[contains(text(),'Цифры с картинки введены неверно')]")
                    url_bad = "http://rucaptcha.com/res.php?key={apikey}&action=reportbad&id={captcha_id}".format(
                        apikey=api_key, captcha_id=captcha_id)
                    r1 = requests.get(url_bad, proxies=proxies)
                    if r1.status_code == 200:
                        # print("Жалоба на неправильное решение отправлена\n")
                        res += "\t" + "Жалоба на неправильное решение отправлена\n"
                    else:
                        # print("Жалоба на неправильное решение не отправлена\n")
                        res += "\t" + "Жалоба на неправильное решение не отправлена\n"
                except:
                    res += "\t" + "не найден\n"

            #d1.find_element_by_xpath(".//*[@id='frmInn']/div[2]/div/div[1]/div[10]/div/div/a").click()

        #if cap == "ERROR_CAPTCHA_UNSOLVABLE":

        #    res += "\t" + "некорректная капча\n"


        else: pass

        time.sleep(2)
        #sys.exit(1)

    # Неправильно решена
    else: pass


    #os.remove(os.getcwd() + "/captcha.png")

    fo = open('output.txt', 'a')
    fo.write(res)
    fo.close()

    while not fo.closed:
        time.sleep(1)

    print(str(cap)+"\t"+ res)
    i += 1



d1.close()
#d2.close()

#fo.write(res)
#fo.close()

print("Операция выполнена")
input("")
sys.exit(1)
