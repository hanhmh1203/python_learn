from selenium import webdriver
import time

from xlsxwriter import Workbook

from src.scrapy.journeyinlife.journey.journey.locator import bluesprint_locator
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from src.scrapy.journeyinlife.journey.journey.items import JourneyItem
import xlsxwriter
import hashlib

time_loading = 2


class JourneyParse:
    page_total = 5
    driver = None
    page_number = 1
    count = 1
    workbook = None
    worksheet = None

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome('./chromedriver', chrome_options=options)
        self.workbook = xlsxwriter.Workbook(f'journey_in_life_{self.page_total}.xlsx')

        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write('A1', 'STT')
        self.worksheet.write('B1', 'Key')
        self.worksheet.write('C1', 'Title')
        self.worksheet.write('D1', 'Meaning')
        self.worksheet.write('E1', 'Link')
        self.worksheet.write('F1', 'Image_Link')
        self.worksheet.write('G1', 'thumb_Link')

    def parse_list_soup(self):
        self.list_item = []
        url = f'https://www.journeyinlife.net/search/label/phrase?v=full&page={self.page_number}'
        self.driver.get(url)
        print(f"url: {url}")
        time.sleep(time_loading)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        row = soup.find('div', class_='row')
        list_phrase = row.find_all('div', class_='col-md-4')

        for i in list_phrase:
            item_journey = JourneyItem()
            a = i.find('a')
            link = a.get('href')
            item_journey.link = link
            # print(link)
            img = a.find('img').get('data-src')
            item_journey.thumb = img
            # print(img)
            title = i.find('div', class_='title').text
            item_journey.key = hashlib.md5(title.encode()).hexdigest()
            item_journey.title = title
            self.list_item.append(item_journey)

            print(item_journey.title)

        for detail in self.list_item:
            self.parse_detail(detail)

        self.writer_csv(list_item=self.list_item)

        if self.page_number < self.page_total:
            self.page_number += 1
            self.parse_list_soup()

    # def tag_content(self, tag):
    #     return tag['class'] == 'col-md-4' and tag.parent['class'] == 'row'

    def parse_detail(self, item_journey):
        self.driver.get(item_journey.link)
        print(f"url: {item_journey.link}")
        time.sleep(time_loading)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        page = soup.find('div', class_='entry-body')
        item_journey.image = page.find('img').get('src')

        texts = page.findAll('div', {'style': 'text-align: justify;'})
        for text in texts:
            item_journey.str_content = f'{item_journey.str_content} \n ' \
                                       f'{text.text}'
            # item_journey.content.append(text.text)

        print(item_journey.title)

    def close(self):
        self.workbook.close()
        self.driver.close()
        self.driver.quit()

    def writer_csv(self, list_item):

        print('writer excel')

        for i in range(len(list_item)):
            row_number = self.count + 1
            self.worksheet.write(f'A{row_number}', f'{self.count}')
            self.worksheet.write(f'B{row_number}', list_item[i].key)
            self.worksheet.write(f'C{row_number}', list_item[i].title)
            self.worksheet.write(f'D{row_number}', list_item[i].str_content)
            self.worksheet.write(f'E{row_number}', list_item[i].link)
            self.worksheet.write(f'F{row_number}', list_item[i].image)
            self.worksheet.write(f'G{row_number}', list_item[i].thumb)
            self.count += 1


if __name__ == '__main__':
    parse = JourneyParse()
    try:
        parse.parse_list_soup()
    except:
        parse.close()
    parse.close()
