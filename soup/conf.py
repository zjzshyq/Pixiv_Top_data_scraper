import os

proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project direction
lmt100pages = True  # limit the number of pages in 100 regardless other parameters like tops, end_date.
begin_date = ''  # empty means from today, otherwise use YYYYMMDD date format
end_date = '20230603'  # empty means end at 20221031 when is AI begins, this end_date will be crawled too
tops = 50  # to control how many top pages per day you want to crawl
is_ai = True  # to crawl pictures generate by AI or not
redis_host = 'localhost'
redis_db = 0
