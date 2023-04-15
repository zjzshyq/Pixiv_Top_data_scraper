# coding=utf-8
from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen
import json
import re
re.compile('^<.*>$')

url= 'https://www.pixiv.net/artworks/102345178'
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

dict_page['tid'] = page_id
dict_page['title'] = info['title']
dict_page['uid'] = info['userId']

dict_page['desc'] = desc
dict_page['tags'] = '/'.join(info['tags']) if info['tags'] is not None else ''
dict_page['uname'] = info['userName']
dict_page['date'] = info['createDate'] # 从外层获取
dict_page['rank'] = 0 # 从外层获取
dict_page['aiType'] = info['aiType'] # 1非ai，2ai

dict_page['views'] = illust['viewCount']
dict_page['comments'] = illust['commentCount']
dict_page['likes'] = illust['likeCount']
dict_page['bookmarks'] = illust['bookmarkCount']
# dict_page['update_date'] = info['updateDate']

for k in dict_page.keys():
    print(k+':',dict_page[k])