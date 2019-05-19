import requests
from bs4 import BeautifulSoup
import re
import time
headers = {
    'referer': 'https://www.chepaishe1.com/xiyouchepai/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}


def download_pic(pic_url, name='pic'):
    req = requests.get(pic_url, headers=headers)
    with open('c:\\AV\\' + name + '.' + pic_url.split('.')[-1], 'wb') as pic:
        pic.write(req.content)


def get_beautiful_soup(url):
    req = requests.get(url, headers=headers)
    return BeautifulSoup(req.text, 'html.parser')


def designation_pic_url(url):
    bs = get_beautiful_soup(url)
    designations = [designation.text for designation in bs.find_all('h2', class_="entry-title")]
    p = r"src=(https://www\.chepaishe1\.com[^']+?\.[a-z]{3})"
    pic_urls = re.findall(p, bs.prettify(), re.S)
    return dict(zip(designations, pic_urls))


if __name__ == '__main__':
    for page in range(1,132):
        page_url = 'https://www.chepaishe1.com/xiyouchepai/page/{}/'.format(page)
        for name, pic_url in designation_pic_url(page_url).items():
            try:
                download_pic(pic_url, name)
                print(name+'\tsuccess')
            except:
                print(name+'\terror')
            time.sleep(2)

