'''
爬取热销图书TOP500内容
'''
import requests
import re
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3738.0 Safari/537.36 Edg/75.0.107.0'
}
for page in range(1,26):
    url = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-24hours-0-0-1-{}'.format(str(page))
    req = requests.get(url,headers=headers)
    print(req.text)
