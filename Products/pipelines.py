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
        self.db = mysql.connector.connect(host='localhost', user='Kushagra', passwd='kushagrasql123pass', database='amazon')
        self.cursr = self.db.cursor()
        try:
            self.cursr.execute('''
                CREATE TABLE Amazon_data (
                    ID TEXT,
                    Product_Name TEXT,
                    Product_Price TEXT,
                    Product_Link TEXT,
                    Website_Name TEXT,
                    Seller TEXT,
                    Machine_Name TEXT,
                    UTC_Time TEXT
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
            INSERT INTO Amazon_data (ID, Product_Name, Product_Price, Product_Link, Website_Name, Seller, Machine_Name, UTC_Time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (
            item.get('ID'),
            item.get('pd_name'),
            item.get('pd_price'),
            item.get('pd_link'),
            item.get('website_name'),
            'Amazon',
            item.get('machine_name'),
            item.get('time')
        ))
        self.db.commit()
        return item


class AmazonImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'pname': item.get('p_name')}) for x in item.get(self.images_urls_field, [])]


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
        filename = request.meta['pname'].replace(':','')
        return 'Amazon_Images/%s.jpg' % (filename)
        