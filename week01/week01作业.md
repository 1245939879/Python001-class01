# 作业01_1

安装并使用 requests、bs4 库，爬取[猫眼电影](https://maoyan.com/films?showType=3)（）的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。

定义好user_agent，cookie：进入页面，F12进入开发模式获取

将页面内容存到文件  ./bs_info.txt 里，

再次运行时，先读取有没有该文件，如果有就直接读文件内容，不去爬虫。

如果没有，就爬虫回来，并且保存进该文件。

filename = './bs_info.txt'

responsetext = readfile(filename)

遍历所有'class': 'movie-hover-info'的标签，限定10个

然后再遍历所有'class': 'movie-hover-title'的标签，它们分别是电影名称、电影类型、主演和上映时间

for divtag in tags.find_all('div', attrs={'class': 'movie-hover-title'}):

电影名称找span里的文本

电影类型找'class': 'hover-tag'文本是"类型:"的文本内容

上映时间找'class': 'hover-tag'文本是"上映时间:"的文本内容

然后写入文件

```plain

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
# bs4是第三方库需要使用pip命令安装
def writefile(filename, content_text):
    with open(filename, 'w') as f:
        f.write(content_text)
def readfile(filename):
    with open(filename, 'r') as f:
        file_text = f.read()
    return file_text
# Python 使用def定义函数，myurl是函数的参数
def get_url_name(myurl):
    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
    cookie = 'Cookie: uuid_n_v=v1; uuid=CE180950B88E11EA8E55532676AF0F4A3F62B12A9AE14493A7A3B8A389017E89; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593273408,1593352474; _lxsdk_cuid=172f67edbc9c8-05eaeb2c35a8258-386b4644-1fa400-172f67edbc9c8; _lxsdk=CE180950B88E11EA8E55532676AF0F4A3F62B12A9AE14493A7A3B8A389017E89; __mta=174432157.1593273408685.1593278724870.1593352474395.4; mojo-uuid=3e6d068da9af7fa8fd53b65d2d9fe899; _csrf=ef923e139f55433b37ae0f17e9cf7c7ea21f4fd39e3d94f69033ab4dbdf51213; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593352474; _lxsdk_s=172fb82656f-36a-3e7-6e0%7C%7C1'
    header = {'user-agent': user_agent, 'Cookie': cookie}

    filename = './bs_info.txt'
    responsetext = readfile(filename)

    if len(responsetext) == 0:
        response = requests.get(myurl, headers=header)
        print(f'返回码是: {response.status_code}')
        if response.status_code == 200:
            writefile(filename, response.text)
            responsetext = response.text

    bs_info = bs(responsetext, 'html.parser')

    movie_list = []
    i = 0
    # print(bs_info)
    # Python 中使用 for in 形式的循环,Python使用缩进来做语句块分隔
    for tags in bs_info.find_all('div', attrs={'class': 'movie-hover-info'}):
        if i >= 10:
            break
        i += 1
        print(i)
        # print(tags)
        # for tags in bs_info.find_all('dl', attrs={'class': 'movie-list'}):

        # for spantag in tags.find_all('span', attrs={'class': 'name'}):
        #     print('span:' + spantag.text)

        movie_name = ''
        movie_type = ''
        movie_zy = ''
        movie_sy = ''
        for divtag in tags.find_all('div', attrs={'class': 'movie-hover-title'}):
            moviename = divtag.find('span', attrs={'class': 'name'})
            # 获取电影名字
            if moviename is not None:
                movie_name = moviename.text
                print('电影名称:' + movie_name)
            
            movietags0 = divtag.find('span', attrs={'class': 'hover-tag'})
            if movietags0 is not None and movietags0.text == "类型:":
                movie_type = movietags0.next_sibling.strip()
                print('类型:' + movie_type)

            movietags1 = divtag.find('span', attrs={'class': 'hover-tag'})
            if movietags1 is not None and movietags1.text == "主演:":
                movie_zy = movietags1.next_sibling.strip()
                print('主演:' + movie_zy)

            movietags2 = divtag.find('span', attrs={'class': 'hover-tag'})
            if movietags2 is not None and movietags2.text == "上映时间:":
                movie_sy = movietags2.next_sibling.strip()
                print('上映时间:' + movie_sy)
            
            movie_list.append((movie_name,movie_type,movie_zy,movie_sy))
            
            if movie_list:
                movies = pd.DataFrame(data=movie_list)
                movies.to_csv('./movies.csv', encoding='utf8', index=False, header=False)



url = 'https://maoyan.com/films?showType=3'
get_url_name(url)

```


---


# 作业01_2

使用 Scrapy 框架和 XPath 抓取[猫眼](https://maoyan.com/films?showType=3) [电影](https://maoyan.com/films?showType=3)的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。

 

**猫眼电影网址：**[ https://maoyan.com/films?showType=3 ](https://maoyan.com/films?showType=3)

 **要求：**必须使用 Scrapy 框架及其自带的 item pipeline、选择器功能，不允许使用 bs4 进行页面内容的筛选。

## 课程回顾：

```plain
先获取第一个页面，保存页面
然后查看分页，进入第二个分页，保存页面
然后依次请求后面的页面，同样的方法保存页面
爬虫默认函数：parse是从起始页start_urls开始爬取的
我们要的是能自动转到下一页的再次爬取，所以不能使用默认的parse函数
先写前置逻辑，让爬虫能够翻页，根据不同页面进行循环
编写 def start_requests(self):
for i in range(0, 10):
url = f'https://movie.douban.com/top250?start={i*25}'
yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)
Request会调用下载器Downloader去真正发起请求
请求头文件在settings里
设置延时，都在settings里配置
在开头import scrapy就会自动导入这个配置文件了
Request里要2个参数，url：不同翻页请求的页面。callback：回调函数self.parse
然后重写parse函数，用来解析网页响应
每翻一页，都会调一次回调函数，用来提取网页里的内容
items组件通过管道方式进行数据储存，将数据丢到管道里，管道再去传递给不同的items
title_list = soup.find_all('div', attrs={'class': 'hd'})
        for i in title_list:
            # 在items.py定义
            item = DoubanmovieItem()
            title = i.find('a').find('span').text
            link = i.find('a').get('href')
            item['title'] = title
            item['link'] = link
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)
item = DoubanmovieItem()通过from doubanmovie.items import DoubanmovieItem
获取管道
打开items.py文件：
    title = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
里面定义了存储的设置项，要存储多少个具体项目就写多少个设置项
比如想存标题title，链接link，那就定义2个item
title = i.find('a').find('span').text  将a标签里的span的文本内容存起来
link = i.find('a').get('href')  将a标签里的链接href存起来
item['title'] = title  
item['link'] = link
将2个变量存到item字典里
yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)
会将取回来的item（标题，链接）再次调用回调函数parse2。
其中parse2才是真正需要解析的详细页面。parse解析的只是分页简介页面，通过分页简介页面里的链接调用parse2得到里面的详情。然后循环所有分页，得到所有详情。
    def parse2(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', attrs={'class': 'related-info'}).get_text().strip()
        item['content'] = content
        yield item
parse2里返回item会调用pipelines.py
    # 每一个item管道组件都会调用该方法，并且必须返回一个item对象实例或raise DropItem异常
    def process_item(self, item, spider):
        title = item['title']
        link = item['link']
        content = item['content']
        output = f'|{title}|\t|{link}|\t|{content}|\n\n'
        with open('./doubanmovie.txt', 'a+', encoding='utf-8') as article:
            article.write(output)
        return item
函数process_item负责将item的数据存起来到./doubanmovie.txt里
以后要改存储对象，比如存入数据库，则修改pipelines即可，不用修改解析函数parse2，实现解耦
```



## 作业开始

>使用 Scrapy 框架和 XPath 抓取猫眼 电影的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
>>猫眼电影网址： [https://maoyan.com/films?showType=3](https://maoyan.com/films?showType=3) 
> 要求：必须使用 Scrapy 框架及其自带的 item pipeline、选择器功能，不允许使用 bs4 进行页面内容的筛选。
### 步骤1

```plain
0，准备基础设施：pip install scrapy
1，进入爬虫根目录（spider/）
2，在创建爬虫项目maoyanmovie
scrapy startproject maoyanmovie
3，进入爬虫器：cd maoyanmovie/maoyanmovie/spiders
4，产生一个爬虫器Spiders： scrapy genspider [Spiders名称] [网址]
scrapy genspider maoyan https://maoyan.com/films?showType=3
生成maoyan.py文件

```

### 开始处理爬虫逻辑

### 研究页面结构

chrome进入F12， 查看猫眼 电影名称、电影类型和上映时间 的所属标签，使用XPath复制

观察结构，单部电影所需要的内容在

<dl class="movie-list">

<dd>

<div class="movie-item film-channel">

<div class="movie-item-hover">

<a href="/films/1250952" target="_blank" data-act="movie-click" data-val="{movieid:1250952}">

<div class="movie-hover-info">

这个标签下

因为只需要前 10 个电影，而每一个电影对象里都有<div class="movie-hover-info">这个标签，且这个标签里包含了所有需要的内容（电影名称、电影类型和上映时间），所以不必获得整个<dd>，只需要用XPath定位到<div class="movie-hover-info">即可。

右键，复制，copy XPath

//*[@id="app"]/div/div[2]/div[2]/dl/dd[1]/div[1]/div[2]/a/div

简化一下，XPath式子就是：  '//div[@class="movie-hover-info"]'

只需要前10，那么解析函数逻辑就是

response.xpath('//div[@class="movie-hover-info"]')[:10]:

### 修改配置文件

maoyanmovie/settings.py

```plain
#加入
USER_AGENT_LIST=[
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
import random
USER_AGENT = random.choice(USER_AGENT_LIST)
#原有
# Obey robots.txt rules
ROBOTSTXT_OBEY = True
#加入
#DOWNLOAD_DELAY = 3
DOWNLOAD_DELAY = 1
#加入maoyanmovie/pipelines.py的类MaoyanmoviePipeline
ITEM_PIPELINES = {
    'maoyanmovie.pipelines.MaoyanmoviePipeline': 300,
}
```
### 修改主逻辑

<div class="movie-hover-info">下有4组<div>标签，分别装着

电影名称、电影类型、主演、上映时间

电影名称取第一组<div>里的<span>的内容

电影类型取第二组<div>里的文本内容

主演在第三组<div>里文本内容，但不需要取

上映时间取第四组<div>里的文本内容

所以表达式：

电影名称='./div[1]/span[1]/text()'

电影类型='./div[2]/text()[2]'

上映时间='./div[4]/text()[2]'


引入MaoyanmovieItem

from maoyanmovie.items import MaoyanmovieItem

使用MaoyanmovieItem

item = MaoyanmovieItem()

spiders/maoyan.py

```plain
import scrapy
from maoyanmovie.items import MaoyanmovieItem
from scrapy.selector import Selector
......
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
### 修改items文件

主逻辑里使用了item['title']，item['movie_type']，item['time']

所以items文件也要进行更改

maoyanmovie/items.py文件

```plain
修改MaoyanmovieItem类
#注释原有的pass
    # pass
    title = scrapy.Field()
    movie_type = scrapy.Field()
    time = scrapy.Field()
```

### 修改管道

主逻辑里不断往item字典扔数据，管道负责从item字典拿数据，拿出来后保存到文件

maoyanmovie/pipelines.py

```plain
    def process_item(self, item, spider):
        title = item['title']
        movie_type = item['movie_type']
        time = item['time']
        output = f'|{title}|\t|{movie_type}|\t|{time}|\n\n'
        with open('./MaoYanmovie.txt', 'a+', encoding='utf-8') as article:
            article.write(output)
        return item
```
## 开始运行

#进入项目目录(maoyanmovie，包含settings.py的那个目录)

在shell里运行： scrapy crawl [爬虫name]

scrapy crawl maoyan

目录里就会多出一个文件

MaoYanmovie.txt


