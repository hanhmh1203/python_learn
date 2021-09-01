from selenium import webdriver
import time

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
        self.driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()


if __name__ == '__main__':
    parser = linkedin_parser()
    parser.login()
