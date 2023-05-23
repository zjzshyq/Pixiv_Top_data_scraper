from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import ftfy
import pytz
import json
import time
import re

name_lst_outside = ['pid', 'date', 'rank', 'img', 'crawl_time']  # str
name_lst_info = ['title', 'uid', 'uname', 'aiType', 'tags',
                 'desc', 'create_time', 'update_time']  # all str
name_lst_illust = ['views', 'comments', 'likes', 'bookmarks']  # all int
name_lst = name_lst_outside + name_lst_info + name_lst_illust

driver = webdriver.Chrome()

end_date = '20230522'
is_ai = True
end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
current_date = datetime.datetime.now()
delta = datetime.timedelta(days=1)
start_urls = []
while current_date >= end_date:
    current_date -= delta

    url = 'https://www.pixiv.net/ranking.php?mode=daily{ai_flag}&date={date}' \
        .format(ai_flag='_ai' if is_ai else '', date=current_date.strftime('%Y%m%d'))
    start_urls.append(url)

# top_links = []
# work_url = 'https://www.pixiv.net/artworks/'
# for url in start_urls:
#     driver.get(url)
#     page_source = driver.page_source
#     soup = BeautifulSoup(page_source, 'html.parser')
#     rank_tbl = soup.find('div', {'class': 'ranking-items adjust'})
#
#     for sec in rank_tbl.find_all('section'):
#         try:
#             page_url = work_url + sec['data-id']
#         except Exception as e:
#             page_url = None
#             print(e)
#         top_links.append(page_url)

page_dict_lst = []
top_links = ['https://www.pixiv.net/artworks/108297847', 'https://www.pixiv.net/en/artworks/108318799']
for link in top_links:
    dict_page = {}
    driver.get(link)
    is_dynamic = False
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    print(link)
    page_id = link.split('/')[-1]
    dict_page['pid'] = page_id

    now = datetime.datetime.now()
    tz = pytz.timezone('Asia/Tokyo')  # 转换为东京时区的时间
    now_tz = tz.localize(now)
    crawl_time_str = now_tz.strftime('%Y-%m-%dT%H:%M:%S%z')
    dict_page['crawl_time'] = crawl_time_str

    current_date = datetime.datetime.now()
    previous_date = current_date - datetime.timedelta(days=1)
    previous_date_str = previous_date.strftime('%Y%m%d')
    dict_page['date'] = previous_date_str

    try:
        js = json.loads(soup.find_all('meta')[-1]['content'])
        if type(js) != dict:
            is_dynamic = True
    except Exception as e:
        print('meta', e)
        continue

    if is_dynamic:
        fig_caption = soup.find('figcaption')
        print(fig_caption.find_all('h1')[0].text)
        print('浏览量', fig_caption.find('dd', {'title': '浏览量'}).text)
        print('赞！', fig_caption.find('dd', {'title': '赞！'}).text)
        print('收藏', fig_caption.find('dd', {'title': '收藏'}).text)

    else:
        try:
            illust = js['illust'][page_id]
        except Exception as e:
            for n in name_lst_info:
                dict_page[n] = ''
            illust = None
            print(e)

        try:
            info = illust['userIllusts'][page_id]
        except Exception as e:
            for n in name_lst_illust:
                dict_page[n] = -1
            info = None
            print(e)

        try:
            dict_page['title'] = ftfy.fix_text(info['title'])
        except Exception as e:
            dict_page['title'] = ''
            print(e)

        try:
            dict_page['uid'] = str(info['userId'])
        except Exception as e:
            dict_page['uid'] = ''
            print(e)

        try:
            dict_page['uname'] = ftfy.fix_text(info['userName'])
        except Exception as e:
            dict_page['uname'] = ''
            print(e)

        try:
            dict_page['create_time'] = info['createDate']
        except Exception as e:
            dict_page['create_time'] = ''
            print(e)

        try:
            dict_page['update_time'] = info['updateDate']
        except Exception as e:
            dict_page['update_time'] = ''
            print(e)

        try:
            dict_page['aiType'] = str(info['aiType'])  # 0被认证的原创作品，1非ai，2ai
        except Exception as e:
            dict_page['aiType'] = ''
            print(e)

        try:
            dict_page['tags'] = '/'.join(info['tags']) if info['tags'] is not None else ''
            dict_page['tags'] = ftfy.fix_text(dict_page['tags'])
        except Exception as e:
            dict_page['tags'] = ''
            print(e)

        try:
            pattern = re.compile(r'<.+?>')
            desc = info['description']
            for s in re.findall(pattern, desc):
                desc = desc.replace(s, '')
            dict_page['desc'] = ftfy.fix_text(desc)
        except Exception as e:
            dict_page['desc'] = ''
            print(e)

        try:
            dict_page['views'] = int(illust['viewCount'])
        except Exception as e:
            dict_page['views'] = -1
            print(e)

        try:
            dict_page['comments'] = int(illust['commentCount'])
        except Exception as e:
            dict_page['views'] = -1
            print(e)

        try:
            dict_page['likes'] = int(illust['likeCount'])
        except Exception as e:
            dict_page['likes'] = -1
            print(e)

        try:
            dict_page['bookmarks'] = int(illust['bookmarkCount'])
        except Exception as e:
            dict_page['bookmarks'] = -1
            print(e)
    page_dict_lst.append(dict_page)
    time.sleep(2)

pd.DataFrame.from_records(page_dict_lst).to_csv('./data.csv', index=False)
