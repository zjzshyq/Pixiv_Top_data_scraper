# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
# import pandas as pd
# user_head = 'https://www.pixiv.net/en/users/'
# df = pd.read_csv('../../../../data/tops.csv')
# uids = df['uid'].unique()
# user_urls = list(map(lambda x: user_head+str(x), uids))
# print(user_urls)
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
# webpage = request.urlopen(response.url)
url = 'https://www.pixiv.net/ranking.php?mode=daily_ai'
header = {"User-Agent": "Mozilla/5.0", 'Content-type': "text/html"}
request_site = Request(url, headers=header)
webpage = urlopen(request_site)
bs = BeautifulSoup(webpage.read(), 'html.parser')
work_url = 'https://www.pixiv.net/artworks/'
rank_tbl = bs.find('div', {'class': 'ranking-items adjust'})
for sec in rank_tbl.find_all('section'):
    page_url={}
    try:
        page_url['link'] = work_url + sec['data-id']
    except Exception as e:
        page_url['link'] = None
        print(e)
    print(page_url['link'])

