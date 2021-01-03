# -*- coding: utf-8 -*-
import scrapy
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
 
 
class SnapdealSpider(scrapy.Spider):
    name = 'Snapdeal'
 
    start_urls = ['https://www.snapdeal.com']
 
    def __init__(self, product_names=None, low_prices=None, high_prices=None, brand_names=None, product_filters=None, *args, **kwargs):
        super(SnapdealSpider, self).__init__(*args, **kwargs)
 
        self.page_sources = []
 
        for i in range(len(product_names)):
 
            # chrome_options = Options()
            # chrome_options.add_argument('--headless')
 
            chrome_path = which('chromedriver')
 
            driver = webdriver.Chrome(executable_path=chrome_path)
 
            driver.set_window_size(1920, 1080)
 
            driver.get('https://www.snapdeal.com')
 
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
                        (By.XPATH, "//input[@id='inputValEnter']"))
                )
                if element == True:
                    pass
            except:
                pass
            finally:
                input_box = driver.find_element_by_xpath("//input[@id='inputValEnter']")
                input_box.send_keys(product_names[i])
                input_box.send_keys(Keys.ENTER)
 
            if high_prices[i] == 0 or high_prices[i] == '0':
                raise CloseSpider('High price value cannot be zero!!!')
 
            if low_prices[i] != None:
                try:
                    low = int(low_prices[i])
                except ValueError:
                    raise CloseSpider('Low Price value must be an integer!')
 
            if high_prices[i] != None:
                try:
                    high = int(high_prices[i])
                except ValueError:
                    raise CloseSpider('High Price value must be an integer!')
 
            try:
                element1 = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='fromVal']"))
                )
                element2 = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='toVal']"))
                )
                if element1 == True or element2 == True:
                    pass
            except:
                pass
            finally:
                driver.find_element_by_xpath("//input[@name='fromVal']").clear()
                driver.find_element_by_xpath("//input[@name='toVal']").clear()

                if low_prices[i] != None:
                    self.low_pr = driver.find_element_by_xpath("//input[@name='fromVal']")
                    self.low_pr.send_keys(low)
 
                if high_prices[i] != None:
                    self.high_pr = driver.find_element_by_xpath("//input[@name='toVal']")
                    self.high_pr.send_keys(high)
 
                if high_prices[i] == None and low_prices[i] != None:
                    self.high_pr.send_keys(Keys.ENTER)
 
                elif low_prices[i] == None and high_prices[i] != None:
                    self.high_pr.send_keys(Keys.ENTER)
 
                elif low_prices[i] != None and high_prices[i] != None:
                    self.high_pr.send_keys(Keys.ENTER)
 
 
            if product_filters[i] != None:
                if product_filters[i].lower() == 'relevance':
                    pass
 
            try:
                elementA = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='sort-drop clearfix']"))
                )
                elementB = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='sort-drop clearfix']"))
                )
                if elementA or elementB == True:
                    pass
                if product_filters[i] != None and product_filters[i] != 'relevance':
                    if product_filters[i].lower() == 'low to high':
                        sort_btn = driver.find_element_by_xpath(
                            "//div[@class='sort-drop clearfix']")
                        sort_btn.click()
 
                        low_high = driver.find_element_by_xpath(
                            "//ul[@class='sort-value']/li[3]")
                        low_high.click()
 
                    if product_filters[i].lower() == 'high to low':
                        sort_btn = driver.find_element_by_xpath(
                            "//div[@class='sort-drop clearfix']")
                        sort_btn.click()
 
                        high_low = driver.find_element_by_xpath(
                            "//ul[@class='sort-value']/li[4]")
                        high_low.click()
 
                    if product_filters[i].lower() == 'popularity':
                        sort_btn = driver.find_element_by_xpath(
                            "//div[@class='sort-drop clearfix']")
                        sort_btn.click()
 
                        avg_rv = driver.find_element_by_xpath(
                            "//ul[@class='sort-value']/li[2]")
                        avg_rv.click()
 
                    if product_filters[i].lower() == 'fresh arrivals':
                        sort_btn = driver.find_element_by_xpath(
                            "//div[@class='sort-drop clearfix']")
                        sort_btn.click()
 
                        new_ar = driver.find_element_by_xpath(
                            "//ul[@class='sort-value']/li[6]")
                        new_ar.click()
 
            except Exception:
                pass

            # For plus button:-
            try:
                element1 = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "(//i[@class='sd-icon sd-icon-plus'])[1]"))
                )
                if element1 == True:
                    pass
            except:
                pass
            finally:
                pls_btn = driver.find_element_by_xpath("(//i[@class='sd-icon sd-icon-plus'])[1]")
                pls_btn.click()

            # For Brand Name:-
            if brand_names[i] != None:
                pg_src = driver.page_source
                resp = Selector(text=pg_src)
 
                pro_names = []
                pro_num = []
 
                try:
                    names_list = resp.xpath("(//input[@placeholder='Search by Brand']/following::label[contains(@for,'Brand')])/a/text()").getall()
 
                    for nm in names_list:
                        if nm != None:
                            nm = nm.strip()
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
                            (By.XPATH, f"(//input[@placeholder='Search by Brand']/following::label[contains(@for,'Brand')])[{n}]"))
                    )

                    check_box = driver.find_element_by_xpath(
                        f"(//input[@placeholder='Search by Brand']/following::label[contains(@for,'Brand')])[{n}]")
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
                "//div[contains(@class,'product-tuple-image')]/a/@href").getall()
 
            for link in links:
                yield scrapy.Request(url=link, callback=self.parse_pd, meta={'ID': id_count})
 
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
 
        Product_price = '₹ ' + self.remove_char(response.xpath(
            '//span[@itemprop="price"]/text()').get())
 
        pd_img_url = response.xpath(
            'normalize-space((//img[@class="cloudzoom"])[1]/@src)').get()
 
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
 
        Seller = 'Snapdeal'
 
        loader.add_value('Seller', Seller)
 
        yield loader.load_item()