from selenium import webdriver
import src

class BaseParser():
    driver = None

    def __init__(self):
        self.init_selenium()

    def init_selenium(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        # self.driver = webdriver.Chrome('./chromedriver', chrome_options=options)
        self.driver = webdriver.Chrome('./chromedriver')

    def close(self):
        if self.driver is not None:
            self.driver.close()
            self.driver.quit()

