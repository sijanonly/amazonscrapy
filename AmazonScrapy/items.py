# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    product_dimensions = scrapy.Field()
    shipping_weight = scrapy.Field()
    product_description = scrapy.Field()
    domestic_shipping = scrapy.Field()
    international_shipping = scrapy.Field()
    shipping_advisory = scrapy.Field()
    asin = scrapy.Field()
    item_model_number = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()

