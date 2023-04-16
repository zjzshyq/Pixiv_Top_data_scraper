# coding=utf-8
from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen
import json
import re
import utils

url= 'https://www.pixiv.net/artworks/102345178'
headers={"User-Agent": "Mozilla/5.0", 'Content-type': "text/html"}
request_site = Request(url, headers=headers)
webpage = urlopen(request_site)
bs = BS(webpage.read(), 'html.parser')

dict_page = {}
name_lst_info = ['title', 'uid', 'uname', 'aiType', 'tags', 'desc']
name_lst_illust = ['views', 'comments', 'likes', 'bookmarks']
name_lst_outside = ['rank', 'date', 'pid']

page_id = url.split('/')[-1]
try:
    js = json.loads(bs.find_all('meta')[-1]['content'])
except Exception as e:
    for n in name_lst_info+name_lst_illust:
        dict_page[n] = 'NA'
    js = 'NA'
    print(e)
try:
    illust = js['illust'][page_id]
except Exception as e:
    for n in name_lst_info:
        dict_page[n] = 'NA'
    illust = 'NA'
    print(e)

try:
    info = illust['userIllusts'][page_id]
except Exception as e:
    for n in name_lst_illust:
        dict_page[n] = 'NA'
    info = 'NA'
    print(e)

dict_page['pid'] = page_id # str类型，也可从外层获取
dict_page['rank'] = 'NA' # 从外层获取
dict_page['date'] = 'NA' # 外层获取

try:
    dict_page['title'] = info['title']
except Exception as e:
    dict_page['title'] = 'NA'
    print(e)

try:
    dict_page['uid'] = str(info['userId'])
except Exception as e:
    dict_page['uid'] = 'NA'
    print(e)

try:
    dict_page['uname'] = info['userName']
except Exception as e:
    dict_page['uname'] = 'NA'
    print(e)

try:
    dict_page['aiType'] = int(info['aiType'])  # 1非ai，2ai
except Exception as e:
    dict_page['aiType'] = 'NA'
    print(e)

try:
    dict_page['tags'] = '/'.join(info['tags']) if info['tags'] is not None else ''
except Exception as e:
    dict_page['tags'] = 'NA'
    print(e)

try:
    pattern = re.compile(r'<.+?>')
    desc = info['description']
    for s in re.findall(pattern, desc):
        desc = desc.replace(s, '')
    dict_page['desc'] = desc
except Exception as e:
    dict_page['desc'] = 'NA'
    print(e)

# dict_page['update_date'] = info['updateDate']
# dict_page['create_date'] = info['createDate']

try:
    dict_page['views'] = int(illust['viewCount'])
except Exception as e:
    dict_page['views'] = 'NA'
    print(e)

try:
    dict_page['comments'] = int(illust['commentCount'])
except Exception as e:
    dict_page['views'] = 'NA'
    print(e)

try:
    dict_page['likes'] = int(illust['likeCount'])
except Exception as e:
    dict_page['likes'] = 'NA'
    print(e)

try:
    dict_page['bookmarks'] = int(illust['bookmarkCount'])
except Exception as e:
    dict_page['bookmarks'] = 'NA'
    print(e)


for k in dict_page.keys():
    print(k+':',dict_page[k])
utils.sav2redis(page_id, dict_page)