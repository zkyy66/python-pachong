# 导入第三方包
import requests
from bs4 import BeautifulSoup
import random
import time
from uaList import ua_list


def ua_list_random(ua_list, ua_limit):
    uaTemp = []
    ua = ua_list['browsers']
    ua_randomize = ua_list['randomize']
    for randVal in ua_randomize.values():
        uaTemp.append(ua[randVal][random.randrange(50)])
    return uaTemp[ua_limit]


# 通过循环实现多页图片的抓取
for page in range(1, 3):
    # 生成顶层图片列表页的链接
    fst_url = 'https://colorhub.me/search?tag=data&page={}'.format(page)
    ua = ua_list_random(ua_list, page)
    # 生成UA，用于爬虫请求头的设置
    # UA = UserAgent()
    # # 向顶层链接发送请求
    fst_response = requests.get(fst_url, headers={'User-Agent': ua})
    # 解析顶层链接的源代码
    fst_soup = BeautifulSoup(fst_response.text, "html.parser")
    # 根据HTML的标记规则，返回次层图片详情页的链接和图片名称
    sec_urls = [i.find('a')['href'] for i in fst_soup.findAll(name='div', attrs={'class': 'card'})]
    pic_names = [i.find('a')['title'] for i in fst_soup.findAll(name='div', attrs={'class': 'card'})]

    # 对每一个次层链接做循环
    for sec_url, pic_name in zip(sec_urls, pic_names):
        # 生成UA，用于爬虫请求头的设置
        ua = ua_list_random(ua_list, page)
        # 向次层链接发送请求
        sec_response = requests.get(sec_url, headers={'User-Agent': ua})
        # 解析次层链接的源代码
        sec_soup = BeautifulSoup(sec_response.text, "html.parser")
        # 根据HTML的标记规则，返回图片链接
        pic_url = 'https:' + sec_soup.find('img', {'class': 'card-img-top'})['src']
        # print(pic_url)
        # 对图片链接发送请求
        pic_response = requests.get(pic_url, headers={'User-Agent': ua})

        # 将二进制的图片数据写入到本地（即存储图片到本地）
        with open(pic_name + '.jpg', mode='wb') as fn:
            fn.write(pic_response.content)
            # 生成随机秒数，用于也没的停留
            seconds = random.uniform(1, 3)
            time.sleep(seconds)
