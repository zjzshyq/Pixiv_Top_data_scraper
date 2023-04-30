# coding=utf-8
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from pageParser import Page
import datetime
# import re


# yesterday 进入推荐页面需要 selenium
# AI生成从31/10/2022开始
# url = 'https://www.pixiv.net/ranking.php?mode=daily_ai'
def daily_tops(date, tops=0):
    if date == '' or date is None:
        url = 'https://www.pixiv.net/ranking.php'
        date = datetime.date.today().strftime('%Y%m%d')
    else:
        url = 'https://www.pixiv.net/ranking.php?mode=daily&date='+date

    header = {"User-Agent": "Mozilla/5.0", 'Content-type': "text/html"}
    request_site = Request(url, headers=header)
    webpage = urlopen(request_site)
    bs = BeautifulSoup(webpage.read(), 'html.parser')

    work_url = 'https://www.pixiv.net/artworks/'
    rank_tbl = bs.find('div', {'class': 'ranking-items adjust'})
    # date = bs.find('a', {'class': 'current', 'href': re.compile('date=')}).text

    i = 0
    for sec in rank_tbl.find_all('section'):
        # pid = sec['data-id']
        rank = sec['data-rank']
        page_url = work_url + sec['data-id']
        img_url = sec.find('img', {'class': "_thumbnail ui-scroll-view"})['data-src']

        page = Page(page_url, date, rank, img_url)
        page.parse(page.get_soup())
        page.results(True)

        i += 1
        if 0 < tops <= i:
            break


def days_crawl():
    end_date = datetime.date(2023, 4, 28)
    delta = datetime.timedelta(days=1)
    today = datetime.date.today()
    url_date = today - delta

    while url_date >= end_date:
        predate = url_date.strftime('%Y%m%d')
        daily_tops(predate, 2)
        url_date -= delta


if __name__ == '__main__':
    days_crawl()
    # daily_tops('20230426', 2)
