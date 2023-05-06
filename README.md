### Pixiv_Top data_scraper
1. run \_\_init__.py to start the program.
2. crawler.py is to crawl page links.
3. pageParser.py is to parse single page.
4. dao.py is data persistence layer to operate sqlite, redis and csv.
5. downloader.py will get data from redis pipeline to download covers asynchronously.
6. conf.py is to the set the parameters for controlling the whole program.