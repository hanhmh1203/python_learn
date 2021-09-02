import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import src

action_delay_time = 2


class BaseParser():
    driver = None

    def __init__(self):
        self.init_selenium()

    def init_selenium(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--incognito')
        # options.add_argument('--headless')
        options.add_argument("user-data-dir=selenium")
        # self.driver = webdriver.Chrome('./chromedriver', chrome_options=options)
        self.driver = webdriver.Chrome('./chromedriver', chrome_options=options)
        self.driver.implicitly_wait(20)

    def close(self):
        if self.driver is not None:
            self.driver.close()
            self.driver.quit()

    def click_element_xpath(self, locator):
        self.driver.find_element_by_xpath(locator).click()
        time.sleep(action_delay_time)

    def click_element_id(self, locator):
        self.driver.find_element_by_id(locator).click()
        time.sleep(action_delay_time)

    def click_element_xpath_enter(self, locator):
        self.driver.find_element_by_xpath(locator).send_keys(Keys.ENTER)
        time.sleep(action_delay_time)

    def send_key_by_xpath(self, locator, text):
        self.driver.find_element_by_xpath(locator).send_keys(text)
        time.sleep(action_delay_time)

    def get_element_by_text(self, text):
        el = self.driver.find_element_by_xpath(f"//*[contains(text(),'{text}')]")
        return el

    def get_elements_by_xpath(self, locator):
        els = self.driver.find_elements_by_xpath(locator)
        return els

    def get_elements_class_name(self, locator):
        return self.driver.find_elements_by_class_name(locator)

    def click_element_class_name(self, locator):
        self.driver.find_element_by_class_name(locator).click()
        time.sleep(action_delay_time)

    def scroll_to_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
