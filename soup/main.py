import sqlite3
import os
import conf
from crawler import Crawler


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

crawl = Crawler(tops=conf.tops, is_ai=conf.is_ai)
crawl.set_date(conf.begin_date, conf.end_date)
crawl.days_crawl()