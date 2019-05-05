'''
设计爬虫目标，输入电影名称，返回是否下载资源
有：获取下载链接
没有：返回失败结果
'''

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import re

target_url = 'https://www.bd-film.cc/'

moviename = input('输入搜索的电影名称：')
searchinfourl = target_url+'search.jspx?q={}'.format(moviename)
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
req = requests.get(searchinfourl,headers=headers)
'<span class="badge badge-warning">0 条</span>'
bsoup =BeautifulSoup(req.text,'html.parser')
print(bsoup.find('span',class_='badge badge-warning').text)
if bsoup.find('span',class_='badge badge-warning').text != '0 条':
    print('there have some infomation')
