# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def price_to_int(price):
    if price:
        return int(price.replace(" ", ""))
    return price


def clean_string(d):
    if d:
        return d.replace('\n', '').rstrip().lstrip()
    return d

class LeroyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_to_int), output_processor=TakeFirst())
    photo = scrapy.Field()
    params_keys = scrapy.Field(input_processor=MapCompose(clean_string))
    params_items = scrapy.Field(input_processor=MapCompose(clean_string))
    link = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
    params = scrapy.Field()
    pass
