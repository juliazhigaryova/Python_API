# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    follower_id = scrapy.Field()
    user_id = scrapy.Field()
    photo = scrapy.Field()
    name = scrapy.Field()
    _id = scrapy.Field()
    following_id = scrapy.Field()
    user_name = scrapy.Field()
    is_follower = scrapy.Field()
    pass
