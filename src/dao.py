import redis
import sqlite3
import pandas as pd
import datetime


class DAO(object):
    def __init__(self, db=0):
        try:
            self.rd = redis.Redis(host='localhost', port=6379, db=db)
            self.rd.set('opt_date', datetime.date.today())
            self.redis_server_flag = True
        except redis.exceptions.ConnectionError:
            self.rd = ''
            self.redis_server_flag = False
            print('redis server is off.')
        try:
            self.sqlite = sqlite3.connect(database='../data/pixiv.db')
            self.create_tbl()
            self.sqlite_server_flag = True
        except sqlite3.OperationalError:
            self.sqlite = ''
            self.sqlite_server_flag = False
            print('Can\'t connect sqlite database')

    def create_tbl(self):
        sql = """
            CREATE TABLE IF NOT EXISTS pixiv_tops(
                pid VARCHAR(11),
                date VARCHAR(8),
                rank VARCHAR(2),
                img TEXT,
                title TEXT,
                uid VARCHAR(15),
                uname TEXT,
                aiType VARCHAR(1),
                tags TEXT,
                desc TEXT,
                create_time VARCHAR(25),
                update_time VARCHAR(25),
                views INTEGER,
                comments INTEGER,
                likes INTEGER,
                bookmarks INTEGER,
                PRIMARY KEY (pid, date)
            ) 
        """
        cursor = self.sqlite.cursor()
        cursor.execute(sql)
        cursor.close()

    def insert2sql(self, dict_page):
        sql = """
            INSERT OR IGNORE INTO pixiv_tops(
                pid,date,rank,img,title,uid,uname,aiType,
                tags,desc,create_time,update_time,
                views,comments,likes,bookmarks
            ) VALUES(
                \'{pid}\',\'{date}\',\'{rank}\',\'{img}\',\'{title}\',\'{uid}\',\'{uname}\',\'{aiType}\',
                \'{tags}\',\'{desc}\',\'{create_time}\',\'{update_time}\',
                {views},{comments},{likes},{bookmarks}
            )
        """.format(
            pid=dict_page['pid'],
            date=dict_page['date'],
            rank=dict_page['rank'],
            img=dict_page['img'],
            title=dict_page['title'],
            uid=dict_page['uid'],
            uname=dict_page['uname'],
            aiType=dict_page['aiType'],
            tags=dict_page['tags'],
            desc=dict_page['desc'],
            create_time=dict_page['create_time'],
            update_time=dict_page['update_time'],
            views=dict_page['views'],
            comments=dict_page['comments'],
            likes=dict_page['likes'],
            bookmarks=dict_page['bookmarks']
        )
        cursor = self.sqlite.cursor()
        cursor.execute(sql)
        self.sqlite.commit()
        if cursor.rowcount == 1:
            print("Insert successful!")
        else:
            print("Insert failed.")
        cursor.close()

    def drop_tbl(self, tbl='pixiv_tops'):
        sql = """
            DROP TABLE {tbl}
        """.format(tbl=tbl)
        cursor = self.sqlite.cursor()
        cursor.execute(sql)
        cursor.close()

    def info2rd(self, pid, page_dict):
        dict_drop_none = {}
        for k in page_dict:
            dict_drop_none[k] = '' if page_dict[k] is None else page_dict[k]
        self.rd.hmset(pid, dict_drop_none)

    def img2rd(self, pid, date, img_url):
        self.rd.set(pid+'_'+date, img_url)

    def delete(self, key):
        self.rd.delete(key)

    def img_queue_push(self, pid, rank, date, img_url, lname='img'):
        if self.redis_server_flag:
            if int(rank) < 10:
                rank = '0'+str(rank)
            else:
                rank = str(rank)
            val = ';'.join([pid, rank, date, img_url])
            self.rd.lpush(lname, val)
        else:
            print()

    def img_queue_pop(self, lname='img'):
        if self.redis_server_flag:
            if self.rd.llen(lname) > 0:
                return self.rd.lpop(lname).decode('utf-8')
            else:
                return 'End of Redis Queue.'
        else:
            return 'redis is un-connected'

    @staticmethod
    def sav2csv(df: pd.DataFrame):
        print(df.head())
        df.to_csv('../data/tops.csv', index=False, header=True)


if __name__ == '__main__':
    dao = DAO()
