import redis
import sqlite3
import pandas as pd
import datetime
import os
import conf


class DAO(object):
    def __init__(self):
        try:
            self.rd = redis.Redis(host=conf.redis_host, port=6379, db=conf.redis_db)
            self.rd.set('opt_date', str(datetime.date.today()))
            self.redis_server_flag = True
        except redis.exceptions.ConnectionError:
            self.rd = ''
            self.redis_server_flag = False
            print('redis server is off.')
        try:
            self.sqlite = sqlite3.connect(database=os.path.join(conf.proj_dir, 'pixiv.db'))
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
                crawl_time VARCHAR(25),
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
                tags,desc,crawl_time,create_time,update_time,
                views,comments,likes,bookmarks
            ) VALUES(
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )
        """

        values = (
            dict_page['pid'],
            dict_page['date'],
            dict_page['rank'],
            dict_page['img'],
            dict_page['title'],
            dict_page['uid'],
            dict_page['uname'],
            dict_page['aiType'],
            dict_page['tags'],
            dict_page['desc'],
            dict_page['crawl_time'],
            dict_page['create_time'],
            dict_page['update_time'],
            dict_page['views'],
            dict_page['comments'],
            dict_page['likes'],
            dict_page['bookmarks']
        )
        cursor = self.sqlite.cursor()
        cursor.execute(sql, values)

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

    def img_queue_push(self, pid, rank, date, img_url, lname='img', is_ai=False):
        if self.redis_server_flag:
            if int(rank) < 10:
                rank = '0'+str(rank)
            else:
                rank = str(rank)
            if not is_ai:
                val = ';'.join([pid, rank, date, img_url])
            else:
                val = ';'.join([pid, rank, date, img_url, 'ai'])
            self.rd.lpush(lname, val)
        else:
            print()

    def img_queue_pop(self, lname='img'):
        if self.redis_server_flag:
            if self.rd.llen(lname) > 0:
                return self.rd.lpop(lname).decode('utf-8')
            else:
                print('End of Redis Queue.')
                return None
        else:
            print('redis is un-connected')
            return None

    @staticmethod
    def sav2csv(df: pd.DataFrame, ai=False):
        print(df.head())
        data_dir = os.path.join(conf.proj_dir, 'data')
        if not ai:
            csv_dir = os.path.join(data_dir, 'tops.csv')
        else:
            csv_dir = os.path.join(data_dir, 'tops_ai.csv')
        header_flag = not os.path.isfile(csv_dir)
        df.to_csv(csv_dir, index=False, header=header_flag, mode='a')
