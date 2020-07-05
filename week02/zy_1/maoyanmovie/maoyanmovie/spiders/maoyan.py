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
            
