# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import pandas as pd
user_head = 'https://www.pixiv.net/en/users/'
df = pd.read_csv('../../../../data/tops.csv')
uids = df['uid'].unique()
user_urls = list(map(lambda x: user_head+str(x), uids))
print(user_urls)
