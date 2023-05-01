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

crawl = Crawler(tops=50, is_ai=True)
crawl.days_crawl()

