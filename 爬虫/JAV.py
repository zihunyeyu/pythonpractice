import requests
from bs4 import BeautifulSoup
import os
import time
base_url = 'https://javzoo.com'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
}


def makeanewdir(name):
    '''
    在当前目录下新建一个目录
    :param name: 新建目录名
    :return: 返回新建的目录名
    '''
    nowpath = os.path.abspath('.')
    newdirpath = os.path.join(nowpath,name)
    try:
        os.mkdir(newdirpath)
    except FileExistsError:
        print('当前目录下已存在同名目录')
    return newdirpath


def get_bs(target_url):
    '''
    获取目标网址的beautifulsoup
    :param target_url: 目标网址
    :return: beautifulsoup
    '''
    req = requests.get(target_url,headers=headers)
    beautifulsoup = BeautifulSoup(req.text,'html.parser')
    return beautifulsoup


def downloadpic(pic_url,name='pic',type='jpg',dir=""):
    '''
    获取图片
    :param pic_url: 目标网址
    :param name: 保存名称
    :param type: 保存格式
    :param dir: 可选保存目录
    :return:
    '''
    req = s=requests.get(pic_url, headers=headers)
    picname = dir+name+'.'+type
    try:
        with open(picname,'wb') as pic:
            pic.write(req.content)
    except FileNotFoundError:
        print('指定目录不存在！已为您新建目录：'+dir+'copy')
        makeanewdir(dir)
        with open(dir+name+'.'+type,'wb') as pic:
            pic.write(req.content)


def get_maxpages(url):
    '''
    获取搜索结果的最大页数
    :param url: 初始页面
    :return: 最大页数
    '''
    req = requests.get(url,headers=headers)
    search_bs = BeautifulSoup(req.text,'html.parser')
    if search_bs.find(text='下一页 '):
        while search_bs.find(text='下一页 '):
            next_url = base_url+search_bs.find(text='下一页 ').parent.previous_element.previous_sibling.a['href']
            req = requests.get(next_url,headers=headers)
            search_bs = BeautifulSoup(req.text,'html.parser')
        return int(next_url.split('/')[-1])
    else:
        return 1


def get_ed2k(fanhao,dir=''):
    baseurl1 = 'https://www.clb8.net'
    searchurl = baseurl1+'/s/{}.html'.format(fanhao)
    soup = get_bs(searchurl)
    if '约0条' not in soup.find('div',class_="search-statu").text:
        for a_ in soup.find_all('div',class_="search-item"):
            url = baseurl1+a_.find('a')['href']
            name = a_.find('a').text
            ed2k = get_bs(url).find('a',class_='download')['href']
            try:
                with open(dir+fanhao+'_ed2k.txt','a+') as f:
                    f.write(name+':\t'+ed2k+'\n')
            except:
                pass
        print(fanhao + '\tGet!')
    else:
        with open(dir+'该片没资源.txt', 'a+'):
            print(fanhao+'好像没资源哦~')


def downloadinfos(AVinfos):
    for info in AVinfos:
        movie_url = info.a['href']
        name = info.img['title']
        fanhao = info.span.date.text
        #创建一个番号_名称的文件夹
        os.chdir(motopath)
        avdir = makeanewdir(fanhao+'_'+name)
        get_ed2k(fanhao,avdir+'\\')
        time.sleep(1)
        movie_bs = get_bs(movie_url)
        #下载封面图片
        fengmianpicurl = movie_bs.find('a',class_="bigImage")['href']
        downloadpic(fengmianpicurl,fanhao+'_0','jpg',avdir+'\\')
        #movie_bs.h3.text
        #下载样图
        samplepicurls = movie_bs.find_all('a',class_="sample-box")
        num = 1
        for picurl in samplepicurls:
            url = picurl['href']
            type = url.split('.')[-1]
            bianhao = str(num)
            downloadpic(url,fanhao+'_'+bianhao,type,avdir+'\\')
            num+=1


def get_searchinfos(searchmessage):
    '''
    获取搜素目标的信息
    :param searchmessage:搜索对象，女优名字或者番号
    :return:
    '''
    search_url = 'https://javzoo.com/cn/search/{}'.format(searchmessage)
    search_bs = get_bs(search_url)
    if search_bs.h4.text != '搜寻没有结果。':
        maxpages = get_maxpages(search_url)
        for page in range(1,maxpages+1):
            everypageurl = search_url+'/page/'+str(page)
            AVinfos = get_bs(everypageurl).find_all('div',class_='item')
            downloadinfos(AVinfos)
            time.sleep(3)
    else:
        print('没有相关女优或者作品')


def main():
    while True:
        searchmessage = input('输入搜索信息（女优名字或者番号）：')
        get_searchinfos(searchmessage)
        q = input('继续搜索请输入"yes",输入其他任意字符为退出')
        if q.lower() != 'yes':
            break


if __name__ == '__main__':
    motopath = makeanewdir('AVinfos')
    print(motopath)
    main()

