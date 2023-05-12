import scrapy


class MainSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["www.pixiv.net"]
    start_urls = ["http://www.pixiv.net/"]

    def parse(self, response):
        pass
