from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import ftfy
import pytz
import json
import time
import re
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
name_lst_outside = ['pid', 'date', 'rank', 'img', 'crawl_time']  # str
name_lst_info = ['title', 'uid', 'uname', 'aiType', 'tags',
                 'desc', 'create_time', 'update_time']  # all str
name_lst_illust = ['views', 'comments', 'likes', 'bookmarks']  # all int
name_lst = name_lst_outside + name_lst_info + name_lst_illust


driver = webdriver.Chrome()
# gecko_path = '/opt/homebrew/bin/geckodriver'
# ser = Service(gecko_path)
# options = webdriver.firefox.options.Options()
# options.headless = False
# #options.add_argument('-headless')
# driver = webdriver.Firefox(options = options, service=ser)
# options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0')  User-Agent

end_date = '20230603'
is_ai = True
end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
delta = datetime.timedelta(days=1)
current_date = datetime.datetime.now()
current_date -= delta
start_urls = []
while current_date >= end_date:
    current_date -= delta

    url = 'https://www.pixiv.net/ranking.php?mode=daily{ai_flag}&date={date}' \
        .format(ai_flag='_ai' if is_ai else '', date=current_date.strftime('%Y%m%d'))
    start_urls.append(url)

top_links = []
work_url = 'https://www.pixiv.net/artworks/'
i = 0
for url in start_urls:
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    rank_tbl = soup.find('div', {'class': 'ranking-items adjust'})

    for sec in rank_tbl.find_all('section'):
        try:
            page_url = work_url + sec['data-id']
        except Exception as e:
            page_url = None
            print(e)
        top_links.append(page_url)

        if i > 9:
            break
        i += 1
    time.sleep(5)

page_dict_lst = []
for link in top_links:
    time.sleep(2)
    dict_page = {}
    is_dynamic = False

    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

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
    if is_ai:
        dict_page['aiType'] = '2'
    else:
        dict_page['aiType'] = '1'

    try:
        js = json.loads(soup.find_all('meta')[-1]['content'])
        if type(js) != dict:
            is_dynamic = True
    except Exception as e:
        print('meta', e)
        is_dynamic = True
        js = None

    # for dynamic
    if is_dynamic:
        fig_caption = soup.find('figcaption')
        print(link)
        print('浏览量', fig_caption.find('dd', {'title': '浏览量'}).text)
        print('赞！', fig_caption.find('dd', {'title': '赞！'}).text)
        print('收藏', fig_caption.find('dd', {'title': '收藏'}).text)

        try:
            title_h1 = fig_caption.find_all('h1')[0]
            txt = title_h1.text
            dict_page['title'] = ftfy.fix_text(txt)
        except Exception as e:
            dict_page['title'] = ''
            print('title', e)

        try:
            desc = ''
            dict_page['desc'] = ftfy.fix_text(desc)
        except Exception as e:
            dict_page['desc'] = ''
            print('desc', e)

        try:
            time_str = fig_caption.find('div', {'title': '投稿时间'}).text
            time_obj = datetime.datetime.strptime(time_str, "%Y年%m月%d日[上午下午凌晨]%H点%M分")
            target_timezone = pytz.timezone("Asia/Tokyo")
            target_format = "%Y-%m-%dT%H:%M:%S%z"
            create_time = time_obj.astimezone(target_timezone).strftime(target_format)

            dict_page['create_time'] = create_time
            dict_page['update_time'] = create_time
        except Exception as e:
            dict_page['create_time'] = ''
            dict_page['update_time'] = ''
            print('create_time', e)

        # tags
        try:
            tag_lst = []
            li_lst = fig_caption.find('footer').find_all('li')
            for li in li_lst[1:]:
                tag = ftfy.fix_text(li.find('a').text)
                if tag:
                    tag_lst.append(tag)
            dict_page['tags'] = '/'.join(tag_lst)
        except Exception as e:
            dict_page['tags'] = -1
            print('tags', e)

        dict_page['comments'] = 0
        try:
            txt = fig_caption.find('dd', {'title': '赞！'}).text
            dict_page['likes'] = int(txt.replace(',', ''))
        except Exception as e:
            dict_page['likes'] = -1
            print('likes', e)
        try:
            txt = fig_caption.find('dd', {'title': '收藏'}).text
            dict_page['bookmarks'] = int(txt.replace(',', ''))
        except Exception as e:
            dict_page['bookmarks'] = -1
            print(e)
        try:
            txt = fig_caption.find('dd', {'title': '浏览量'}).text
            dict_page['views'] = int(txt.replace(',', ''))
        except Exception as e:
            dict_page['views'] = -1
            print(e)

        try:
            dict_page['img'] = work_url+page_id#driver.find_element(By.XPATH, '/html/head/link[3]')
        except Exception as e:
            dict_page['title'] = ''
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
            dict_page['uid'] = str(info['userId']) #or str(info['authorId'])
        except Exception as e:
            dict_page['uid'] = ''
            print(e)
        try:
            dict_page['update_time'] = info['updateDate']
        except Exception as e:
            dict_page['update_time'] = ''
            print(e)
    # for static
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
            dict_page['img'] = work_url+page_id#driver.find_element(By.XPATH, '/html/head/link[3]')
        except Exception as e:
            dict_page['title'] = ''
            print(e)

        try:
            dict_page['title'] = ftfy.fix_text(info['title'])
        except Exception as e:
            dict_page['title'] = ''
            print(e)

        try:
            dict_page['uid'] = str(info['userId']) #or str(info['authorId'])
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
        try: # 加进去的
            dict_page['aiType'] = str(info['aiType'])  # 0被认证的原创作品，1非ai，2ai
        except Exception as e:
            dict_page['aiType'] = ''
            print(e)# 加进去的
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

pd.DataFrame.from_records(page_dict_lst).to_csv('./data.csv', index=False)
