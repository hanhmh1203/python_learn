from selenium import webdriver
import time

import openpyxl

from src.scrapy.journeyinlife.journey.journey.locator import bluesprint_locator
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from src.scrapy.journeyinlife.journey.journey.items import JourneyItem
import xlsxwriter
import hashlib

time_loading = 2


class JourneyParse:
    page_total = 990
    driver = None
    page_number = 975
    count = 11689
    workbook = None
    worksheet = None

    def init_excel(self):
        try:
            self.workbook = openpyxl.load_workbook(f'journey_in_life_{self.page_total}.xlsx')
        except FileNotFoundError:
            openpyxl.Workbook().save(f'journey_in_life_{self.page_total}.xlsx')
            self.workbook = openpyxl.load_workbook(f'journey_in_life_{self.page_total}.xlsx')

        self.worksheet = self.workbook.active

        cell_obj = self.worksheet.cell(row=1, column=1)
        if cell_obj.value is None:
            self.worksheet['A1'].value = 'STT'
            self.worksheet['B1'].value = 'Key'
            self.worksheet['C1'].value = 'Title'
            self.worksheet['D1'].value = 'Meaning'
            self.worksheet['E1'].value = 'Link'
            self.worksheet['F1'].value = 'Image_Link'
            self.worksheet['G1'].value = 'thumb_Link'
        self.workbook.save(f'journey_in_life_{self.page_total}.xlsx')

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome('./chromedriver', chrome_options=options)


    def parse_list_soup(self):
        start_time = time.time()
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
            # a = i.find('a')
            # link = a.get('href')
            # img = a.find('img').get('data-src')
            item_journey.link = i.find('a').get('href')
            item_journey.thumb = i.find('a').find('img').get('data-src')
            title = i.find('div', class_='title').text

            item_journey.key = hashlib.md5(title.encode()).hexdigest()
            item_journey.title = title
            self.list_item.append(item_journey)

        # for detail in self.list_item:
        #     self.parse_detail(detail)

        self.writer_csv(list_item=self.list_item)
        print("--- %s seconds ---" % (time.time() - start_time))
        if self.page_number < self.page_total:
            self.page_number += 1
            self.parse_list_soup()


    # def tag_content(self, tag):
    #     return tag['class'] == 'col-md-4' and tag.parent['class'] == 'row'

    def parse_detail(self, item_journey):
        self.driver.get(item_journey.link)
        print(f"url: {item_journey.link}")
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
        self.workbook.save(f'journey_in_life_{self.page_total}.xlsx')
        self.workbook.close()
        self.driver.close()
        self.driver.quit()

    def writer_csv(self, list_item):
        print('writer excel')
        self.init_excel()
        for i in range(len(list_item)):
            row_number = self.count + 1
            self.worksheet[f'A{row_number}'].value = f'{self.count}'
            self.worksheet[f'B{row_number}'].value = list_item[i].key
            self.worksheet[f'C{row_number}'].value = list_item[i].title
            self.worksheet[f'D{row_number}'].value = list_item[i].str_content
            self.worksheet[f'E{row_number}'].value = list_item[i].link
            self.worksheet[f'F{row_number}'].value = list_item[i].image
            self.worksheet[f'G{row_number}'].value = list_item[i].thumb
            self.count += 1
        self.workbook.save(f'journey_in_life_{self.page_total}.xlsx')


if __name__ == '__main__':
    parse = JourneyParse()
    try:
        parse.parse_list_soup()
    except:
        # parse.close()
        print("Caught it!")
    finally:
        parse.close()
