#coding=utf-8

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import lxml,re,codecs
input_url=codecs.open('mobile_food_nantou_url.txt','r','utf-8')
foutput=codecs.open('article/mobile01_food_nantou.txt','w','utf-8')
#送出GET請求到遠端伺服器，伺服器接受請求後回傳<Response [200]>，代表請求成功
for waypoint in input_url:
    url='http://www.mobile01.com/'+waypoint
    res = requests.get(url)
    #經過BeautifulSoup內lxml編輯器解析的結果
    soup = BeautifulSoup(res.text,'lxml')


    div_content=soup.find_all("div",class_='single-post-content')
    cleanr = re.compile('<.*?>')
    #foutput=codecs.open('abc.txt','w','utf-8')
    final_content=[]
    for content in div_content:
        str_content = str(content)
        str_content = re.sub(cleanr, '', str_content)
        str_content = str_content.strip().replace('\n','').replace('\r','')
        final_content.append(str_content)
    final_content=''.join(final_content).decode("utf-8")
    #print final_content
    try:
        foutput.write(final_content+'\n')
    except:
        pass    
#print type(final_content)