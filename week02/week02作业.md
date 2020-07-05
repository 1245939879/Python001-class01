## **作业一：**

 

* 为 Scrapy 增加代理 IP 功能。
* 将保存至 csv 文件的功能修改为保持到 MySQL，并在下载部分增加异常捕获和处理机制。

 

备注：代理 IP 可以使用 GitHub 提供的免费 IP 库。

 

### 初始化

```plain
1，在创建爬虫项目maoyanmovie
scrapy startproject maoyanmovie
2，进入爬虫器：cd maoyanmovie/maoyanmovie/spiders
3，产生一个爬虫器Spiders： scrapy genspider [Spiders名称] [网址]
scrapy genspider maoyan maoyan.com
生成maoyanmovie.py文件
```

maoyanmovie.py文件

```plain
import scrapy
from maoyanmovie.items import MaoyanmovieItem
from scrapy.selector import Selector
class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']
    # 解析函数
    def parse(self, response):
        xpathexp_main = '//div[@class="movie-hover-info"]'
        movies = Selector(response=response).xpath(xpathexp_main)
        for movie in movies[:10]:
            item = MaoyanmovieItem()
            xpathexp_sub = './div[1]/span[1]/text()'
            xpathtxt_sub = movie.xpath(xpathexp_sub)
            item['title'] = xpathtxt_sub.extract_first().strip()
            
            xpathexp_sub = './div[2]/text()[2]'
            xpathtxt_sub = movie.xpath(xpathexp_sub)
            item['movie_type'] = xpathtxt_sub.extract_first().strip()
            
            xpathexp_sub = './div[4]/text()[2]'
            xpathtxt_sub = movie.xpath(xpathexp_sub)
            item['time'] = xpathtxt_sub.extract_first().strip()
            yield item
            
```
### 修改items.py

```plain
    title=scrapy.Field()
    movie_type=scrapy.Field()
    time=scrapy.Field()
```

### 修改middlewares.py

```plain
#加入
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured
from collections import defaultdict
from urllib.parse import urlparse
import random

#加入
class RandomHttpProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, auth_encoding='utf-8', proxy_list = None):
        self.proxies = defaultdict(list)
        for proxy in proxy_list:
            parse = urlparse(proxy)
            self.proxies[parse.scheme].append(proxy)
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('HTTP_PROXY_LIST'):
            raise NotConfigured
        http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')  
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')
        return cls(auth_encoding, http_proxy_list)
    def _set_proxy(self, request, scheme):
        proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
```

### SQL

```plain
service mysql start
create database film;
create table film.film_name(title varchar(50),movie_type varchar(50),c_time varchar(50));
select * from film.film_name;
```


### 修改pipelines.py

```plain
from itemadapter import ItemAdapter
import pandas as pd 
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
dic_info ={'title':[],'movie_type':[],'time':[]}
path='./scrapy-xpath.csv'
class MaoyanmoviePipeline:
    def process_item(self, item, spider):
        conn = pymysql.connect(host = '127.0.0.1',
                                port = 3306,
                                user = 'root',
                                password = '123456',
                                database = 'test',
                                charset = 'utf8'
                                )
        cur=conn.cursor()
        result=[]
        values=(item['title'],item['movie_type'],item['time'])
        try:
            cur.execute('insert into film.film_name(title,movie_type,c_time) '+' values(%s,%s,%s)',values)
            # cur.execute('select * from film.film_name')
            result.append(cur.fetchall())
            cur.close()
            conn.commit()
            print(result)
        except Exception as a:
            print(a)
        conn.close()
        return item
```
### 修改settings.py

```plain
#加入
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
DOWNLOAD_DELAY = 1
COOKIES_ENABLED = False
#加入
DOWNLOADER_MIDDLEWARES = {
    'maoyanmovie.middlewares.MaoyanmovieDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'maoyanmovie.middlewares.RandomHttpProxyMiddleware': 400,
}
HTTP_PROXY_LIST = [
     'http://52.179.231.206:80',
     'http://95.0.194.241:9090',
]
ITEM_PIPELINES = {
    'maoyanmovie.pipelines.MaoyanmoviePipeline': 300,
}
```
### 设置代理

export http_proxy='http://52.179.231.206:80'

### 运行

scrapy crawl maoyan

### 查看

select * from film_name;


---


## **作业二：**

 使用 requests 或 Selenium 模拟登录石墨文档 [ https://shimo.im ](https://shimo.im)


