'''
设计爬虫目标，输入电影名称，返回是否下载资源
有：获取下载链接
没有：返回失败结果
'''

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}

def get_downloadlink(moive_url):
    '''
    爬去bdmovie电影页面的下载链接
    :param moive_url: 目标url
    :return: 返回一个下载工具，链接的词典
    '''
    #爬出下载链接
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # 设置headless模型
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=chrome_options,desired_capabilities=dcap)
    driver.get(moive_url)
    data = driver.page_source
    downloadlinks = {}
    ed2k = r'"(ed2k[^"]+)"'
    magnet = r'"(magnet:\?xt=urn:btih:[^"]+)"'
    xunlei = r'"(thunder:[^"]+)"'
    baidu = r'<a title=".*" href="([^"]+)" target="_blank">.*span>([a-zA-Z0-9]{4})</span></div></div>'
    downloadlinks['ed2k'] = set(re.findall(ed2k,data))
    downloadlinks['磁力链接'] = set(re.findall(magnet,data))
    downloadlinks['迅雷'] = set(re.findall(xunlei,data))
    downloadlinks['百度网盘'] = set(re.findall(baidu,data))
    rname = r'<h3>(.+)</h3>'
    print(re.search(rname,data).group(1))
    driver.quit()
    return downloadlinks
def selectmovie(bsoup):
    '''
    捕捉搜索页面，并进行选择要查找的电影
    :param bsoup: 搜索页面的beautifulsoup
    :return: 电影链接
    '''
    name_urls = {}
    select_items = {}
    lists = bsoup.find_all('li',class_='list-item')
    n = 1
    for list in lists:
        name = list.find('a').text.strip()
        murl = list.find('a')['href'].strip()
        name_urls[name] = murl
        select_items[str(n)] = name
        print(str(n)+':\t'+name)
        n+=1
    select_index = input('输入想查找电影的序号(多个选择用","分隔):')
    urls = []
    try:
        indexs = select_index.split(',')
        for index in indexs:
            urls.append(name_urls[select_items[str(index)]])
    except KeyError:
        print('输入序号有问题！')
    return urls
def main(searchinfourl):
    req = requests.get(searchinfourl, headers=headers)
    bsoup = BeautifulSoup(req.text, 'html.parser')
    if bsoup.find('span', class_='badge badge-warning').text != '0 条':
        urls = selectmovie(bsoup)
        for url in urls:
            downloadlinks = get_downloadlink(url)
            for tool, links in downloadlinks.items():
                print(tool + ':')
                for link in links:
                    print(link)
        pass
    else:
        print('目标网站暂时没有该影视资源嗷！')
if __name__=='__main__':
    target_url = 'https://www.bd-film.cc/'
    moviename = input('输入搜索的电影名称：')
    searchinfourl = target_url+'search.jspx?q={}'.format(moviename)
    main(searchinfourl)



