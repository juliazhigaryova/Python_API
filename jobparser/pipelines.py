import re
from pymongo import MongoClient
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.vacancies_scrapy


    def process_item(self, item, spider):
        print()
        salary = item['salary']
        link = item['link']
        if (spider.name.startswith('hhru')):
            site = item['site'][0:13]
            result = self.validateSalaryHH(item['salary'])
        else:
            site = item['site'][0:23]
            result = self.validateSalarySJ(item['salary'])


        item['min_salary'] = result['min_salary']
        item['max_salary'] = result['max_salary']
        item['currency'] = result['currency']
        print(item)
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def validateSalaryHH(self,salary):
        result = {}
        if salary[0].strip().startswith('от'):
            if salary[2].strip().startswith('до'):
                result['min_salary'] = int(re.sub(r'[^0-9]+', r'', salary[1]))
                result['max_salary'] = int(re.sub(r'[^0-9]+', r'', salary[3]))
                result['currency'] = salary[5]
            else:
                result['min_salary'] = int(re.sub(r'[^0-9]+', r'', salary[1]))
                result['max_salary'] = 0
                result['currency'] = salary[3]
        elif salary[0].strip().startswith('до'):
            result['max_salary'] = int(re.sub(r'[^0-9]+', r'', salary[1]))
            result['min_salary'] = 0
            result['currency'] = salary[3]
        else:
            result['max_salary'] = 0
            result['min_salary'] = 0
            result['currency'] = 0
        return result

    def validateSalarySJ(self,salary):
        result = {}
        if salary[0].strip().startswith('от'):
            if salary[2].strip().startswith('до'):
                result['min_salary'] = int(re.sub(r'[^0-9]+', r'', salary[1]))
                result['max_salary'] = int(re.sub(r'[^0-9]+', r'', salary[3]))
                result['currency'] = salary[5]
            else:
                result['min_salary'] = int(re.sub(r'[^0-9]+', r'', salary[2]))
                result['max_salary'] = 0
                result['currency'] = salary[2][-4:]
        elif salary[0].strip().startswith('до'):
            result['max_salary'] = int(re.sub(r'[^0-9]+', r'', salary[1]))
            result['min_salary'] = 0
            result['currency'] = salary[3]
        elif len(salary) == 3:
                result['min_salary'] = salary[0]
                result['max_salary'] = 0
                result['currency'] = salary[2]
        elif len(salary) > 3:
            result['min_salary'] = salary[0].strip()
            result['max_salary'] = salary[2].strip()
            result['currency'] = salary[6]
        else:
            result['max_salary'] = 0
            result['min_salary'] = 0
            result['currency'] = 0
        return result

