from pprint import pprint
from lxml import html
import requests
from datetime import datetime
import re

# выбираем новости на главной странице в рубрике "Общество"
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
main_link = 'https://news.mail.ru/'
response = requests.get(main_link,headers=header)

dom = html.fromstring(response.text)

items = dom.xpath("//div[@class='cols__column cols__column_small_percent-50 cols__column_medium_percent-50 cols__column_large_percent-50 link-hdr margin_top_30'][1]//a[not(contains(@class,'hdr__text'))]")
news = []

for item in items:
    headline = {}
    name = item.xpath("./span/text()")
    link = item.xpath("./@href")
    response = requests.get(link[0], headers=header)
    dom = html.fromstring(response.text)
    article_date = dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
    date = article_date
    source = main_link

    headline['name'] = re.sub(r"\\xa0", " ", str(name))
    headline['link'] = str(link)
    headline['date'] = str(date)
    headline['source'] = source
    news.append(headline)

pprint(news)

