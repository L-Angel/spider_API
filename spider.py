from db import run_sql
from config import start_urls
import urllib2
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
f=open('result2.txt','w+')
sys.stdout=f
def get_type_list(url):
    object=urllib2.urlopen(url)
    soup=BeautifulSoup(object.read(),'html.parser')
    cache=soup.find_all('dl')[0]
    cache=cache.find_all('dd')[1:-1]
    result=[]
    for item in cache:
        item.span.extract()
        c=[]
        c.append(item.a.string)
        c.append(url[:-5]+item.a['href'])
        result.append(c)
    return result

def get_API_list(url):
    object=urllib2.urlopen(url)
    soup=BeautifulSoup(object.read(),'html.parser')
    cache=soup.find_all('div',class_='juheapis_desc clearfix')
    result=[]
    for item in cache:
        c=[]
        item.img.extract()
        r=item.select('a')[1]
        c.append(r.string)
        c.append(url[:url.find('/',8)]+r['href'])
        result.append(c)
    cache=soup.select('.juheapi_next')
    if cache:
        if cache[0].has_attr('href'):
            u=url[:url.find('/',8)]+cache[0]['href']
            cc=[]
            cc=get_API_list(u)
            result.extend(cc)
    return result

def get_API_list_childrens(url):
    object=urllib2.urlopen(url)
    soup=BeautifulSoup(object.read(),'html.parser')
    cache=soup.select('.das_left a')
    result=[]
    for item in cache:
        c=[]
        c.append(item.string[item.string.index('.')+1:])
        c.append(url[:url.find('/',8)]+item['href'])
        result.append(c)
    return result

def get_API_info(url):
    object=urllib2.urlopen(url)
    soup=BeautifulSoup(object.read(),'html.parser')
    cache=soup.select('.simpleline')
    cache=cache[:4]
    result=[]
    for item in cache:
        c=[]
        c.append(item.strong.string[:-1])
        c.append(item.span.string)
        result.append(c)
    return result


if __name__ == '__main__':
    for item in get_type_list(start_urls[0]):
        print item[0]
        urls=get_API_list(item[1])
        for item2 in urls:
            print '----',item2[0],item2[1]
            for item3 in get_API_list_childrens(item2[1]):
                print '---- ----',item3[0],item3[1]
                for item4 in get_API_info(item3[1]):
                    print '---- ---- ----',item4[0],item4[1]