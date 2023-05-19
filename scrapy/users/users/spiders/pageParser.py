from urllib import request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import scrapy
import json
import re
import ftfy
import datetime
import pytz


name_lst_outside = ['pid', 'date', 'rank', 'img', 'crawl_time']  # str
name_lst_info = ['title', 'uid', 'uname', 'aiType', 'tags',
                 'desc', 'create_time', 'update_time']  # all str
name_lst_illust = ['views', 'comments', 'likes', 'bookmarks']  # all int
name_lst = name_lst_outside + name_lst_info + name_lst_illust


class Artwork(scrapy.Item):
    for n in name_lst:
        locals()[n] = scrapy.Field()


class PageparserSpider(scrapy.Spider):
    name = "pageParser"
    user_agent = 'Mozilla/5.0'
    allowed_domains = ["www.pixiv.net"]
    try:
        with open("links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except Exception as e:
        start_urls = []
        print(e)

    def parse(self, response):
        header = {"User-Agent": 'Mozilla/5.0', 'Content-type': "text/html"}
        url = response.url
        webpage = request.urlopen(request.Request(url, headers=header))
        bs = BeautifulSoup(webpage.read(), 'html.parser')

        dict_page = Artwork()
        page_id = url.split('/')[-1]
        dict_page['pid'] = page_id

        now = datetime.datetime.now()
        tz = pytz.timezone('Asia/Tokyo')  # 转换为东京时区的时间
        now_tz = tz.localize(now)
        crawl_time_str = now_tz.strftime('%Y-%m-%dT%H:%M:%S%z')
        dict_page['crawl_time'] = crawl_time_str

        current_date = datetime.now()
        previous_date = current_date - timedelta(days=1)
        previous_date_str = previous_date.strftime('%Y%m%d')
        dict_page['date'] = previous_date_str

        try:
            js = json.loads(bs.find_all('meta')[-1]['content'])
        except Exception as e:
            print(e)
            return

        try:
            illust = js['illust'][page_id]
        except Exception as e:
            for n in name_lst_info:
                dict_page[n] = ''
            illust = None
            print(e)

        try:
            info = illust['userIllusts'][page_id]
        except Exception as e:
            for n in name_lst_illust:
                dict_page[n] = -1
            info = None
            print(e)

        try:
            dict_page['title'] = ftfy.fix_text(info['title'])
        except Exception as e:
            dict_page['title'] = ''
            print(e)

        try:
            dict_page['uid'] = str(info['userId'])
        except Exception as e:
            dict_page['uid'] = ''
            print(e)

        try:
            dict_page['uname'] = ftfy.fix_text(info['userName'])
        except Exception as e:
            dict_page['uname'] = ''
            print(e)

        try:
            dict_page['create_time'] = info['createDate']
        except Exception as e:
            dict_page['create_time'] = ''
            print(e)

        try:
            dict_page['update_time'] = info['updateDate']
        except Exception as e:
            dict_page['update_time'] = ''
            print(e)

        try:
            dict_page['aiType'] = str(info['aiType'])  # 0被认证的原创作品，1非ai，2ai
        except Exception as e:
            dict_page['aiType'] = ''
            print(e)

        try:
            dict_page['tags'] = '/'.join(info['tags']) if info['tags'] is not None else ''
            dict_page['tags'] = ftfy.fix_text(dict_page['tags'])
        except Exception as e:
            dict_page['tags'] = ''
            print(e)

        try:
            pattern = re.compile(r'<.+?>')
            desc = info['description']
            for s in re.findall(pattern, desc):
                desc = desc.replace(s, '')
            dict_page['desc'] = ftfy.fix_text(desc)
        except Exception as e:
            dict_page['desc'] = ''
            print(e)

        try:
            dict_page['views'] = int(illust['viewCount'])
        except Exception as e:
            dict_page['views'] = -1
            print(e)

        try:
            dict_page['comments'] = int(illust['commentCount'])
        except Exception as e:
            dict_page['views'] = -1
            print(e)

        try:
            dict_page['likes'] = int(illust['likeCount'])
        except Exception as e:
            dict_page['likes'] = -1
            print(e)

        try:
            dict_page['bookmarks'] = int(illust['bookmarkCount'])
        except Exception as e:
            dict_page['bookmarks'] = -1
            print(e)

        yield dict_page
