# 翻页的处理

import requests
from bs4 import BeautifulSoup as bs
# bs4是第三方库需要使用pip命令安装



def writefile(filename,content_text):
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
    header = {'user-agent':user_agent, 'Cookie' : cookie}

    filename = './bs_info.txt'
    responsetext = readfile(filename)

    if len(responsetext) == 0:
        response = requests.get(myurl,headers=header)
        print(f'返回码是: {response.status_code}')
        if response.status_code == 200:
            writefile(filename,response.text)
            responsetext = response.text

    bs_info = bs(responsetext, 'html.parser')

    i=0
    # print(bs_info)
    # Python 中使用 for in 形式的循环,Python使用缩进来做语句块分隔
    for tags in bs_info.find_all('div', attrs={'class': 'movie-hover-info'}):
        if i >= 10:
            break
        i+=1
        print(i)
        # print(tags)
        # for tags in bs_info.find_all('dl', attrs={'class': 'movie-list'}):
        for divtag in tags.find_all('div', attrs={'class': 'movie-hover-title'}):
            # 获取所有链接
            # print(divtag.get('href'))
            
            # 获取电影名字
            print(divtag.find('span').text)


url = 'https://maoyan.com/films?showType=3'
get_url_name(url)
