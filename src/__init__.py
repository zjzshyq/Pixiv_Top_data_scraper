import sqlite3
import os

try:
    os.mkdir('../data')
    os.mkdir('../covers')
except Exception as e:
    print(e)

conn = sqlite3.connect(database='../data/pixiv.db')
conn.close()
