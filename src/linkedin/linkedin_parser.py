from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys

from src.BaseParser import BaseParser
from src.linkedin import locator, information

sleep_time = 2


class linkedin_parser(BaseParser):
    def __init__(self):
        super().__init__()
        self.locator = locator

    url = 'https://www.linkedin.com/'
    url_sign_in = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'

    def login(self):
        self.driver.get(url=self.url_sign_in)
        time.sleep(sleep_time)
        self.driver.find_element_by_id(self.locator.user_name_id).send_keys(information.username)
        self.driver.find_element_by_id(self.locator.password_id).send_keys(information.password)
        self.click_element_xpath('//*[@id="organic-div"]/form/div[3]/button')

    def search(self):
        # value = input('input search something: ')
        value = ''
        time.sleep(sleep_time)
        self.send_key_by_xpath(self.locator.filter.xpath_search_box, value)
        # self.driver.find_element_by_xpath(self.locator.xpath_search_box).send_keys(value)
        self.click_element_xpath_enter(self.locator.filter.xpath_search_box)
        self.click_element_xpath(self.locator.filter.xpath_search_people)
        self.click_element_xpath(self.locator.filter.xpath_all_filter)
        # self.click_element_xpath(self.locator.xpath_button_load_more)
        self.click_element_xpath(self.locator.filter.xpath_locations_vietnam)
        # self.click_element_xpath(self.locator.filter.xpath_locations_hochiminh)
        self.click_element_xpath(self.locator.filter.xpath_show_results)


if __name__ == '__main__':
    parser = linkedin_parser()
    parser.login()
    parser.search()
