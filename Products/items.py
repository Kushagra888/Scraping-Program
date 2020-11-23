# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

class ProductsItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()

    ID = scrapy.Field(
        output_processor=TakeFirst()
    )

    Product_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    Product_price = scrapy.Field(
        output_processor=TakeFirst()
    )
    Machine_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    Time = scrapy.Field(
        output_processor=TakeFirst()
    )

    Product_link = scrapy.Field(
        output_processor=TakeFirst()
    )

    Website_name = scrapy.Field(
        output_processor=TakeFirst()
    )

    Seller = scrapy.Field(
        output_processor=TakeFirst()
    )