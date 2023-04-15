# coding=utf-8
from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen
import json
import re
re.compile('^<.*>$')

url= 'https://www.pixiv.net/artworks/107094071'
headers={"User-Agent": "Mozilla/5.0"}
request_site = Request(url, headers={"User-Agent": "Mozilla/5.0", 'Content-type': "text/html"})
webpage = urlopen(request_site)
bs = BS(webpage.read(), 'html.parser')

page_id = url.split('/')[-1]
js = json.loads(bs.find_all('meta')[-1]['content'])
illust = js['illust'][page_id]
info = illust['userIllusts'][page_id]

dict_page = {}

pattern = re.compile(r'<.+?>')
desc = info['description']
for s in re.findall(pattern, desc):
    desc = desc.replace(s, '')

dict_page['title'] = info['title']
dict_page['desc'] = desc
dict_page['tags'] = '/'.join(info['tags']) if info['tags'] is not None else ''
dict_page['uid'] = info['userId']
dict_page['uname'] = info['userName']
dict_page['create_date'] = info['createDate']
dict_page['update_date'] = info['updateDate']
dict_page['aiType'] = info['aiType'] # 1非ai，2ai
dict_page['views'] = illust['viewCount']
dict_page['comments'] = illust['commentCount']
dict_page['likes'] = illust['likeCount']
dict_page['bookmarks'] = illust['bookmarkCount']

for k in dict_page.keys():
    print(k+':',dict_page[k])