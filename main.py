import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class ExpertVoice(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_login_error_handle_sleep(self):
        login_page = 'https://www.expertvoice.com/sign-in'
        expected_alert = 'This account information is incorrect. Would you like to sign up or reset your password?'

        driver = self.driver
        driver.get(login_page)
        login_button = driver.find_element_by_class_name('button')

        interactions = ActionChains(driver)
        interactions.click(login_button)
        interactions.perform()

        time.sleep(1)
        login_alert = driver.find_element_by_class_name('alert-content')
        self.assertTrue(expected_alert == login_alert.text, "Login alert is incorrect")

    def test_login_error_handle_polling(self):
        login_page = 'https://www.expertvoice.com/sign-in'
        expected_alert = 'This account information is incorrect. Would you like to sign up or reset your password?'
        tries = 10

        driver = self.driver
        driver.get(login_page)
        login_button = driver.find_element_by_class_name('button')

        interactions = ActionChains(driver)
        interactions.click(login_button)
        interactions.perform()

        alert_does_not_exist = True
        login_alert = ''
        attempt_num = 0
        while alert_does_not_exist and attempt_num < tries:
            try:
                login_alert = driver.find_element_by_class_name('alert-content')
            except Exception as e:
                print("LOG: TRY #{} ALERT NOT FOUND\n{}".format(attempt_num+1, e))
                continue
            finally:
                attempt_num += 1
                if login_alert:
                    alert_does_not_exist = False
                    print("LOG: ALERT DETECTED")
                else:
                    time.sleep(1)

        self.assertTrue(login_alert, "Unable to find the error handling alert")
        self.assertTrue(expected_alert == login_alert.text, "Login alert is incorrect")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
