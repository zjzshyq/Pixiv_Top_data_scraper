import sqlite3
import os
from crawler import Crawler


try:
    os.mkdir('../data')
    os.mkdir('../covers')
except FileExistsError:
    print(FileExistsError)

conn = sqlite3.connect(database='../data/pixiv.db')
cursor = conn.cursor()
cursor.execute('SELECT SQLITE_VERSION()')
data = cursor.fetchone()
print("SQLite version:", data[0])

crawl = Crawler(tops=2, is_ai=True)
crawl.set_end_date('20230428')
crawl.days_crawl()
# crawl.daily_tops('20230426')
