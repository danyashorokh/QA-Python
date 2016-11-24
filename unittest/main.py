from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

import elements
import accounts
import texts
from clients import pool_clients as p
import fill_pages


max_wait = 15 # Задеркжа отклика страницы
timeout_auth = 15 # Ожидание перехода в ЛК после авторизации
auth_error = 5 #
firstpage_ecp1page = 10

prod_url = ""
test1_url = ""
test3_url = ""

# Инициализация
url = test3_url

log = ""
ecp1_code = "1234"

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(max_wait)

    # 15
    # Проброс на страницу ЭЦП-1
    def test_case_15(self):

        d1 = self.driver
        d1.implicitly_wait(max_wait)
        d1.get(url+"dengi3/")
        client = p["КЕЙДЖ"]
        try:
            mobile_phone = accounts.generate_new_login()
            fill_pages.fill_1_page(d1,0,0,client["lastname"],client["name"],client["patronymic"],client["date_birthday"],\
                        client["nationality"],0,fill_pages.regionDict["Москва"]["region"],mobile_phone,client["email"])
            # time.sleep(5)
            elem = d1.find_element_by_xpath(".//*[@id='submit_step1']")
            elem.click()
            time.sleep(15)

        except: print("123")

        elem = d1.find_element_by_xpath(".//*[@id='smscode']")
        # elem.click()
        elem.send_keys(ecp1_code)

        for item in elements.ecp1_page:
            self.assertTrue(item in d1.page_source, msg="Text '%s' isn't found" % item)

    # 67
    # Переход на страницу авторизации по кнопке "Личный кабинет"
    def test_case_67(self):
        d1 = self.driver
        d1.get(url)
        #self.assertIn("Деньги в долг срочно в Москве, взять денег в долг быстро | МигКредит", d1.title)
        try:
            elem = d1.find_element_by_xpath(".//*[contains(text(),'Личный кабинет')]") #.//*[@id='header_wrapper']/div/header/div/div[2]/div[2]/a[1]
            elem.click()
        except: pass

        for item in elements.elements_auth_page:
            #xpath = ".//*[contains(text(),'" + item + "')]"
            #d1.find_element_by_xpath(xpath)
             self.assertTrue(item in d1.page_source, msg="Text'%s' isn't found" % item)


    # 70
    # Ошибка авторизации (нет действующей УЗ)
    def test_case_70(self):

        d1 = self.driver
        d1.implicitly_wait(auth_error)
        d1.get(url + "login/")
        try:
            elem = d1.find_element_by_xpath(".//*[@id='lk_auth_phone']")
            elem.click()
            login = accounts.generate_new_login()
            elem.send_keys(login)
            elem = d1.find_element_by_xpath(".//*[@id='lk_auth_pswd']")
            elem.click()
            elem.send_keys(accounts.default_password)
            d1.find_element_by_xpath(".//*[@id='lk_auth_submit']").click()
            time.sleep(timeout_auth)
        except:
            pass

        for item in elements.incorrect_auth_login:
            self.assertTrue(item in d1.page_source, msg="Text '%s' isn't found" % item)

    # 71
    # Ошибка авторизации (некорректные данные по УЗ)
    def test_case_71(self):
        stats = ["3.4"]
        stats_count = len(stats)
        for stat in stats:
            if stat in accounts.account.keys():
                stats_count -= 1
                d1 = self.driver
                d1.implicitly_wait(auth_error)
                d1.get(url + "login/")
                try:
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_phone']")
                    elem.click()
                    elem.send_keys(accounts.account[stat]["login"])
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_pswd']")
                    elem.click()
                    incorrect_pwd = accounts.account[stat]["password"] + "123"
                    elem.send_keys(incorrect_pwd)
                    d1.find_element_by_xpath(".//*[@id='lk_auth_submit']").click()
                    time.sleep(timeout_auth)
                except:
                    pass

                for item in elements.incorrect_auth_pwd:
                    self.assertTrue(item in d1.page_source, msg="Text '%s' isn't found" % item)
            else:
                print(accounts.log[stat])

        self.assertEqual(stats_count, 0, msg="All statuses have not been checked")

    # 73
    # Авторизация в ЛК с заявкой в промежуточном статусе (Статус заявки 200, 201, 202, 5.5, …)
    # Description = App_InProgress
    def test_case_73(self):
        stats = ["200", "201", "202", "5.5", "5.51"]
        stats_count = len(stats)
        for stat in stats:
            if stat in accounts.account.keys():
                stats_count -= 1
                d1 = self.driver
                d1.get(url + "login/")
                try:
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_phone']")
                    elem.click()
                    elem.send_keys(accounts.account[stat]["login"])
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_pswd']")
                    elem.click()
                    elem.send_keys(accounts.account[stat]["password"])
                    d1.find_element_by_xpath(".//*[@id='lk_auth_submit']").click()
                    time.sleep(timeout_auth)
                except:
                    pass

                for item in texts.text[texts.map_texts[stat]]:
                    self.assertTrue(item in d1.page_source)
            else:
                print(accounts.log[stat])

        self.assertEqual(stats_count, 0, msg="All statuses have not been checked")

    # 74
    # Авторизация в ЛК с отмененной заявкой (Статус заявки 2.6, 5.8)
    # Description = App_Canceled
    def test_case_74(self):
        stats = ["2.6","5.8"]
        stats_count = len(stats)
        for stat in stats:
            if stat in accounts.account.keys():
                stats_count -= 1
                d1 = self.driver
                d1.get(url+"login/")
                try:
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_phone']")
                    elem.click()
                    elem.send_keys(accounts.account[stat]["login"])
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_pswd']")
                    elem.click()
                    elem.send_keys(accounts.account[stat]["password"])
                    d1.find_element_by_xpath(".//*[@id='lk_auth_submit']").click()
                    time.sleep(timeout_auth)
                except: pass

                for item in texts.text[texts.map_texts[stat]]:
                    self.assertTrue(item in d1.page_source)
            else:
                print(accounts.log[stat])

        self.assertEqual(stats_count, 0, msg="All statuses have not been checked")

    # 75
    # Авторизация в ЛК с заявкой на КЦ (Статус заявки 2.5, 2.7)
    # Description = App_InProgress_CC
    def test_case_75(self):
        stats = ["2.7"]
        stats_count = len(stats)
        for stat in stats:
            if stat in accounts.account.keys():
                stats_count -= 1
                d1 = self.driver
                d1.get(url + "login/")
                try:
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_phone']")
                    elem.click()
                    elem.send_keys(accounts.account[stat]["login"])
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_pswd']")
                    elem.click()
                    elem.send_keys(accounts.account[stat]["password"])
                    d1.find_element_by_xpath(".//*[@id='lk_auth_submit']").click()
                    time.sleep(timeout_auth)
                except:
                    pass

                for item in texts.text[texts.map_texts[stat]]:
                    self.assertTrue(item in d1.page_source)
            else:
                print(accounts.log[stat])

        self.assertEqual(stats_count, 0, msg="All statuses have not been checked")

    # 76
    # Авторизация в ЛК с заявкой на ФК (Статус заявки 6.4, 204)
    # Description = App_InProgress_Office
    def test_case_76(self):
        stats = ["6.4","204"]
        stats_count = len(stats)
        for stat in stats:
            if stat in accounts.account.keys():
                stats_count -= 1
                d1 = self.driver
                d1.get(url+"login/")
                try:
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_phone']")
                    elem.click()
                    elem.send_keys(accounts.account[stat]["login"])
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_pswd']")
                    elem.click()
                    elem.send_keys(accounts.account[stat]["password"])
                    d1.find_element_by_xpath(".//*[@id='lk_auth_submit']").click()
                    time.sleep(timeout_auth)
                except: pass

                for item in texts.text[texts.map_texts[stat]]:
                    self.assertTrue(item in d1.page_source)

        self.assertEqual(stats_count,0, msg="All statuses have not been checked")

    # 77
    # Авторизация в ЛК с заявкой на ГА (Статус заявки 5.55)
    # Description = App_Decision
    def test_case_77(self):
        stats = ["5.55"]
        stats_count = len(stats)
        for stat in stats:
            if stat in accounts.account.keys():
                stats_count -= 1
                d1 = self.driver
                d1.get(url+"login/")
                try:
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_phone']")
                    elem.click()
                    elem.send_keys(accounts.account[stat]["login"])
                    elem = d1.find_element_by_xpath(".//*[@id='lk_auth_pswd']")
                    elem.click()
                    elem.send_keys(accounts.account[stat]["password"])
                    d1.find_element_by_xpath(".//*[@id='lk_auth_submit']").click()
                    time.sleep(timeout_auth)

                except: pass

                for item in texts.text[texts.map_texts[stat]]:
                    self.assertTrue(item in d1.page_source)

        self.assertEqual(stats_count, 0, msg="All statuses have not been checked")

    def tearDown(self):
        self.driver.close()



if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    #unittest.TextTestRunner(verbosity=2).run(suite)

    #unittest.main()

    test_cases = []
    # test cases exist:
    # 15 67 70 71 73 - 77
    test_numbers = [67,'70-71','73-77'] # диапазоны кейсов необходимо задавать в виде строки: например, "50-60"
    for item in test_numbers:
        item = str(item)
        if item.find("-",0,len(item)) < 0:
            test_cases.append("test_case_"+str(item))
        else:
            index = item.split("-")
            for i in range(int(index[0]),int(index[1])+1):
                test_cases.append("test_case_" + str(i))

    #test_cases = ['test_case_67', 'test_case_77']
    suite = unittest.TestSuite(map(Test, test_cases))
    unittest.TextTestRunner(verbosity=2).run(suite)
