import sqlite3
import os
import conf
from crawler import Crawler


try:
    os.mkdir(os.path.join(conf.proj_dir, 'data'))
    os.mkdir(os.path.join(conf.proj_dir, 'covers'))
except FileExistsError:
    print('files already exist.')

conn = sqlite3.connect(database=os.path.join(conf.proj_dir, 'pixiv.db'))
cursor = conn.cursor()
cursor.execute('SELECT SQLITE_VERSION()')
data = cursor.fetchone()
print("SQLite version:", data[0])

crawl = Crawler(tops=conf.tops, is_ai=conf.is_ai)
crawl.set_date(conf.begin_date, conf.end_date)
crawl.days_crawl()
