from pprint import pprint
from lxml import html
import requests
from datetime import datetime
import re

# выбираем новости на главной странице

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
main_link = 'https://lenta.ru/'
response = requests.get(main_link,headers=header)

dom = html.fromstring(response.text)

items = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']/div[@class='span4']/div[not(contains(@class,'button-more-news'))]")
news = []

for item in items:
    headline = {}
    name = item.xpath(".//a/time/../text()")
    link = item.xpath(".//a/time/../@href")
    date = item.xpath(".//a/time/@datetime")
    source = main_link

    headline['name'] = re.sub(r"\\xa0", " ", str(name))
    headline['link'] = str(link)
    headline['date'] = str(date)
    headline['source'] = source
    news.append(headline)

pprint(news)

