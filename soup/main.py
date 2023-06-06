import sqlite3
import os
import conf
from crawler import Crawler
from datetime import datetime, timedelta
import time

# init the files
try:
    os.mkdir(os.path.join(conf.proj_dir, 'data'))
    os.mkdir(os.path.join(conf.proj_dir, 'covers'))
except FileExistsError:
    print('files already exist.')

try:
    data_dir = os.path.join(conf.proj_dir, 'data')
    conn = sqlite3.connect(database=os.path.join(data_dir, 'pixiv.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT SQLITE_VERSION()')
    data = cursor.fetchone()
    print("SQLite version:", data[0])
except sqlite3.OperationalError:
    print('sqlite3 is not on.')

# a boolean parameter limiting the number of pages
if conf.lmt100pages:
    tops = 50
    begin_date = ''

    current_date = datetime.now()
    previous_date = current_date - timedelta(days=2)
    end_date = previous_date.strftime("%Y%m%d")
else:
    tops = conf.tops
    begin_date = conf.begin_date
    end_date = conf.end_date

# start to crawl
start_time = time.time()
crawl = Crawler(tops=tops, is_ai=conf.is_ai)
crawl.set_date(begin_date, end_date)
crawl.days_crawl()
print('soup cost:', time.time() - start_time)
