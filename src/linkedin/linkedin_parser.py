from selenium import webdriver
import time

from src.BaseParser import BaseParser
from src.linkedin import locator


class linkedin_parser(BaseParser):
    def __init__(self):
        super().__init__()
        self.locator = locator
