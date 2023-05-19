import scrapy
from urllib import request
from bs4 import BeautifulSoup


class Link(scrapy.Item):
    link = scrapy.Field()


class MainSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["www.pixiv.net"]
    start_urls = ['https://www.pixiv.net/ranking.php?mode=daily_ai']

    def parse(self, response):
        header = {"User-Agent": 'Mozilla/5.0', 'Content-type': "text/html"}
        webpage = request.urlopen(request.Request(response.url, headers=header))
        # webpage = request.urlopen(response.url)
        bs = BeautifulSoup(webpage.read(), 'html.parser')
        work_url = 'https://www.pixiv.net/artworks/'
        rank_tbl = bs.find('div', {'class': 'ranking-items adjust'})

        for sec in rank_tbl.find_all('section'):
            page_url = Link()
            try:
                page_url['link'] = work_url + sec['data-id']
            except Exception as e:
                page_url['link'] = None
                print(e)
            yield page_url
