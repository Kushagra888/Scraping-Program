# -*- coding: utf-8 -*-
import scrapy
import re
import socket
import mysql.connector
from shutil import which
from datetime import datetime
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from Products.items import ProductsItem
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class IndustrybuyingSpider(scrapy.Spider):
    name = 'Industrybuying'

    start_urls = ['https://www.industrybuying.com']

    def __init__(self, product_names=None, low_prices=None, high_prices=None, brand_names=None, conditions=None, product_filters=None, *args, **kwargs):
        super(IndustrybuyingSpider, self).__init__(*args, **kwargs)

        self.page_sources = []

        for i in range(len(product_names)):

            # chrome_options = Options()
            # chrome_options.add_argument('--headless')

            chrome_path = which('chromedriver')

            driver = webdriver.Chrome(executable_path=chrome_path)

            driver.set_window_size(1920, 1080)

            driver.get('https://www.industrybuying.com')

            if product_names[i] == '' or product_names[i] == None:
                raise CloseSpider('Please enter a product name.')

            if product_filters[i] == '':
                raise CloseSpider('Please enter a filter name.')

            if low_prices[i] == '':
                raise CloseSpider('Low Price cannot be a empty value.')

            if high_prices[i] == '':
                raise CloseSpider('High Price cannot be a empty value.')

            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.ID, "search_input"))
                )
                if element == True:
                    pass
            except:
                pass
            finally:
                input_box = driver.find_element_by_id('search_input')
                input_box.send_keys(product_names[i])
                input_box.send_keys(Keys.ENTER)

            # if high_prices[i] == 0 or high_prices[i] == '0':
            #     raise CloseSpider('High price value cannot be zero!!!')

            # if low_prices[i] != None:
            #     try:
            #         low = int(low_prices[i])
            #     except ValueError:
            #         raise CloseSpider('Low Price value must be an integer!')

            # if high_prices[i] != None:
            #     try:
            #         high = int(high_prices[i])
            #     except ValueError:
            #         raise CloseSpider('High Price value must be an integer!')

            # try:
            #     element1 = WebDriverWait(driver, 5).until(
            #         EC.presence_of_element_located((By.ID, "low-price"))
            #     )
            #     element2 = WebDriverWait(driver, 5).until(
            #         EC.presence_of_element_located((By.ID, "high-price"))
            #     )
            #     if element1 == True or element2 == True:
            #         pass
            # except:
            #     pass
            # finally:
            #     if low_prices[i] != None:
            #         self.low_pr = driver.find_element_by_id('low-price')
            #         self.low_pr.send_keys(low)

            #     if high_prices[i] != None:
            #         self.high_pr = driver.find_element_by_id('high-price')
            #         self.high_pr.send_keys(high)

            #     if high_prices[i] == None and low_prices[i] != None:
            #         self.low_pr.send_keys(Keys.ENTER)

            #     elif low_prices[i] == None and high_prices[i] != None:
            #         self.high_pr.send_keys(Keys.ENTER)

            #     elif low_prices[i] != None and high_prices[i] != None:
            #         self.high_pr.send_keys(Keys.ENTER)

            if product_filters[i] != None:
                if product_filters[i].lower() == 'relevance':
                    pass

            try:
                elementA = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[@class='btn btn-default dropdown-toggle']"))
                )
                elementB = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@class='btn btn-default dropdown-toggle']"))
                )
                if elementA or elementB == True:
                    pass
                if product_filters[i] != None and product_filters[i] != 'relevance':
                    if product_filters[i].lower() == 'low to high':
                        sort_btn = driver.find_element_by_xpath(
                            "//button[@class='btn btn-default dropdown-toggle']")
                        sort_btn.click()

                        low_high = driver.find_element_by_xpath(
                            "(//a[@class='AH_Sortby'])[3]")
                        low_high.click()

                    if product_filters[i].lower() == 'high to low':
                        sort_btn = driver.find_element_by_xpath(
                            "//button[@class='btn btn-default dropdown-toggle']")
                        sort_btn.click()

                        high_low = driver.find_element_by_xpath(
                            "(//a[@class='AH_Sortby'])[4]")
                        high_low.click()

                    if product_filters[i].lower() == 'new arrivals':
                        sort_btn = driver.find_element_by_xpath(
                            "//button[@class='btn btn-default dropdown-toggle']")
                        sort_btn.click()

                        new_ar = driver.find_element_by_xpath(
                            "(//a[@class='AH_Sortby'])[7]")
                        new_ar.click()

                    if product_filters[i].lower() == 'popularity':
                        sort_btn = driver.find_element_by_xpath(
                            "//button[@class='btn btn-default dropdown-toggle']")
                        sort_btn.click()

                        popu = driver.find_element_by_xpath(
                            "(//a[@class='AH_Sortby'])[2]")
                        popu.click()

            except Exception:
                pass

            # For Brand Name:-
            if brand_names[i] != None:
                pg_src = driver.page_source
                resp = Selector(text=pg_src)

                pro_names = []
                pro_num = []

                try:
                    names_list = resp.xpath(
                        "(//h3[contains(text(),'Brands')]/following::ul[@id='filter_name_brand_id']/li/label)/span/text()").getall()

                    for nm in names_list:
                        if nm != None:
                            nm = nm.strip()
                            result = re.search(r'(\d+)', nm)
                            rem = nm[result.start()-2:result.end()+1]
                            nm = nm.strip(rem)
                        pro_names.append(nm)

                    for s in range(1, len(pro_names)+1):
                        pro_num.append(s)

                    pro_dict = dict(zip(pro_names, pro_num))

                    n = pro_dict.get(brand_names[i])

                except Exception:
                    raise CloseSpider(
                        'Please enter a valid brand name! or do not pass any brand name if you do not want any brand name.')

                try:
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f"(//h3[contains(text(),'Brands')]/following::ul[@id='filter_name_brand_id']/li/label)[{n}]"))
                    )

                    check_box = driver.find_element_by_xpath(
                        f"(//h3[contains(text(),'Brands')]/following::ul[@id='filter_name_brand_id']/li/label)[{n}]")
                    check_box.click()

                except:
                    pass

            self.page_sources.append(driver.page_source)

            driver.close()

    def parse(self, response):
        id_count = 1
        for html in self.page_sources:
            resp = Selector(text=html)

            links = resp.xpath(
                "//a[@class='prFeatureName']/@href").getall()

            for link in links:
                url = response.urljoin(link)
                yield scrapy.Request(url=url, callback=self.parse_pd, meta={'ID': id_count})

            id_count += 1

    def remove_char(self, val):
        if val != None:
            return val.strip('\xa0')
        elif val == None:
            return val

    def parse_pd(self, response):

        ID = response.meta.get('ID')

        Product_name = response.xpath(
            "normalize-space(//span[contains(@class,'productTitle')]/h1/text())").get()

        Product_price = '₹' + self.remove_char(response.xpath(
            "//span[@class='AH_PricePerPiece']/text()").get())

        pd_img_url = response.urljoin(response.xpath("normalize-space(//img[@class='mainImg zoom_img']/@src)").get())

        Product_link = response.url

        loader = ItemLoader(item=ProductsItem(), response=response)
        loader.add_value('image_urls', pd_img_url)
        loader.add_value('ID', ID)
        loader.add_value('Product_name', Product_name)

        if Product_price is None:
            Product_price = '₹0'

        loader.add_value('Product_price', Product_price)

        utc_now = datetime.utcnow()
        Time = utc_now.strftime("%H:%M:%S %b-%d-%Y")

        loader.add_value('Machine_name', socket.gethostname())
        loader.add_value('Time', Time)
        loader.add_value('Product_link', Product_link)

        Website_name = self.start_urls[0]

        loader.add_value('Website_name', Website_name)

        Seller = 'Industrybuying'

        loader.add_value('Seller', Seller)

        yield loader.load_item()
