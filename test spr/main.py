#! /usr/bin/env python
# -*- coding: utf-8 -*-

from zeep import Client
from zeep.transports import Transport
from requests import Session
import time
import pymssql
import config as c
from datetime import datetime, timedelta

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


t = '1'
timeout = 30

session = Session()
# session.verify = c.verify[t]
transport = Transport(session=session)

client = Client(wsdl=c.wsdl[t], transport=transport, strict=False)


stage = 10
ids = [

1031296439

]



TEST = {
    'Data': {
        'inputVector': {
            'item': [],
        }
    },

}

str_ids = ""

for id in ids:

    TEST['Data']['inputVector']['item'].append({'UCDB_ID': id, 'STAGE': stage,})
    str_ids += "'" + str(id) + "',"

str_ids = str_ids[:-1]
# print(TEST)


# 1 Send applications to SPR
res = client.service.TEST(**TEST)

print("1 Send applications to SPR")
print(res)

time.sleep(timeout)

# 2 Check SPR workflow
print("2 Check SPR workflow")
res1 = execute_db(c.test_sql[t], c.my_user, c.my_password, c.my_db, c.req1.replace("REPLACE", str_ids))
for row in res1:

    time = datetime.strptime(row[8].split('.')[0], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    print(row[0], time, (now-time)/timedelta(minutes=1), (now-time)/timedelta(minutes=1) < 5)

