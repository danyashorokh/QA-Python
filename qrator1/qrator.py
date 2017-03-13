import win32com
import csv # imports the csv module
import sys # imports the sys module
import re
import datetime
import time
import config as c

import os, uuid
import itertools as it
from win32com import client

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import *

fi = open('log.txt', 'r')

e_list = []
my_str = ""
flag = False

try:
    #fi = open('log.txt', 'a')
    #with open('log.txt', 'a') as fi:
    for line in fi:
        my_str += line
except OSError:
    pass

fi.close()
while not fi.closed:
    time.sleep(1)

if my_str:
    e_list = my_str.split("\n")

print(e_list)

def makeDocumentGenerator(folderName):
    # Get folder
    folder = notesDatabase.GetView(folderName)
    if not folder:
        raise Exception('Folder "%s" not found' % folderName)
    # Get the first document
    document = folder.GetFirstDocument()
    # If the document exists,
    while document:
        # Yield it
        yield document
        # Get the next document
        document = folder.GetNextDocument(document)

def send_mail(subject, body_text, sendto, copyto=None, blindcopyto=None, attach=None):


    doc = notesDatabase.CreateDocument()
    doc.ReplaceItemValue("Form", "Memo")
    doc.ReplaceItemValue("Subject", subject)

    # assign random uid because sometimes Lotus Notes tries to reuse the same one
    uid = str(uuid.uuid4().hex)
    doc.ReplaceItemValue('UNIVERSALID', uid)

    # "SendTo" MUST be populated otherwise you get this error:
    # 'No recipient list for Send operation'
    doc.ReplaceItemValue("SendTo", sendto)

    if copyto is not None:
        doc.ReplaceItemValue("CopyTo", copyto)
    if blindcopyto is not None:
        doc.ReplaceItemValue("BlindCopyTo", blindcopyto)

    # body
    body = doc.CreateRichTextItem("Body")
    body.AppendText(body_text)

    # attachment
    if attach is not None:
        attachment = doc.CreateRichTextItem("Attachment")
        for att in attach:
            attachment.EmbedObject(1454, "", att, "Attachment")

    # save in `Sent` view; default is False
    doc.SaveMessageOnSend = False
    doc.Send(False)


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


#Connect to notes database on server
notesSession = win32com.client.Dispatch('Lotus.NotesSession')
notesSession.Initialize(c.notesPass)
notesDatabase = notesSession.GetDatabase(c.notesServer,c.notesFile)

''''
# Get a list of folders
for view in notesDatabase.Views:
    if view.IsFolder:
        print(view.Name)
'''

fi = open('log.txt', 'a')
for document in makeDocumentGenerator('тест'):

    subject = document.GetItemValue('Subject')[0].strip()
    date = str(document.GetItemValue('PostedDate')[0])

    #print(date,e_list)
    if date not in e_list:
        flag = True
        fi.write(date+"\n")

    print(subject,document.GetItemValue('From')[0].strip(), date)


fi.close()
while not fi.closed:
    time.sleep(1)


if flag:
    print("begin")
    d1 = webdriver.Chrome()
    d1.maximize_window()
    d1.implicitly_wait(25)
    d1.get(c.url)

    d1.find_element_by_xpath("html/body/div[2]/div/form/div[1]/div/input").send_keys(c.login)
    d1.find_element_by_xpath("html/body/div[2]/div/form/div[2]/div/input").send_keys(c.password)

    time.sleep(2)

    d1.find_element_by_xpath("html/body/div[2]/div/form/button").click()

    wait_form(d1, "xpath", ".//*[@id='row_1452']/td[1]/a[1]", 10, 3, "Страница Live stats не загружается")

    wait_form(d1, "xpath", ".//*[@id='contol-holder']/span", 10, 3, "Страница с графиком не загружается")

    time.sleep(5)

    d1.save_screenshot('screenshot.png')

    d1.close()

    subject = "QRator screenshot"
    body = ""
    sendto = [c.sendto, ]
    files = [os.getcwd()+'/screenshot.png']
    attachment = it.takewhile(lambda x: os.path.exists(x), files)
    print("attached")
    send_mail(subject, body, sendto, attach=attachment)
    print("send")

    flag = False
