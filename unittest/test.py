from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

import elements
import accounts
import texts


max_wait = 15 # Задеркжа отклика страницы
timeout_auth = 15 # Ожидание перехода в ЛК после авторизации

prod_url = ""
test1_url = ""
test3_url = ""

# Инициализация
url = test3_url



class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(max_wait)

    # 67
    # Переход на страницу авторизации по кнопке "Личный кабинет"
    def test_case_67(self):
        d1 = self.driver
        d1.get(url)
        #self.assertIn("Деньги в долг срочно в Москве, взять денег в долг быстро | МигКредит", d1.title)
        try:
            elem = d1.find_element_by_xpath(".//*[contains(text(),'Личный кабинет')]") #.//*[@id='header_wrapper']/div/header/div/div[2]/div[2]/a[1]
            elem.click()
            for item in elements.elements_auth_page:
                #xpath = ".//*[contains(text(),'" + item + "')]"
                #d1.find_element_by_xpath(xpath)
                self.assertTrue(item in d1.page_source)
        except: pass

    # 76
    # Авторизация в ЛК с заявкой на ФК (Статус заявки 6.4, 204)
    # Description = App_InProgress_Office
    def test_case_76(self):
        stat = "6.4"
        if stat in accounts.account.keys():
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

            for item in texts.text["144"]:
                self.assertTrue(item in d1.page_source)

        self.assertTrue(stat in accounts.account.keys())

    # 77
    # Авторизация в ЛК с заявкой на ГА (Статус заявки 5.55)
    # Description = App_Decision
    def test_case_77(self):
        stat = "5.55"
        if stat in accounts.account.keys():
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

            for item in texts.text["145"]:
                self.assertTrue(item in d1.page_source)

        self.assertTrue(stat in accounts.account.keys())


    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    #unittest.TextTestRunner(verbosity=2).run(suite)

    #unittest.main()
    test_cases = []
    test_numbers = [76,77]
    for item in test_numbers:
        test_cases.append("test_case_"+str(item))
    #test_cases = ['test_case_67', 'test_case_77']
    suite = unittest.TestSuite(map(Test, test_cases))
    unittest.TextTestRunner(verbosity=2).run(suite)