import scrapy
import pandas as pd
from urllib import request
from bs4 import BeautifulSoup


class User(scrapy.Item):
    uid = scrapy.Field()
    uname = scrapy.Field()
    followers = scrapy.Field()
    illustrations = scrapy.Field()
    gender = scrapy.Field()
    birth = scrapy.Field()


class MainSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["www.pixiv.net"]

    df = pd.read_csv('../../../../data/tops.csv')
    uids = df['uid'].unique()
    start_urls = list(map(lambda x: 'https://www.pixiv.net/en/users/' + str(x), uids))

    def parse(self, response):
        html = request.urlopen(response.url)
        bs = BeautifulSoup(html.read(), 'html.parser')
