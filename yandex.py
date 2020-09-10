from pprint import pprint
from lxml import html
import requests
from datetime import datetime
import re

# выбираем новости из раздела "Интересное"
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
main_link = 'https://yandex.ru/news'
response = requests.get(main_link,headers=header)

dom = html.fromstring(response.text)

items = dom.xpath("//div[@class='mg-grid__col mg-grid__col_xs_12 mg-grid__col_sm_9']/div[5]//article")
news = []

for item in items:
    headline = {}
    name = item.xpath(".//h2[@class='news-card__title']/text()")
    link = item.xpath(".//span[@class='mg-card-source__source']/a/@href")
    date = item.xpath(".//span[@class='mg-card-source__time']/text()")
    source = item.xpath(".//a[@class='news-card__link']/@href")
    response = requests.get(source[0], headers=header)
    dom = html.fromstring(response.text)
    article_source = dom.xpath("//article[@class='mg-story news-story mg-grid__item']//a[@class='mg-story__meta']/@href")

    headline['name'] = re.sub(r"\\xa0", " ", str(name))
    headline['link'] = str(link)
    headline['date'] = str(date)
    headline['source'] = article_source
    news.append(headline)

pprint(news)

