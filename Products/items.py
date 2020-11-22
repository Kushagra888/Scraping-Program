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
    p_name = scrapy.Field(
        output_processor = TakeFirst()
    )

    pd_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    pd_price = scrapy.Field(
        output_processor=TakeFirst()
    )
    machine_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    time = scrapy.Field(
        output_processor=TakeFirst()
    )

    pd_link = scrapy.Field(
        output_processor=TakeFirst()
    )

    website_name = scrapy.Field(
        output_processor=TakeFirst()
    )
