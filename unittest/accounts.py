
import pymssql
import sha1
import sql_reqs
import main
from datetime import datetime


test1_sql = ''
test3_sql = ''

my_host = test3_sql
my_user = ''
my_password = ''
my_db = ''

account = {}

log = {}
status_group_1 = ['200','201','202','5.5','5.51','3.4','2.5','2.7','2.6','5.8','5.55', '6.4', '204']
#status_group_1 = ['2.5']

req_add = "" # Дополнительная строка в запрос

used_logins = [] # Список для создаваемых новых номеров телефона
bad_pass_logins = []

default_password = "1234"


# Функция выполняющая запрос в SQL
def execute_db(host,user,password,db,request):
    res = []
    conn = pymssql.connect(host, user, password, db)
    #print("aloha db!\n")
    cur = conn.cursor()
    cur.execute(request)

    for row in cur:
        #print(row)
        res.append(row)
    conn.close()
    # print(request)
    return res

def generate_new_login():
    # Генерация номера телефона, для которого нет ЛК
    while(True):
        new_login = (str(datetime.now()))[11:-2]
        new_login = new_login.replace(":", "")
        new_login = new_login.replace(".", "")
        #print(new_login)
        incorrect_login = execute_db(my_host, my_user, my_password, my_db, sql_reqs.req2.replace("REPLACE", new_login))
        if not incorrect_login and new_login not in used_logins:
            used_logins.append(new_login)
            main.log += "generated new login: " + str(new_login) + "\n"
            break
    return new_login

# Подтягивание учетных записей для статусов из группы 1
for item in status_group_1:
    while(True):
        res = execute_db(my_host, my_user, my_password, my_db, sql_reqs.req1.replace("REPLACE", item)+req_add)
        req_add = ""
        if res:
            #main.log += str(res) + "\n"
            #print(res[0][0], res[0][1], item)
            if(str(res[0][1]) in sha1.pwd_dict.keys()):
                account[item] = {}
                account[item]["login"] = res[0][0]
                account[item]["password"] = sha1.pwd_dict[res[0][1]]
                #main.log += "sha1: "+ str(sha1.pwd_dict[res[0][1]]) + "\n"
                break
            else:
                log[item] = "Password for login=%s isn't found\n" % res[0][0]
                #main.log += "Password for login=%s isn't found\n" % res[0][0] + "\n"
                bad_pass_logins.append(res[0][0])
                req_add = " and ta.Login not in ("
                for login in bad_pass_logins:
                    req_add += "'" + str(login) + "',"
                req_add = req_add[0:len(req_add)-1]
                req_add += ")"

                #print(log[item])
        else:
            log[item] = "Accounts with status=%s aren't found\n" % item
            # main.log += "Accounts with status=%s aren't found\n" % item + "\n"
            # print(log[item])
        break

print(account)

