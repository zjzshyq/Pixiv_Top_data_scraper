import scrapy
from urllib import request
from bs4 import BeautifulSoup
import datetime


class Link(scrapy.Item):
    link = scrapy.Field()


class MainSpider(scrapy.Spider):
    name = "main"
    end_date = '20230603'
    is_ai = True
    adjust_end_date = True  # Boolean parameter

    allowed_domains = ["www.pixiv.net"]

    end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
    current_date = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    start_urls = []

    # Adjust the end_date based on the value of adjust_end_date
    if adjust_end_date:
        end_date = current_date - (2 * delta)

    while current_date >= end_date:
        current_date -= delta
# class MainSpider(scrapy.Spider):
#     name = "main"
#     end_date = '20230604'
#     is_ai = True
#     allowed_domains = ["www.pixiv.net"]
#
#     end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
#     current_date = datetime.datetime.now()
#     delta = datetime.timedelta(days=1)
#     start_urls = []
#     while current_date >= end_date:
#         current_date -= delta

        url = 'https://www.pixiv.net/ranking.php?mode=daily{ai_flag}&date={date}' \
            .format(ai_flag='_ai' if is_ai else '', date=current_date.strftime('%Y%m%d'))
        start_urls.append(url)

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
