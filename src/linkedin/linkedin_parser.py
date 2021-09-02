from selenium import webdriver
import time
import pickle

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
        time.sleep(5)
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

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

    def load_season(self):
        self.driver.get(url=self.url)

    def open_search(self):
        self.driver.get(url=self.locator.filter.url_search)
        time.sleep(5)
        els = self.get_elements_class_name('entity-result__image')
        #
        print(f'els size {len(els)}')
        if len(els) > 0:
            print(f'click image avg id{els[0].id}')
            els[0].click()

        # for i in range(3):
        #     print('scroll')
        #     self.scroll_to_down()
        #     time.sleep(1)
        #     print('click xpath')
        #     self.click_element_class_name(self.locator.filter.class_name_button_next)
        #     time.sleep(5)


if __name__ == '__main__':
    parser = linkedin_parser()
    # parser.login()
    parser.open_search()
    time.sleep(10)
