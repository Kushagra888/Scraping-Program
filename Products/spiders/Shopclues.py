# -*- coding: utf-8 -*-
import scrapy
import socket
import re
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
 
 
class ShopcluesSpider(scrapy.Spider):
    name = 'Shopclues'
 
    start_urls = ['https://www.shopclues.com']
 
    def __init__(self, product_names=None, low_prices=None, high_prices=None, brand_names=None, conditions=None, product_filters=None, *args, **kwargs):
        super(ShopcluesSpider, self).__init__(*args, **kwargs)
 
        self.page_sources = []
 
        for i in range(len(product_names)):
 
            # chrome_options = Options()
            # chrome_options.add_argument('--headless')
 
            chrome_path = which('chromedriver')
 
            driver = webdriver.Chrome(executable_path=chrome_path)
 
            driver.set_window_size(1920, 1080)
 
            driver.get('https://www.shopclues.com')
 
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
                        (By.XPATH, "//span[@id='search']/input[@type='text']"))
                )
                if element == True:
                    pass
            except:
                pass
            finally:
                input_box = driver.find_element_by_xpath("//span[@id='search']/input[@type='text']")
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
                        (By.XPATH, "//ul[@id='sortBy']/li/a"))
                )

                if elementA == True:
                    pass
                if product_filters[i] != None and product_filters[i] != 'relevance':
                    pflters = driver.find_elements_by_xpath("//ul[@id='sortBy']/li/a")

                    if product_filters[i].lower() == 'low to high':
                        pflters[2].click()
 
                    if product_filters[i].lower() == 'high to low':
                        pflters[1].click()
 
                    if product_filters[i].lower() == 'popularity':
                        pflters[3].click()
 
                    if product_filters[i].lower() == 'newest arrivals':
                        pflters[5].click()
 
            except Exception:
                pass
 
            # For Brand Name:-
            if brand_names[i] != None:
                pg_src = driver.page_source
                resp = Selector(text=pg_src)
 
                pro_names = []
                pro_num = []
 
                try:
                    names_list = resp.xpath("//div[@class='heading'][contains(text(),'Brand')]/following::ul[contains(@id,'show_brand')]/li/label/text()").getall()
 
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
                            (By.XPATH, f"(//div[@class='heading'][contains(text(),'Brand')]/following::ul[contains(@id,'show_brand')]/li/label)[{n}]"))
                    )

                    check_box = driver.find_element_by_xpath(
                        f"(//div[@class='heading'][contains(text(),'Brand')]/following::ul[contains(@id,'show_brand')]/li/label)[{n}]")
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
                "//div[@class='row']/div/a/@href").getall()
 
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
            'normalize-space(//h1[@itemprop="name"]/text())').get()
 
        Product_price = self.remove_char(response.xpath(
            '//span[@class="f_price"]/text()').get())
 
        pd_img_url = response.xpath(
            'normalize-space(//img[@class="img"]/@src)').get()
 
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
 
        Seller = 'Shopclues'
 
        loader.add_value('Seller', Seller)
 
        yield loader.load_item()
        