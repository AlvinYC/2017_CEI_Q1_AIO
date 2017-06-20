#coding=utf-8

import requests
from bs4 import BeautifulSoup
import lxml

#送出GET請求到遠端伺服器，伺服器接受請求後回傳<Response [200]>，代表請求成功
for i in range(1,117):
    url="http://www.mobile01.com/waypointtopiclist.php?f=198&p="+str(i)
    res = requests.get(url)

    #經過BeautifulSoup內lxml編輯器解析的結果
    soup = BeautifulSoup(res.text,'lxml')
    #rint soup.find_all("a",class_='topic_gen')
    for link in soup.find_all("a",class_='topic_gen'):
        print(link.get('href'))
#印出網頁內容
#print soup 

#使用select選取特定元素
#title = soup.select('#h1')[0].text
#content = soup.select('#summary')[0].text

#印出標題及內文
#print title
#print content