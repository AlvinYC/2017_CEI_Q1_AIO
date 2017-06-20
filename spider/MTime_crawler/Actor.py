#coding = utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
import codecs,time,random
year='2016'
output=codecs.open('Actor_cn_419.txt','w','utf-8')
url='http://movie.mtime.com/people/search/focus/#sortType=4&listType=0&r=1&pageIndex='
#url_all='http://movie.mtime.com/people/search/focus/#sortType=4&listType=0&r=3&pageIndex=391'
"""
#url_all='http://movie.mtime.com/movie/search/section/#pageIndex=18&year=2016'
driver = webdriver.PhantomJS(executable_path=r'C:/Users/Charliewk_chang/Desktop/phantomjs-2.1.1-windows/bin/phantomjs.exe')
driver.get(url_all)
pageSource=driver.page_source 
soup = BeautifulSoup(pageSource, 'lxml')
#output.write(soup.prettify())
#counter=0
#for a in soup.find_all("img",class_="img_box"):
    #output.write(a['alt']+'\n')
    #counter+=1
    #if counter==20:
        #break
        """
for i in range(419,437):
    url_all=url+str(i)
    print url_all
    driver = webdriver.PhantomJS(executable_path=r'C:/Users/Charliewk_chang/Desktop/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    driver.get(url_all)
    
    pageSource=driver.page_source 
    soup = BeautifulSoup(pageSource, 'lxml') 
    #print soup
    #output.write("page"+str(i))
    counter=0
    """
    for h3 in soup.find_all("h3",class_="normal mt6"):
        try:
            output.write(h3.a['href']+','+h3.a.string+'\n')
            counter+=1
        except:
            output.write(h3.a['href']+','+'name'+'\n')
            counter+=1 
    """
    for a in soup.find_all("img",class_="img_box"):
        output.write(a['alt']+'\n')
        counter+=1
        if counter==20:
            break        
    driver.close()
    if counter==20:
        output.write('Page'+str(i)+' Done'+'\n')
        print "done"
    else:
        output.write('Page'+str(i)+' Miss'+'\n')
        print 'miss'
        break
    time.sleep(8)