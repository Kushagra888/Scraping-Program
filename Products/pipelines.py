# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter

class SQLlitePipeline(object):
    def open_spider(self, spider):
        self.db = mysql.connector.connect(host='localhost', user='Kushagra', passwd='kushagrasql123pass', database='scraping_project')
        self.cursr = self.db.cursor()
        try:
            self.cursr.execute('''
                CREATE TABLE Web_data (
                    ID TEXT,
                    Product_name TEXT,
                    Product_price TEXT,
                    Product_link TEXT,
                    Website_name TEXT,
                    Seller TEXT,
                    Machine_name TEXT,
                    Time TEXT
                )
            ''')
            self.db.commit()
        
        except mysql.connector.errors.ProgrammingError:
            pass

    def close_spider(self, spider):
        self.cursr.close()
        self.db.close()

    def process_item(self, item, spider):
        self.cursr.execute('''
            INSERT INTO Web_data (ID, Product_name, Product_price, Product_link, Website_name, Seller, Machine_name, Time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (
            item.get('ID'),
            item.get('Product_name'),
            item.get('Product_price'),
            item.get('Product_link'),
            item.get('Website_name'),
            item.get('Seller'),
            item.get('Machine_name'),
            item.get('Time')
        ))
        self.db.commit()
        return item


class IndustrybuyingImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'pname': item.get('Product_name')}) for x in item.get(self.images_urls_field, [])]


    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block
        filename = request.meta['pname'].strip(':').strip('/').strip('\\')
        return 'Industrybuying_Images/%s.jpg' % (filename)
        