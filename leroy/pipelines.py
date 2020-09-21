# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
import os
from urllib.parse import urlparse

class LeroyPipeline:

    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.leroy_merlin

    def process_item(self, item, spider):
        item['params'] = dict(zip(item['params_keys'], item['params_items']))
        del item['params_keys'], item['params_items']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
           for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        url = urlparse(info.spider.start_urls[0])
        return '/full/' + url.query[2:] + '/' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item
