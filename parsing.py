from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
from datetime import datetime

now = datetime.now()
now_data = now.strftime(" %Y-%m-%d %H:%M").split(' ')[0]
news = []
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
response = requests.get('https://m.yandex.ru/news/', headers=header)
dom = html.fromstring(response.text)
blocks = dom.xpath("//td[contains(@class,'stories-set__item')]")

for block in blocks:
    item = {}
    name = block.xpath(".//a[contains(@class,'link_theme_black')]/text()")
    link = block.xpath(".//a[contains(@class,'link_theme_black')]/@href")
    source = block.xpath(".//div[contains(@class,'story__date')]/text()")

    item['name'] = ''.join(name)
    item['link'] = 'https://m.yandex.ru' + ''.join(link)
    item['source'] = ''.join(source).split(' ')[0]
    item['data'] = ''.join(source).split(' ')[-1] + now_data
    news.append(item)
response = requests.get('https://lenta.ru/', headers=header)
dom = html.fromstring(response.text)

blocks = dom.xpath("//section[contains(@class,'row b-top7-for-main js-top-seven')]/*/div[contains(@class,'item')]")

for block in blocks:
    item = {}
    name = block.xpath(".//a/text()")
    link = block.xpath(".//a/@href")
    time = block.xpath(".//time[contains(@class,'g-time')]/text()")

    item['name'] = ''.join(name).replace('\xa0', ' ')
    item['link'] = 'https://lenta.ru' + ''.join(link)
    item['source'] = 'lenta.ru'
    item['data'] = ''.join(time) + now_data
    news.append(item)
db_name = 'news_db'
client = MongoClient('mongodb://127.0.0.1:27017')
db = client[db_name]
db.news_db.insert_many(news)