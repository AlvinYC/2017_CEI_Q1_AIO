#coding=utf-8

import requests
from bs4 import BeautifulSoup
import lxml

#�e�XGET�ШD�컷�ݦ��A���A���A�������ШD��^��<Response [200]>�A�N��ШD���\
for i in range(1,117):
    url="http://www.mobile01.com/waypointtopiclist.php?f=198&p="+str(i)
    res = requests.get(url)

    #�g�LBeautifulSoup��lxml�s�边�ѪR�����G
    soup = BeautifulSoup(res.text,'lxml')
    #rint soup.find_all("a",class_='topic_gen')
    for link in soup.find_all("a",class_='topic_gen'):
        print(link.get('href'))
#�L�X�������e
#print soup 

#�ϥ�select����S�w����
#title = soup.select('#h1')[0].text
#content = soup.select('#summary')[0].text

#�L�X���D�Τ���
#print title
#print content