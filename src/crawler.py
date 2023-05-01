# coding=utf-8
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from pageParser import Page, name_lst
from dao import DAO
import datetime
import re
import pandas as pd
import warnings


# AI生成从31/10/2022开始
def daily_tops(date, tops=0, ai_type=''):
    if date == '' or date is None:
        if ai_type == '':
            url = 'https://www.pixiv.net/ranking.php'
        else:
            url = 'https://www.pixiv.net/ranking.php?mode=daily_ai'
        date = datetime.date.today().strftime('%Y%m%d')
    else:
        url = 'https://www.pixiv.net/ranking.php?mode=daily{ai_flag}&date={date}'\
            .format(ai_flag=ai_type, date=date)

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

    column_names = dict(map(lambda x: (x, []), name_lst))
    df = pd.DataFrame(column_names)
    i = 0
    for sec in rank_tbl.find_all('section'):
        rank = str(sec['data-rank'])
        page_url = work_url + sec['data-id']
        img_url = sec.find('img', {'class': "_thumbnail ui-scroll-view"})['data-src']

        page = Page(page_url, date, rank, img_url)
        page.parse(page.get_soup())
        page.results(True)

        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            df = df.append(page.dict_page, ignore_index=True)

        i += 1
        if 0 < tops <= i:
            break
    DAO.sav2csv(df)
    return current_date


def days_crawl(tops=50, ai_type=''):
    end_date = datetime.date(2022, 10, 31)
    delta = datetime.timedelta(days=1)

    date_rec = daily_tops('', tops, ai_type)
    pattern = re.compile(r'(\d+)年(\d+)月(\d+)日')
    match = pattern.search(date_rec)
    url_date = datetime.date(int(match.group(1)),
                             int(match.group(2)),
                             int(match.group(3))) - delta
    # url_date = datetime.date(2022, 10, 31)  # start_date for test

    while url_date >= end_date:
        predate = url_date.strftime('%Y%m%d')
        daily_tops(predate, tops, ai_type)
        url_date -= delta


if __name__ == '__main__':
    days_crawl(tops=50)
    # daily_tops('20230426', tops=1, ai_type='_ai')
