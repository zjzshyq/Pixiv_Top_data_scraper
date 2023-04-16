# coding=utf-8
from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen
import re
import utils
from soup import Page

# yesterday 进入推荐页面需要 selenium
# AI生成从31/10/2022开始
# url = 'https://www.pixiv.net/ranking.php?mode=daily_ai'
url = 'https://www.pixiv.net/ranking.php'
headers={"User-Agent": "Mozilla/5.0", 'Content-type': "text/html"}
request_site = Request(url, headers=headers)
webpage = urlopen(request_site)
bs = BS(webpage.read(), 'html.parser')

work_url = 'https://www.pixiv.net/artworks/'
rank_tbl = bs.find('div', {'class': 'ranking-items adjust'})
date = bs.find('a', {'class': 'current', 'href': re.compile('date=')}).text

i = 0
for sec in rank_tbl.find_all('section'):
    pid = sec['data-id']
    rank = sec['data-rank']
    page_url = work_url + sec['data-id']
    img_url = sec.find('img', {'class': "_thumbnail ui-scroll-view"})['data-src']

    page = Page(page_url, date, rank)
    page.parse(page.get_soup())
    page.results()

    utils.download_cover(img_url, pid, date)

    i +=1
    if i>3:
        break
