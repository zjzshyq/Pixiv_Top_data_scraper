# coding=utf-8
from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen

# yesterday 进入推荐页面需要 selenium
# AI生成从31/10/2022开始
# url = 'https://www.pixiv.net/ranking.php?mode=daily_ai'
url = 'https://www.pixiv.net/ranking.php'
headers={"User-Agent": "Mozilla/5.0"}
request_site = Request(url, headers={"User-Agent": "Mozilla/5.0", 'Content-type': "text/html"})
webpage = urlopen(request_site)
bs = BS(webpage.read(), 'html.parser')

work_url = 'https://www.pixiv.net/artworks/'
rank_tbl = bs.find('div', {'class': 'ranking-items adjust'})
for i, sec in enumerate(rank_tbl.find_all('section')):
    url = work_url+sec['data-id']
    print(sec['data-rank'], url)
    #print(sec)
