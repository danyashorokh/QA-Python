#! /usr/bin/env python
# -*- coding: utf-8 -*-

from zeep import Client
from zeep.transports import Transport
from requests import Session
import time
import data as d
import pymssql
import sys
import config as c

# SQL request
def execute_db(host,user,password,db,request):
    res = []
    conn = pymssql.connect(host, user, password, db)
    # print("I AM IN DB!")
    cur = conn.cursor()
    cur.execute(request)

    for row in cur:
        #print(row)
        res.append(row)
    conn.close()
    # print(request)
    return res

max_count = 10
timeout = 30

session = Session()
session.verify = c.verify
transport = Transport(session=session)

client = Client(wsdl=c.wsdl, transport=transport, strict=False)


SendApplication = d.SendApplication

# 1 SendApplication
UCDB_ID = client.service.SendApplication(**SendApplication).bankApplicationId
print("1 SendApplication")

# UCDB_ID = '1016051084'
print("UCDB_ID: " + UCDB_ID)

count = 0
while(count < max_count):
    status = execute_db(c.test3_sql, c.my_user, c.my_password, c.my_db, c.req1.replace("REPLACE", UCDB_ID))[0][2]
    print("Status: " + status)
    if status != '5.0':
        if count == max_count-1:
            sys.exit(1)
        else:
            count += 1
            time.sleep(timeout)
    else: break

# 2 ConfirmOffer
ConfirmOffer = d.ConfirmOffer
ConfirmOffer['bankApplicationId'] = UCDB_ID
client.service.ConfirmOffer(**ConfirmOffer)
print("2 ConfirmOffer")

time.sleep(10)

count = 0
while(count < max_count):
    status = execute_db(c.test3_sql, c.my_user, c.my_password, c.my_db, c.req1.replace("REPLACE", UCDB_ID))[0][2]
    print("Status: " + status)
    if status != '5.4':
        if count == max_count-1:
            sys.exit(1)
        else:
            count += 1
            time.sleep(timeout)
    else: break

# 3 GetAgreementInfo
GetAgreementInfo = d.GetAgreementInfo
GetAgreementInfo['bankApplicationId'] = UCDB_ID
client.service.GetAgreementInfo(**GetAgreementInfo)
print("3 GetAgreementInfo")
time.sleep(5)

# 4 GetPrintForms
GetPrintForms = d.GetPrintForms
GetPrintForms['bankApplicationId'] = UCDB_ID
client.service.GetPrintForms(**GetPrintForms)
print("4 GetPrintForms")
time.sleep(5)

# 5 ConfirmAgreement
ConfirmAgreement = d.ConfirmAgreement
ConfirmAgreement['bankApplicationId'] = UCDB_ID
client.service.ConfirmAgreement(**ConfirmAgreement)
print("5 ConfirmAgreement")
time.sleep(5)

count = 0
while(count < max_count):
    status = execute_db(c.test3_sql, c.my_user, c.my_password, c.my_db, c.req1.replace("REPLACE", UCDB_ID))[0][2]
    print("Status: " + status)
    if status != '7.1':
        if count == max_count-1:
            sys.exit(1)
        else:
            count += 1
            time.sleep(timeout)
    else: break

application_number = execute_db(c.test3_sql, c.my_user, c.my_password, c.my_db,
                                c.req2.replace("REPLACE", UCDB_ID))[0][2]
print("Application_number: " + application_number)

# 6 SendScans
# SendScans = d.SendScans
# SendScans['bankApplicationId'] = UCDB_ID
# client.service.SendScans(**SendScans)
