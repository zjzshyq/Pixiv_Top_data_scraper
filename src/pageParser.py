# coding=utf-8
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from dao import DAO
import json
import re
import time

name_lst_outside = ['pid', 'date', 'rank', 'img']  # str
name_lst_info = ['title', 'uid', 'uname', 'aiType',
                 'tags', 'desc', 'create_time', 'update_time']  # all str
name_lst_illust = ['views', 'comments', 'likes', 'bookmarks']  # all int
name_lst = name_lst_outside + name_lst_info + name_lst_illust


class Page(object):
    def __init__(self, page_url, date, rank, img_url):
        self.url = page_url
        self.date = date
        self.rank = rank
        self.page_id = page_url.split('/')[-1]
        self.dict_page = {'pid': self.page_id, 'date': date, 'rank': rank, 'img': img_url}

        self.dao = DAO()
        # time.sleep(1)

    def get_soup(self):
        headers = {"User-Agent": "Mozilla/5.0", 'Content-type': "text/html"}
        request_site = Request(self.url, headers=headers)
        webpage = urlopen(request_site)
        return BeautifulSoup(webpage.read(), 'html.parser')

    def parse(self, bs):
        try:
            js = json.loads(bs.find_all('meta')[-1]['content'])
        except Exception as e:
            print(e)
            return

        try:
            illust = js['illust'][self.page_id]
        except Exception as e:
            for n in name_lst_info:
                self.dict_page[n] = ''
            illust = None
            print(e)

        try:
            info = illust['userIllusts'][self.page_id]
        except Exception as e:
            for n in name_lst_illust:
                self.dict_page[n] = -1
            info = None
            print(e)

        try:
            self.dict_page['title'] = info['title']
        except Exception as e:
            self.dict_page['title'] = ''
            print(e)

        try:
            self.dict_page['uid'] = str(info['userId'])
        except Exception as e:
            self.dict_page['uid'] = ''
            print(e)

        try:
            self.dict_page['uname'] = info['userName']
        except Exception as e:
            self.dict_page['uname'] = ''
            print(e)

        try:
            self.dict_page['create_time'] = info['createDate']
        except Exception as e:
            self.dict_page['create_time'] = ''
            print(e)

        try:
            self.dict_page['update_time'] = info['updateDate']
        except Exception as e:
            self.dict_page['update_time'] = ''
            print(e)

        try:
            self.dict_page['aiType'] = str(info['aiType'])  # 1非ai，2ai
        except Exception as e:
            self.dict_page['aiType'] = ''
            print(e)

        try:
            self.dict_page['tags'] = '/'.join(info['tags']) if info['tags'] is not None else ''
        except Exception as e:
            self.dict_page['tags'] = ''
            print(e)

        try:
            pattern = re.compile(r'<.+?>')
            desc = info['description']
            for s in re.findall(pattern, desc):
                desc = desc.replace(s, '')
            self.dict_page['desc'] = desc
        except Exception as e:
            self.dict_page['desc'] = ''
            print(e)

        try:
            self.dict_page['views'] = int(illust['viewCount'])
        except Exception as e:
            self.dict_page['views'] = -1
            print(e)

        try:
            self.dict_page['comments'] = int(illust['commentCount'])
        except Exception as e:
            self.dict_page['views'] = -1
            print(e)

        try:
            self.dict_page['likes'] = int(illust['likeCount'])
        except Exception as e:
            self.dict_page['likes'] = -1
            print(e)

        try:
            self.dict_page['bookmarks'] = int(illust['bookmarkCount'])
        except Exception as e:
            self.dict_page['bookmarks'] = -1
            print(e)

    def results(self, db=False):
        print('Date:', self.dict_page['date'],
              '\nRank:', self.dict_page['rank'],
              '\nURL:', self.url)
        for k in self.dict_page.keys():
            print(k+':', self.dict_page[k])
        if self.dao.redis_server_flag:
            if db:
                # self.dao.info2rd(self.page_id, self.dict_page)
                self.dao.img_queue_push(self.page_id,
                                        self.dict_page['rank'],
                                        self.dict_page['date'],
                                        self.dict_page['img'])

        else:
            print('can\'t push data in redis with disconnection')
        if self.dao.sqlite_server_flag:
            if db:
                self.dao.insert2sql(self.dict_page)
            self.dao.sqlite.close()
        else:
            print('can\'t insert data in sqlite3')


if __name__ == '__main__':
    url = 'https://www.pixiv.net/artworks/102345178'
    page = Page(url, '2022-10-31', 1, '')
    page.parse(page.get_soup())
    page.results(False)
