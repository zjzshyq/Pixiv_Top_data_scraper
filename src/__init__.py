import sqlite3
import os


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
