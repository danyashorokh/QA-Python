
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


url1 = 'https://service.nalog.ru/inn.do'
d1 = webdriver.Chrome()
d1.get(url1)

fam = "Фамилия"
patr = "NULL"


elem = d1.find_element_by_xpath(".//*[@id='fam']")
for ch in fam[:-1]:
    elem.send_keys(ch)
if (elem.get_attribute("text")!=fam):
    elem.clear()
    for ch in fam:
        elem.send_keys(ch)

if (patr != "NULL"):
    elem = d1.find_element_by_xpath(".//*[@id='otch']")
    for ch in patr:
        elem.send_keys(ch)
else:
    d1.find_element_by_xpath(".//*[@id='unichk_0']").click()