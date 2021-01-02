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

 
class FlipkartSpider(scrapy.Spider):
    name = 'Flipkart'

    start_urls = ['https://www.flipkart.com']
 
    def __init__(self, product_names=None, low_prices=None, high_prices=None, brand_names=None, product_filters=None, *args, **kwargs):
        super(FlipkartSpider, self).__init__(*args, **kwargs)
 
        self.page_sources = []
 
        for i in range(len(product_names)):
 
            # chrome_options = Options()
            # chrome_options.add_argument('--headless')
 
            chrome_path = which('chromedriver')
 
            driver = webdriver.Chrome(executable_path=chrome_path)
 
            driver.set_window_size(1920, 1080)
 
            driver.get('https://www.flipkart.com')
 
            if product_names[i] == '' or product_names[i] == None:
                raise CloseSpider('Please enter a product name.')
 
            if product_filters[i] == '':
                raise CloseSpider('Please enter a filter name.')
 
            if low_prices[i] == '':
                raise CloseSpider('Low Price cannot be a empty value.')
 
            if high_prices[i] == '':
                raise CloseSpider('High Price cannot be a empty value.')

            try:
                elementd = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[@class='_2KpZ6l _2doB4z']"))
                )
                if elementd == True:
                    pass
            except:
                pass
            finally:
                close_btn = driver.find_element_by_xpath("//button[@class='_2KpZ6l _2doB4z']")
                close_btn.click()

            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//input[@title='Search for products, brands and more']"))
                )
                if element == True:
                    pass
            except:
                pass
            finally:
                input_box = driver.find_element_by_xpath("//input[@title='Search for products, brands and more']")
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
                        (By.XPATH, "//div[@class='_5THWM1']/div"))
                )
                if elementA == True:
                    pass

                if product_filters[i] != None and product_filters[i] != 'relevance':
                    pflters = driver.find_elements_by_xpath("//div[@class='_5THWM1']/div")

                    if product_filters[i].lower() == 'popularity':
                        pflters[1].click()

                    if product_filters[i].lower() == 'low to high':
                        pflters[2].click()
 
                    if product_filters[i].lower() == 'high to low':
                        pflters[3].click()
 
                    if product_filters[i].lower() == 'newest first':
                        pflters[4].click()
 
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
                        "//div[contains(text(),'Brand')]/following::div[@class='_3879cV']/text()").getall()
 
                    for nm in names_list:
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
                            (By.XPATH, f"(//div[contains(text(),'Brand')]/following::div[@class='_3879cV'])[{n}]"))
                    )

                    check_box = driver.find_element_by_xpath(
                        f"(//div[contains(text(),'Brand')]/following::div[@class='_3879cV'])[{n}]")
                    check_box.click()
                except:
                    pass
 
            self.page_sources.append(driver.page_source)
 
            driver.close()
 
    def parse(self, response):
        id_count = 1
        for html in self.page_sources:
            resp = Selector(text=html)
 
            links = resp.xpath("//div[@class='_13oc-S']/div/div/a[1]/@href").getall()
 
            for link in links:
                url = response.urljoin(link)
                yield scrapy.Request(url=url, callback=self.parse_pd, meta={'ID': id_count})
 
            id_count += 1
 
    def remove_char(self, val):
        if val != None:
            return val.strip('\xa0')
        elif val == None:
            return val

    def corrector(self, nm):
        if len(nm) > 1:
            return ''.join(nm)
        else:
            return nm[0]
 
    def parse_pd(self, response):
 
        ID = response.meta.get('ID')
 
        templ = self.corrector(response.xpath("//span[@class='B_NuCI']/text()").getall())

        Product_name = self.remove_char(templ)
 
        Product_price = self.remove_char(response.xpath(
            '//div[@class="_30jeq3 _16Jk6d"]/text()').get())
 
        value_url = response.xpath('normalize-space((//div[@class="q6DClP"])[1]/@style)').get()

        pd_img_url = value_url[21:-1].replace('128','240')
 
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
 
        Seller = 'Flipkart'
 
        loader.add_value('Seller', Seller)
 
        yield loader.load_item()