
import pymssql
import sha1

my_host = ''
my_user = ''
my_password = ''
my_db = ''

account = {}

status_group_1 = ['5.55', '6.4']
req1 = """select *"""

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
    return res

for item in status_group_1:
    res = execute_db(my_host, my_user, my_password, my_db, req1.replace("REPLACE", item))
    if res:
        print(res[0][0], res[0][1], item)
        if(str(res[0][1]) in sha1.pwd_dict.keys()):
            account[item] = {}
            account[item]["login"] = res[0][0]
            account[item]["password"] = sha1.pwd_dict[res[0][1]]
        else:
            print("Password for login=%s isn't found\n" % res[0][0])
    else: print("Accounts with status=%s aren't found\n" % item)

