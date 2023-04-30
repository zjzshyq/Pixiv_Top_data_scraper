import redis
import sqlite3
import pandas as pd


class DAO(object):
    def __init__(self, db=0):
        try:
            self.rd = redis.Redis(host='localhost', port=6379, db=db)
            self.sqlite = sqlite3.connect(database='../data/pixiv.db')
        except:
            self.rd = ''
            print('redis server is off')

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
        if int(rank) < 10:
            rank = '0'+str(rank)
        else:
            rank = str(rank)
        val = ';'.join([pid, rank, date, img_url])
        self.rd.lpush(lname, val)

    def img_queue_pop(self, lname='img'):
        if self.rd.llen(lname) > 0:
            return self.rd.lpop(lname).decode('utf-8')
        else:
            return 'End of Redis Queue.'

    def rd2csv(self):
        1

    @staticmethod
    def info2csv(name_lst, page_dict):
        header = dict(map(lambda x: (x, []), name_lst))
        df = pd.DataFrame(header)
        df = df.append(pd.Series(page_dict), ignore_index=True)
        print(df)
