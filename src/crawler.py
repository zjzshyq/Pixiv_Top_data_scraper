# coding=utf-8
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from pageParser import Page, name_lst
from dao import DAO
import datetime
import re
import pandas as pd
import warnings


# AI生成从20221031开始
class Crawler(object):
    def __init__(self, tops: int, is_ai: bool):
        self.is_ai = is_ai
        self.tops = tops
        self.end_date = datetime.date(2022, 10, 31)
        self.begin_date = ''

    def set_date(self, begin_date='', end_date=''):
        if begin_date != '':
            datetime_obj = datetime.datetime.strptime(begin_date, '%Y%m%d')
            self.begin_date = datetime_obj.date()
        if end_date != '':
            datetime_obj = datetime.datetime.strptime(end_date, '%Y%m%d')
            self.end_date = datetime_obj.date()

    def daily_tops(self, date):
        if date == '' or date is None:
            if not self.is_ai:
                url = 'https://www.pixiv.net/ranking.php'
            else:
                url = 'https://www.pixiv.net/ranking.php?mode=daily_ai'
        else:
            url = 'https://www.pixiv.net/ranking.php?mode=daily{ai_flag}&date={date}'\
                .format(ai_flag='_ai' if self.is_ai else '', date=date)

        header = {"User-Agent": "Mozilla/5.0", 'Content-type': "text/html"}
        request_site = Request(url, headers=header)
        webpage = urlopen(request_site)
        bs = BeautifulSoup(webpage.read(), 'html.parser')

        work_url = 'https://www.pixiv.net/artworks/'
        rank_tbl = bs.find('div', {'class': 'ranking-items adjust'})

        current_date = bs.find('li', {'class': 'before'}) \
            .find_next_sibling('li') \
            .find('a', {'class': 'current', 'href': re.compile('date=')}) \
            .text

        print('\n----------------------------------------------------------------')
        print('current_date:', current_date, '\n')
        if date == '' or date is None:
            pattern = re.compile(r'(\d+)年(\d+)月(\d+)日')
            match = pattern.search(current_date)
            year = match.group(1)
            if int(match.group(2)) < 10:
                month = '0'+match.group(2)
            else:
                month = match.group(2)
            if int(match.group(3)) < 10:
                day = '0'+match.group(3)
            else:
                day = match.group(3)
            date = year+month+day

        column_names = dict(map(lambda x: (x, []), name_lst))
        df = pd.DataFrame(column_names)
        i = 0
        for sec in rank_tbl.find_all('section'):
            rank = str(sec['data-rank'])
            page_url = work_url + sec['data-id']
            img_url = sec.find('img', {'class': "_thumbnail ui-scroll-view"})['data-src']

            page = Page(page_url, date, rank, img_url)
            page.parse(page.get_soup())
            page.results(True, self.is_ai)

            with warnings.catch_warnings():
                warnings.simplefilter(action='ignore', category=FutureWarning)
                df = df.append(page.dict_page, ignore_index=True)

            i += 1
            if 0 < self.tops <= i:
                break
        DAO.sav2csv(df, self.is_ai)
        return current_date

    def days_crawl(self):
        delta = datetime.timedelta(days=1)
        if self.begin_date == '':
            date_rec = self.daily_tops(date='')
            pattern = re.compile(r'(\d+)年(\d+)月(\d+)日')
            match = pattern.search(date_rec)
            url_date = datetime.date(int(match.group(1)),
                                     int(match.group(2)),
                                     int(match.group(3))) - delta
        else:
            datetime_obj = datetime.datetime.strptime(self.begin_date, '%Y%m%d')
            url_date = datetime_obj.date()

        while url_date >= self.end_date:
            predate = url_date.strftime('%Y%m%d')
            self.daily_tops(predate)
            url_date -= delta
